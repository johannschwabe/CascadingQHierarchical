from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from VariableOrder import VariableOrderNode
    from graphviz import Digraph
    from Query import Query
    from Relation import Relation


class JoinOrderNode:
    def __init__(self, query_name: str,
                 child_rel_names: str,
                 relations: "set[Relation]",
                 free_vars: "set[str]",
                 aggregated_vars: "set[str]"
                 ):
        self.query_name: str = query_name
        self.child_rel_names: str = child_rel_names
        self.children: "set[JoinOrderNode]" = set()
        self.relations: "set[Relation]" = relations
        self.parent: "JoinOrderNode|None" = None
        self.free_variables: "set[str]" = free_vars
        self.aggregated_variables: "set[str]" = aggregated_vars
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

    def graph_viz_name(self):
        if self.aggregated_variables:
            return f"<V<SUB>{self.child_rel_names}</SUB><SUP>@{''.join(sorted(self.aggregated_variables))}</SUP>({','.join(sorted(self.free_variables))})>"

        return f"<V<SUB>{self.child_rel_names}</SUB>({','.join(sorted(self.free_variables))})>"

    def __repr__(self):
        if self.aggregated_variables:
            return f"{self.query_name}-V_{self.child_rel_names}@{''.join(self.aggregated_variables)}({','.join(self.free_variables)})"
        return f"{self.query_name}-V_{self.child_rel_names}({','.join(self.free_variables)})"

    @staticmethod
    def generate(variable_order_node: "VariableOrderNode", query: "Query"):
        child_relations = variable_order_node.all_relations(source_only=True)
        child_relation_names = "".join(sorted(map(lambda x: x.name, child_relations)))
        parent_vars = variable_order_node.parent_variables()
        if len(variable_order_node.children) + len(variable_order_node.relations) > 1:
            free_vars = parent_vars.difference({variable_order_node.name})
            aggregated_vars = {variable_order_node.name}
            node = JoinOrderNode(query_name=query.name,
                                 child_rel_names=child_relation_names,
                                 relations=variable_order_node.relations,
                                 free_vars=free_vars,
                                 aggregated_vars=aggregated_vars)
            child_nodes = []
            for child in variable_order_node.children:
                child_node = JoinOrderNode.generate(child, query)
                child_node.parent = node
                child_nodes.append(child_node)
            node.children = child_nodes


            return node
        elif len(variable_order_node.children) == 0:
            aggregated_vars = {variable_order_node.name}

            node = JoinOrderNode(query_name=query.name,
                                 child_rel_names=child_relation_names,
                                 relations=variable_order_node.relations,
                                 free_vars=parent_vars.difference(aggregated_vars),
                                 aggregated_vars=aggregated_vars)
            return node

        _iter = variable_order_node
        simple_vars = {_iter.name}
        while len(_iter.children) == 1 and len(_iter.relations) == 0:
            _iter = list(_iter.children)[0]
            simple_vars.add(_iter.name)
        if len(_iter.children) + len(_iter.relations) > 1:
            free_vars = simple_vars.intersection(query.free_variables)
            bound_vars = simple_vars.difference(query.free_variables)
        else:
            bound_vars = simple_vars
            free_vars = parent_vars.difference(bound_vars)


        node = JoinOrderNode(query_name=query.name,
                             child_rel_names=child_relation_names,
                             relations=_iter.relations,
                             free_vars=free_vars,
                             aggregated_vars=bound_vars)
        for child in _iter.children:
            sub = JoinOrderNode.generate(child, query)
            sub.parent = node
            node.children.add(sub)
        return node

    def viz(self, graph: "Digraph", query: "Query"):
        graph.node(str(self), label=self.graph_viz_name())
        for child in self.children:
            child.viz(graph, query)
            graph.edge(str(self), str(child))
        for relation in self.relations:
            rel_name = f"{query.name}_{relation.name}"
            graph.node(rel_name, label=str(relation), shape="rectangle")
            graph.edge(str(self), rel_name)
            if relation.sources:
                for source in relation.root_sources():
                    source_name = f"{query.name}_{source.name}"
                    graph.node(source_name, label=str(source), shape="diamond")
                    graph.edge(rel_name, source_name)

