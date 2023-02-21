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
        self._all_relations_sources = set()
        self._all_relations_no_sources = set()

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
        res = {self.name}
        if self.parent:
            res.update(self.parent.parent_variables())
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

    def generate_views(self, query: "Query"):
        if len(query.free_variables) == 0:
            return []
        _, views = self.generate_views_recurse(query)
        views = sorted(list(views), key=lambda x: len(x.sources), reverse=True)
        for i, view in enumerate(views):
            view.set_name(f"V_{query.name}_{i}")
        return views

    def generate_views_recurse(self, query: "Query"):
        sub_rel = []
        views = set()
        if len(self.children) + len(self.relations) > 1:
            all_child_relations = []
            for child in self.children:
                child_relations, child_views = child.generate_views_recurse(query)
                views.update(child_views)
                all_child_relations.append(child_relations)
                sub_rel.extend(child_relations)
            all_child_relations.extend(self.relations)
            sub_rel.extend(self.relations)
            for i in range(1, len(all_child_relations) + 1):
                for combination in itertools.combinations(all_child_relations, i):
                    rel_views = set()
                    for selection in combination:
                        if type(selection) == Relation:
                            rel_views.add(selection)
                        else:
                            rel_views.update(selection)
                    if len(rel_views) < 2:
                        continue
                    variables = set()
                    for rel in rel_views:
                        variables.update(rel.free_variables)
                    views.add(Relation(f"V_{query.name}_{len(query.views)}", variables.intersection(query.free_variables), query, rel_views))
        else:
            for child in self.children:
                child_relations, child_views = child.generate_views_recurse(query)
                sub_rel.extend(child_relations)
                views.update(child_views)
            sub_rel.extend(self.relations)
        return sub_rel, views

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
