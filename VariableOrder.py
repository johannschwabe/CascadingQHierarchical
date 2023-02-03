from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Relation import Relation


class VariableOrderNode:
    def __init__(self, name: str, children: "set[VariableOrderNode]", relations: "set[Relation]", parent: "VariableOrderNode|None"):
        self.children = children
        self.name = name
        self.relations = relations
        self.parent = parent

    def all_relations(self, source_only = False):
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

    def parentVariables(self):
        res = {self.name}
        if self.parent:
            res.update(self.parent.parentVariables())
        return res

    @staticmethod
    def generate(relations: "set[Relation]"):
        variables = set()
        for relation in relations:
            variables.update(relation.variables)
        variable_list = list(variables)
        variable_list.sort(key=lambda x: sum([1 for rel in relations if x in rel.variables]), reverse=False)
        next_var = variable_list.pop()
        root = VariableOrderNode(next_var, set(),set(), None)
        VariableOrderNode.generate_recursion(relations, root)
        return root

    @staticmethod
    def generate_recursion(relations: "set[Relation]", node: "VariableOrderNode"):
        parent_vars = node.parentVariables()
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
        variable_list.sort(key=lambda x: sum([1 for rel in ungenerateable_relations if x in rel.variables]), reverse=False)

        next_var = variable_list.pop()
        next_node = VariableOrderNode(next_var, set(), set(), node)
        node.children.add(next_node)

        sub_relations = {rel for rel in ungenerateable_relations if next_var in rel.variables}

        VariableOrderNode.generate_recursion(sub_relations, next_node)
        VariableOrderNode.generate_recursion(ungenerateable_relations.difference(sub_relations), node)
