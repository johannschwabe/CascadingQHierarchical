import itertools
from typing import TYPE_CHECKING

from graphviz import Graph, Digraph

from BitSet import BitSet
from Relation import Relation
from RelationPattern import RelationPattern

if TYPE_CHECKING:
    from Query import Query


class VariableOrderNode:
    def __init__(self, name: str, children: "set[VariableOrderNode]", relations: "set[Relation]", parent: "VariableOrderNode|None"):
        self.children = children
        self.name = name
        self.relations = relations
        self.parent = parent
        self._all_relations_sources = set()
        self._all_relations_no_sources = set()
        self._parent_vars = set()
        self._views: "list[Relation]" = []

    def graph_viz(self, graph: "Digraph|None" = None, rootname: str = ""):
        own_name = f"{rootname}_{self.name}"
        graph.node(own_name, label=self.name)
        graph.node(rootname, style="invis")
        for child in self.children:
            child_name = f"{rootname}_{child.name}"
            graph.node(child_name, label=child.name)

            graph.edge(own_name, child_name)

        for child in self.children:
            child.graph_viz(graph, rootname)


        for relation in self.relations:
            relation_name = f"{rootname}_{relation.name}"
            graph.node(relation_name, shape="rectangle", label=str(relation))
            graph.edge(own_name, relation_name)
            if relation.sources:
                for source in relation.root_sources():
                    source_name = f"{rootname}_{source.name}"
                    graph.node(source_name, label=str(source), shape="diamond")
                    graph.edge(relation_name, source_name)
        return graph

    def views(self, query: "Query"):
        if self._views:
            return self._views
        sub_relations: "list[Relation|set[Relation]]" = []
        for child in self.children:
            sub_relations.append(child.all_relations(source_only=True))
        sub_relations.extend(self.relations)

        for i in range(len(sub_relations), 1, -1):
            for j, permutation in enumerate(itertools.combinations(sub_relations, i)):
                cleaned_relations = set()
                for choice in permutation:
                    if type(choice) == Relation:
                        cleaned_relations.add(choice)
                    else:
                        cleaned_relations.update(choice)
                varis = set()
                for relation in cleaned_relations:
                    varis.update(relation.free_variables)
                next_view = Relation(f"V_{query.name}@{self.name}_{i}_{j}", varis, list(cleaned_relations))
                self._views.append(next_view)

        return self._views


    def all_relations(self, source_only = False) -> "set[Relation]":
        if source_only and self._all_relations_sources:
            return self._all_relations_sources
        if not source_only and self._all_relations_no_sources:
            return self._all_relations_no_sources
        res = set()
        if source_only:
            for rel in self.relations:
                res.update(rel.root_sources())
        else:
            res.update(self.relations)
        for child in self.children:
            res.update(child.all_relations(source_only))
        if source_only:
            self._all_relations_sources = res
        else:
            self._all_relations_no_sources = res
        return res

    def copy(self, parent: "VariableOrderNode|None"):
        children = set(map(lambda x: x.copy(self), self.children))
        return VariableOrderNode(self.name, children, self.relations.copy(), parent)

    def parent_variables(self):
        if self._parent_vars:
            return self._parent_vars
        res = {self.name}
        if self.parent:
            res.update(self.parent.parent_variables())
        self._parent_vars = res
        return res

    def child_vars(self):
        res = {self.name}
        for child in self.children:
            res.update(child.child_vars())
        return res

    def parent_relations(self):
        if self.parent:
            return self.relations.union(self.parent.parent_relations())
        return self.relations

    def __repr__(self):
        return f"{self.name}-{','.join([rel.name for rel in self.relations])}-{','.join([child.name for child in self.children])}"

    @staticmethod
    def generate(relations: "set[Relation]", free_variables: "set[str]"):

        variables = set()
        for relation in relations:
            variables.update(relation.free_variables)
        variable_list = list(variables)

        variable_list.sort(key=lambda x: sum([1 for rel in relations if x in rel.free_variables]) + (
            0.1 if x in free_variables else 0), reverse=False)


        next_var = variable_list.pop()
        root = VariableOrderNode(next_var, set(),set(), None)
        VariableOrderNode.generate_recursion(relations, root, free_variables)
        return root

    @staticmethod
    def generate_recursion(relations: "set[Relation]", node: "VariableOrderNode", free_variables: "set[str]"):
        parent_vars = node.parent_variables()
        generateable_relations = {rel for rel in relations if rel.free_variables.issubset(parent_vars)}
        node.relations.update(generateable_relations)
        ungenerateable_relations = relations.difference(generateable_relations)
        if not ungenerateable_relations:
            return

        variables = set()
        for relation in ungenerateable_relations:
            variables.update(relation.free_variables)
        variables.difference_update(parent_vars)
        variable_list = list(variables)

        variable_list.sort(key=lambda x: sum([1 for rel in ungenerateable_relations if x in rel.free_variables]) + (0.1 if x in free_variables else 0), reverse=False)

        next_var = variable_list.pop()
        next_node = VariableOrderNode(next_var, set(), set(), node)
        node.children.add(next_node)

        sub_relations = {rel for rel in ungenerateable_relations if next_var in rel.free_variables}

        VariableOrderNode.generate_recursion(sub_relations, next_node, free_variables)
        VariableOrderNode.generate_recursion(ungenerateable_relations.difference(sub_relations), node, free_variables)

    def find_view(self, pattern: RelationPattern, bitset: "BitSet", query: "Query"):
        relevant_relations = 0
        for child_rel in self.all_relations(True):
            relevant_relations += 2 ** child_rel.index
        if relevant_relations | pattern.required == relevant_relations:
            for child in self.children:
                child_res =child.find_view(pattern, bitset, query)
                if child_res:
                    return child_res
            found_bs = 0
            found = []
            for child in self.children:
                child_relations_bs = 0
                for rel in  child.all_relations(True):
                    child_relations_bs += 2 ** rel.index
                if child_relations_bs | pattern.maximal == pattern.maximal:
                    found_bs += child_relations_bs
                    found.extend(child.all_relations())
            for rel in self.relations:
                if 2**rel.index | pattern.maximal == pattern.maximal:
                    found_bs += 2**rel.index
                    found.append(rel)
            if found_bs | pattern.required == found_bs and (found_bs & pattern.optional > 0 or pattern.optional == 0):
                variables = set()
                relations_names = ""
                for rel in found:
                    variables.update(rel.free_variables)
                    relations_names += rel.name
                return Relation(f"V_{query.name}-{relations_names}", variables, found)
            return None
        return None


