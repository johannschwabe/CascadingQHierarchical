import itertools
from typing import TYPE_CHECKING

from graphviz import Graph, Digraph

from Relation import Relation


if TYPE_CHECKING:
    from Query import Query


class VariableOrderNode:
    def __init__(self, name: str, children: "set[VariableOrderNode]", relations: "set[Relation]", parent: "VariableOrderNode|None"):
        self.children = children
        self.name = name
        self.relations = relations
        self.parent = parent

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
            if relation.dependentOn:
                for source in relation.root_sources():
                    source_name = f"{rootname}_{source.name}"
                    graph.node(source_name, label=str(source), shape="diamond")
                    graph.edge(relation_name, source_name)
        return graph

    def all_relations(self, source_only = False) -> "set[Relation]":
        res = set()
        if source_only:
            for rel in self.relations:
                res.update(rel.root_sources())
        else:
            res.update(self.relations)
        for child in self.children:
            res.update(child.all_relations(source_only))
        return res

    def copy(self, parent: "VariableOrderNode|None"):
        children = set(map(lambda x: x.copy(self), self.children))
        return VariableOrderNode(self.name, children, self.relations.copy(), parent)

    def parent_variables(self):
        res = {self.name}
        if self.parent:
            res.update(self.parent.parent_variables())
        return res

    def parent_relations(self):
        if self.parent:
            return self.relations.union(self.parent.parent_relations())
        return self.relations

    def generate_views(self, query: "Query"):
        res = set()
        branches = self.generate_views_recurse(query)
        for branch in branches:
            for i in range(0, len(branch[0])+1):
                for combination in itertools.combinations(branch[0], i):
                    variables = set()
                    relations = set(combination).union(branch[1])
                    if len(relations) < 2:
                        continue
                    for rel in relations:
                        variables.update(rel.variables)
                    res.add(Relation(f"V_{query.name}-{len(res)}", variables, query, relations))
        return res
    def generate_views_recurse(self, query: "Query"):
        res = []
        parent_relations = self.parent_relations()

        if len(self.children) == 0:
            return [(parent_relations, set())]
        if len(self.children) > 1:
            complete_sub_relations = self.all_relations(False).difference(self.relations)
            res.append((parent_relations.union(self.relations), complete_sub_relations))
        for child in self.children:
            res.extend(child.generate_views_recurse(query))
        return res


    @staticmethod
    def generate(relations: "set[Relation]", free_variables: "set[str]"):

        variables = set()
        for relation in relations:
            variables.update(relation.variables)
        variable_list = list(variables)

        variable_list.sort(key=lambda x: sum([1 for rel in relations if x in rel.variables]) + (
            0.1 if x in free_variables else 0), reverse=False)


        next_var = variable_list.pop()
        root = VariableOrderNode(next_var, set(),set(), None)
        VariableOrderNode.generate_recursion(relations, root, free_variables)
        return root

    @staticmethod
    def generate_recursion(relations: "set[Relation]", node: "VariableOrderNode", free_variables: "set[str]"):
        parent_vars = node.parent_variables()
        generateable_relations = {rel for rel in relations if rel.variables.issubset(parent_vars)}
        node.relations.update(generateable_relations)
        ungenerateable_relations = relations.difference(generateable_relations)
        if not ungenerateable_relations:
            return

        variables = set()
        for relation in ungenerateable_relations:
            variables.update(relation.variables)
        variables.difference_update(parent_vars)
        variable_list = list(variables)

        variable_list.sort(key=lambda x: sum([1 for rel in ungenerateable_relations if x in rel.variables]) + (0.1 if x in free_variables else 0), reverse=False)

        next_var = variable_list.pop()
        next_node = VariableOrderNode(next_var, set(), set(), node)
        node.children.add(next_node)

        sub_relations = {rel for rel in ungenerateable_relations if next_var in rel.variables}

        VariableOrderNode.generate_recursion(sub_relations, next_node, free_variables)
        VariableOrderNode.generate_recursion(ungenerateable_relations.difference(sub_relations), node, free_variables)
