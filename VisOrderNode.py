from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from JoinOrderNode import JoinOrderNode
    from Relation import Relation
    from graphviz import Digraph
    from Query import Query

class VisOrderNode:
    def __init__(self,
                 designation: str,
                 children: "list[VisOrderNode]",
                 relations: "list[Relation]",
                 parent: "VisOrderNode|None",
                 free_variables: "list[str]",
                 aggregated_variables: "list[str]",
                 lifted_variables: "list[str]",
                 child_rel_names: str,
                 query_name: str
                 ):
        self.designation = designation
        self.children: "list[VisOrderNode]" = children
        self.relations: "list[Relation]" = relations
        self.parent: "VisOrderNode|None" = parent
        self.free_variables: "list[str]" = free_variables
        self.aggregated_variables: "list[str]" = aggregated_variables
        self.lifted_variables: "list[str]" = lifted_variables
        self.child_rel_names: str = child_rel_names
        self.query_name: str = query_name

    @staticmethod
    def generate(node: "JoinOrderNode"):
        if len(node.children) + len(node.relations) > 1:
            current_h = VisOrderNode(
                designation="H",
                children=[],
                relations=[],
                parent=None,
                free_variables=list(node.free_variables.union(node.aggregated_variables)),
                aggregated_variables=[],
                lifted_variables=[],
                child_rel_names=node.child_rel_names,
                query_name=node.query_name)
            current = VisOrderNode(
                designation="V",
                children=[current_h],
                relations=list(node.relations),
                parent=None,
                free_variables=list(node.free_variables),
                aggregated_variables=list(node.aggregated_variables),
                lifted_variables=list(node.lifted_variables),
                child_rel_names=node.child_rel_names,
                query_name=node.query_name
            )
            for child in node.children:
                vis_child = VisOrderNode.generate(child)
                vis_child.parent = current
                current_h.children.append(vis_child)
            return current
        else:
            current = VisOrderNode(
                designation="V",
                children=[],
                relations=list(node.relations), parent=None,
                free_variables=list(node.free_variables),
                aggregated_variables=list(node.aggregated_variables),
                lifted_variables=list(node.lifted_variables),
                child_rel_names=node.child_rel_names,
                query_name=node.query_name
            )
        for child in node.children:
            vis_child = VisOrderNode.generate(child)
            vis_child.parent = current
            current.children.append(vis_child)
        return current

    def graph_viz_name(self):
        if self.aggregated_variables:
            return f"<{self.designation}<SUB>{self.child_rel_names}</SUB><SUP>@{''.join(sorted(self.aggregated_variables))}</SUP>({','.join(sorted(self.free_variables))})>"

        return f"<{self.designation}<SUB>{self.child_rel_names}</SUB>({','.join(sorted(self.free_variables))})>"

    def __repr__(self):
        if self.aggregated_variables:
            return f"{self.query_name}-{self.designation}_{self.child_rel_names}@{''.join(self.aggregated_variables)}({','.join(self.free_variables)})"
        return f"{self.query_name}-{self.designation}_{self.child_rel_names}({','.join(self.free_variables)})"

    def viz(self, graph: "Digraph", query: "Query", roots: "dict[Query, VisOrderNode]"):
        graph.node(str(self), label=self.graph_viz_name(), shape="none")
        for child in self.children:
            child.viz(graph, query, roots)
            # edge without arrow head between self and child
            graph.edge(str(self), str(child), dir="none")
        for relation in self.relations:
            rel_name = f"{query.name}_{relation.name}"
            graph.node(rel_name, label=str(relation), shape="none")
            graph.edge(str(self), rel_name, dir="none")
            if relation.source_query:
                root_node_name = str(roots[relation.source_query])
                graph.edge(rel_name, root_node_name, style="dashed", dir="none")

