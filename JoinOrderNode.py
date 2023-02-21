from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from VariableOrder import VariableOrderNode
    from graphviz import Digraph
    from Query import Query
    from Relation import Relation


class JoinOrderNode:
    def __init__(self):
        self.name: str = ""
        self.children: "set[JoinOrderNode]" = set()
        self.relations: "set[Relation]" = set()
        self.parent: "JoinOrderNode|None" = None
        self.free_variables: "set[str]" = set()
        self.aggregated_variables: "set[str]" = set()
        self._all_relations_sources: "set[Relation]" = set()
        self._all_relations_no_sources: "set[Relation]" = set()

    def graph_viz(self, graph: "Digraph", query: "Query"):
        pass

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

    def copy(self, parent: "JoinOrderNode|None"):
        children = set(map(lambda x: x.copy(self), self.children))
        return JoinOrderNode() # Todo

    @staticmethod
    def generate(variable_order_node: "VariableOrderNode", query: "Query"):
        node = JoinOrderNode()
        child_relations = variable_order_node.all_relations(source_only=True)
        child_relation_names = "".join(sorted(map(lambda x: x.name, child_relations)))
        parent_vars = variable_order_node.parent_variables().union(query.free_variables)
        if len(variable_order_node.children) + len(variable_order_node.relations) > 1:
            node.relations = variable_order_node.relations
            if variable_order_node.name in query.free_variables:
                node.name = f"<V<SUB>{child_relation_names}</SUB>({','.join(parent_vars)})>"
            else:
                node.name = f"<V<SUB>{child_relation_names}</SUB><SUP>@{variable_order_node.name}</SUP>({','.join(parent_vars.difference({variable_order_node.name}))})>"
            child_nodes = []
            for child in variable_order_node.children:
                child_node = JoinOrderNode.generate(child, query)
                child_nodes.append(child_node)
            node.children = child_nodes

            return node
        elif len(variable_order_node.children) == 0:
            node.relations = variable_order_node.relations
            node.name = f"<V<SUB>{child_relation_names}</SUB><SUP>@{variable_order_node.name}</SUP>({','.join(parent_vars.difference({variable_order_node.name}))})>"
            return node

        _iter = variable_order_node
        bounded_vars = []
        if _iter.name not in query.free_variables:
            bounded_vars.append(_iter.name)
        while len(_iter.children) == 1 and len(_iter.relations) == 0:
            _iter = list(_iter.children)[0]
            if _iter.name not in query.free_variables:
                bounded_vars.append(_iter.name)

        node.name = f"<V<SUB>{child_relation_names}</SUB><SUP>@{''.join(bounded_vars)}</SUP>({','.join(parent_vars.difference(bounded_vars))})>"
        node.children = []
        for child in _iter.children:
            sub = JoinOrderNode.generate(child, query)
            node.children.append(sub)
        node.relations = _iter.relations
        return node

    def viz(self, graph: "Digraph"):
        graph.node(self.name, label=self.name)
        for child in self.children:
            child.viz(graph)
            graph.edge(self.name, child.name)
        for relation in self.relations:
            graph.node(str(relation), shape="rectangle")
            graph.edge(self.name, str(relation))

