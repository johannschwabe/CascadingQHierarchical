from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Relation import Relation
    from JoinOrderNode import JoinOrderNode


class M3Generator:
    def __init__(self, config_file_path: str, dataset: str, ring: str):
        self.ring = ring
        self.dataset = dataset
        self.vars = {}
        self.relations = []
        self.var_index = 0
        with open(config_file_path, 'r') as config:
            first_line = config.readline()
            nr_vars, nr_relations = first_line.split(' ')
            self.nr_vars = int(nr_vars)
            self.nr_relations = int(nr_relations)
            for _ in range(self.nr_vars):
                line = config.readline().split(' ')
                self.vars[line[1]] = (M3Variable(int(line[0]), line[1], line[2], set(map(lambda x: int(x), line[3].strip('{}').split(',')))))
            for _ in range(self.nr_relations):
                line = config.readline().split(' ')
                self.relations.append(M3Relation(line[0], int(line[1]), set(map(lambda x: self.vars[x], line[2].strip().split(',')))))

    def generate_maps(self, join_tree_node: "JoinOrderNode"):
        res = f'''DECLARE MAP {join_tree_node.M3ViewName(self.ring, self.vars, self.var_index)} :=\n'''
        view_names = map(lambda x: f'{x.M3ViewName(self.ring, self.vars, self.var_index)}<Local>', join_tree_node.children)
        relation_names = map(lambda x: f'{x.M3ViewName(self.ring, self.vars)}<Local>', join_tree_node.relations)
        joined_views = ' * '.join(list(view_names) + list(relation_names))
        lift = f"[lift<{self.var_index}>: {self.ring}<[{self.var_index}, {','.join(map(lambda x: self.vars[x].var_type, join_tree_node.aggregated_variables))}]>]({','.join(join_tree_node.aggregated_variables)})"
        if join_tree_node.aggregated_variables:
            res += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n (({joined_views}) * {lift})\n);\n"
        else:
            res += f"{joined_views}) * {lift});\n"
        self.var_index += len(join_tree_node.aggregated_variables)
        for child in join_tree_node.children:
            res += self.generate_maps(child)
        return res

    def generate_queries(self, join_tree_node: "JoinOrderNode"):
        res = f"DECLARE QUERY {join_tree_node.designation}_{join_tree_node.child_rel_names} := {join_tree_node.M3ViewName(self.ring, self.vars)}<Local>;\n"
        for child in join_tree_node.children:
            res += self.generate_queries(child)
        return res

    def generate_triggers(self, join_tree_node: "JoinOrderNode", operator: str):
        if join_tree_node.children:
            for child in join_tree_node.children:
                resi = self.generate_triggers(child, operator)
                for key in resi.keys():
                    if child.designation == "V":
                        resi[key] += f"{child.M3ViewName(self.ring, self.vars)}<Local> += {'-' if operator == '-' else ''}1"
                    else:
                        temp = "1"
                        for sibling in child.children:
                            if not key in sibling.all_relations():
                                temp = f"(({temp} * {sibling.M3ViewName(self.ring, self.vars)}<Local>) * Lift<{sibling.M3_index}>: {self.ring}<{sibling.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, sibling.aggregated_variables))}>]({','.join(sibling.aggregated_variables)}"
                        for relation in child.relations:
                            if relation != key:
                                temp = f"(({temp} * {sibling.M3ViewName(self.ring, self.vars)}<Local>) * Lift<{sibling.M3_index}>: {self.ring}<{sibling.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, sibling.aggregated_variables))}>]({','.join(sibling.aggregated_variables)}"

                        resi[key] += f"{child.M3ViewName(self.ring, self.vars)}<Local> += "
            return resi
        else:
            res: "dict[Relation,str]" = {}
            for rel in join_tree_node.relations:
                res[rel] = f"ON {operator} {rel} ({', '.join(rel.free_variables)}) {{ \n "
            return res
    def generate(self, join_tree_node: "JoinOrderNode"):
        res = '''---------------- TYPE DEFINITIONS ---------------
CREATE DISTRIBUTED TYPE RingFactorizedRelation
FROM FILE 'ring/ring_factorized.hpp'
WITH PARAMETER SCHEMA (dynamic_min);

-------------------- SOURCES --------------------'''
        for rel in self.relations:
            res += rel.generate_source(self.dataset)
            res += "\n"
        res += self.generate_maps(join_tree_node)
        res += self.generate_queries(join_tree_node)
        # self.generate_triggers(join_tree_node, "+")
        print(res)




class M3Variable:
    def __init__(self, _index: int, name: str, var_type: str, dependent_set: "set[int]"):
        self.index: int = _index
        self.name: str = name
        self.var_type: str = var_type
        self.dependant_set: "set[int]" = dependent_set

    def __hash__(self):
        return self.index
    def __eq__(self, other):
        return self.index == other.index

class M3Relation:
    def __init__(self, name: str, nr: int, variables: "set[M3Variable]"):
        self.name: str = name
        self.nr: int = nr
        self.variables: "set[M3Variable]" = variables

    def generate_source(self, dataset:str):
        return f"CREATE STREAM {self.name} ({','.join(map(lambda x: f'{x.name} {x.var_type}', self.variables))})\n  FROM FILE './datasets/{dataset}/{self.name.capitalize()}.tbl' LINE DELIMITED CSV (delimiter := '|');"

    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name