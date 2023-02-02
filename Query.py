from VariableOrder import VariableOrderNode
from Relation import Relation

class Query:

    def __init__(self, name: str, variable_order: "VariableOrderNode"):
        self.views: "set[Relation]" = set()
        self.name = name
        self.variable_order = variable_order

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

    def generate_views(self, variable_order_root: "VariableOrderNode"):
        all_relations = variable_order_root.all_relations()
        all_variables = set()
        for relation in all_relations:
            all_variables.update(relation.variables)
        self.views = set()
        child_partitions = []
        for relation in all_relations:
            old_child_partition = child_partitions.copy()
            for child_partition in child_partitions:
                child_partition.append(relation)
            child_partitions.extend(old_child_partition)
            child_partitions.append([relation])
        filtered_child_partitions = [partition for partition in child_partitions if len(partition) >= 2]
        for partition in filtered_child_partitions:
            if len(partition) >= 2:
                self.views.add(Relation(f"V_{self.name}", all_variables, None, all_relations))

    def __str__(self):
        return self.name + " = " + "*".join(map(lambda x: str(x), self.variable_order.all_relations()))

    def __hash__(self):
        return hash(f"{self.name}-{'/'.join(map(lambda x: str(x), self.variable_order.all_relations()))}")

    def __eq__(self, other):
        return self.name == other.name