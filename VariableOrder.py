
from graphviz import Digraph
from ordered_set import OrderedSet

from Relation import Relation


class VariableOrderNode:
    def __init__(self, name: str, children: "set[VariableOrderNode]", relations: "OrderedSet[Relation]", parent: "VariableOrderNode|None"):
        self.children = children
        self.name = name
        self.relations:"OrderedSet[Relation]" = relations
        self.parent = parent
        self._all_relations_sources = OrderedSet()
        self._all_relations_no_sources = OrderedSet()
        self._parent_vars = OrderedSet()

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
            if relation.source_query:
                for source in relation.root_sources():
                    source_name = f"{rootname}_{source.name}"
                    graph.node(source_name, label=str(source), shape="diamond")
                    graph.edge(relation_name, source_name)
        return graph


    def all_relations(self, source_only = False) -> "OrderedSet[Relation]":
        if source_only and self._all_relations_sources:
            return self._all_relations_sources
        if not source_only and self._all_relations_no_sources:
            return self._all_relations_no_sources
        res = OrderedSet()
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

    def parent_variables(self) -> "OrderedSet[str]":
        if self._parent_vars:
            return self._parent_vars.copy()
        res = OrderedSet([self.name])
        if self.parent:
            res.update(self.parent.parent_variables())
        self._parent_vars = res
        return res

    def child_vars(self)->"OrderedSet[str]":
        res = OrderedSet([self.name])
        for child in self.children:
            res.update(child.child_vars())
        return res

    def parent_relations(self) -> "OrderedSet[Relation]":
        if self.parent:
            return self.relations.union(self.parent.parent_relations())
        return self.relations

    def __repr__(self):
        return f"{self.name}-{','.join([rel.name for rel in self.relations])}-{','.join([child.name for child in self.children])}"

    @staticmethod
    def generate(relations: "OrderedSet[Relation]", free_variables: "OrderedSet[str]"):

        variables = OrderedSet()
        for relation in relations:
            variables.update(relation.free_variables)
        variable_list = list(variables)

        variable_list.sort(key=lambda x: sum([1 for rel in relations if x in rel.free_variables]) + (
            0.1 if x in free_variables else 0), reverse=False)


        next_var = variable_list.pop()
        root = VariableOrderNode(next_var, set(),OrderedSet(), None)
        VariableOrderNode.generate_recursion(relations, root, free_variables)
        return root

    @staticmethod
    def generate_recursion(relations: "OrderedSet[Relation]", node: "VariableOrderNode", free_variables: "OrderedSet[str]"):
        parent_vars = node.parent_variables()
        generateable_relations = {rel for rel in relations if set(rel.free_variables).issubset(parent_vars)}
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
        next_node = VariableOrderNode(next_var, set(), OrderedSet(), node)
        node.children.add(next_node)

        sub_relations = OrderedSet([rel for rel in ungenerateable_relations if next_var in rel.free_variables])

        VariableOrderNode.generate_recursion(sub_relations, next_node, free_variables)
        VariableOrderNode.generate_recursion(ungenerateable_relations.difference(sub_relations), node, free_variables)

