from VariableOrder import VariableOrderNode
from Relation import Relation

class Query:

    def __init__(self, name: str, relations: "set[Relation]", free_variables: "set[str]"):
        self.views: "set[Relation]" = set()
        self.name = name
        self.free_variables = free_variables
        self.variable_order = VariableOrderNode.generate(relations, free_variables)


    def is_q_hierarchical(self) -> bool:
        variables = set()
        all_relations = self.variable_order.all_relations()
        for rel in all_relations:
            variables = variables.union(rel.variables)
        for variable_a in variables:
            for variable_b in variables:
                if variable_a == variable_b:
                    continue
                atoms_a = set(filter(lambda x: variable_a in x.variables, all_relations))
                atoms_b = set(filter(lambda x: variable_b in x.variables, all_relations))
                c1 = atoms_a.issubset(atoms_b)
                c2 = atoms_b.issubset(atoms_a)
                c3 = atoms_a.isdisjoint(atoms_b)
                if not (c1 or c2 or c3):
                    return False
        return True

    def generate_views(self):
        self.views = self.variable_order.generate_views(self)

    def dependant_on(self):
        res: "set[Query]" = set()
        for relation in self.variable_order.all_relations(False):
            if relation.dependentOn:
                res.add(relation.dependentOn)
                res.update(relation.dependentOn.dependant_on())
        return res

    def __str__(self):
        return self.name + " = " + "*".join(map(lambda x: str(x), self.variable_order.all_relations()))

    def __hash__(self):
        return hash(f"{self.name}-{'/'.join(sorted(map(lambda x: str(x), self.variable_order.all_relations())))}")

    def __eq__(self, other):
        return hash(self) == hash(other)

class QuerySet:
    def __init__(self):
        self.queries: "set[Query]" = set()

    def __hash__(self):
        return hash(",".join(sorted(map(lambda x: str(hash(x)), self.queries))))

    def __repr__(self):
        return ",".join(sorted(map(lambda x: str(x), self.queries)))

    def add(self, other: "Query"):
        self.queries.add(other)

    def __eq__(self, other):
        return hash(self) == hash(other)