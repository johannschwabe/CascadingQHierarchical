from typing import TYPE_CHECKING

from JoinOrderNode import JoinOrderNode

if TYPE_CHECKING:
    from Query import Query
    from Relation import Relation


class M3Generator:
    def __init__(self, config_file_path: str, dataset: str, ring: str, query: "Query"):
        self.ring = ring
        self.dataset = dataset
        self.query = query
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

    def assign_index(self, join_tree_node: "JoinOrderNode"):
        join_tree_node.M3_index = self.var_index
        lifted_variables = join_tree_node.aggregated_variables.intersection(self.query.free_variables)
        self.var_index += len(lifted_variables)
        for child in join_tree_node.children:
            self.assign_index(child)

    def generate_maps(self, join_tree_node: "JoinOrderNode"):
        lifted_variables = join_tree_node.aggregated_variables.intersection(self.query.free_variables)
        res = f'''\nDECLARE MAP {join_tree_node.M3ViewName(self.ring, self.vars, declaration=True)} :=\n'''
        view_names = map(lambda x: f'{x.M3ViewName(self.ring, self.vars)}<Local>', join_tree_node.children)
        relation_names = map(lambda x: x.M3ViewName(), join_tree_node.relations)
        joined_views = ' * '.join(list(view_names) + list(relation_names))
        if join_tree_node.aggregated_variables:
            if lifted_variables:
                lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, lifted_variables))}]>]({','.join(lifted_variables)})"
                res += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n (({joined_views}) * {lift})\n);\n"
            else:
                res += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n ({joined_views})\n);\n"
        else:
            res += f"{joined_views};\n"
        for child in join_tree_node.children:
            res += self.generate_maps(child)
        return res

    def generate_tmp_maps(self, join_tree_node: "JoinOrderNode"):
        lifted_variables = join_tree_node.aggregated_variables.intersection(self.query.free_variables)
        res = ""
        for child in join_tree_node.children:
            view_names = map(lambda x: f'{x.M3ViewName(self.ring, self.vars)}<Local>', join_tree_node.children.difference({child}))
            relation_names = map(lambda x: x.M3ViewName(), join_tree_node.relations)
            joined_views = f"(DELTA TMP_{child.child_rel_names})({','.join(child.free_variables)}) * {' * '.join(list(view_names) + list(relation_names))}"

            _map = f"DECLARE MAP TMP_{child.child_rel_names}_{join_tree_node.M3ViewName(self.ring, self.vars, declaration=True)} :=\n"
            if join_tree_node.aggregated_variables:
                if lifted_variables:
                    lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, lifted_variables))}]>]({','.join(lifted_variables)})"
                    _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n (({joined_views}) * {lift})\n);\n"
                else:
                    _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n ({joined_views})\n);\n"
            else:
                _map += f"{joined_views};\n"
            res += _map
            res += self.generate_tmp_maps(child)
        for relation in join_tree_node.relations:
            view_names = map(lambda x: f'{x.M3ViewName(self.ring, self.vars)}<Local>', join_tree_node.children)
            relation_names = map(lambda x: x.M3ViewName(), join_tree_node.relations.difference({relation}))
            joined_views = ' * '.join([f"(DELTA {relation.name})({','.join(relation.free_variables)})"] + list(view_names) + list(relation_names))

            _map = f"DECLARE MAP TMP_{relation.name}_{join_tree_node.M3ViewName(self.ring, self.vars, declaration=True)} :=\n"
            if join_tree_node.aggregated_variables:
                if lifted_variables:
                    lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, lifted_variables))}]>]({','.join(lifted_variables)})"
                    _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n (({joined_views}) * {lift})\n);\n"
                else:
                    _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n ({joined_views})\n);\n"
                res += _map
        return res
    def generate_queries(self, join_tree_node: "JoinOrderNode"):
        res = f"DECLARE QUERY {join_tree_node.designation}_{join_tree_node.child_rel_names} := {join_tree_node.M3ViewName(self.ring, self.vars)}<Local>;\n"
        for child in join_tree_node.children:
            res += self.generate_queries(child)
        return res
    def generate_triggers(self, join_tree_node: "JoinOrderNode"):
        top = JoinOrderNode(None, "", set(), set(), set(), "H")
        top.children = {join_tree_node}
        res = ""
        removals = self.generate_triggers_recursive(top, "+")
        for rel, value in removals.items():
            res += f"ON + {rel.name} ({', '.join(rel.free_variables)}) {{ \n "
            for update in value:
                res += f"{update};\n"
            res += "}\n"

        removals = self.generate_triggers_recursive(join_tree_node, "-")
        for rel, value in removals.items():
            res += f"ON - {rel.name} ({', '.join(rel.free_variables)}) {{ \n "
            for update in value:
                res += f"{update};\n"
            res += "}\n"
        return res

    def generate_triggers_recursive(self, join_tree_node: "JoinOrderNode", operator: str)->"dict[Relation,list[str]]":
        res = {}
        if join_tree_node.children:
            for child in join_tree_node.children:
                resi = self.generate_triggers_recursive(child, operator)
                for key in resi.keys():
                    lift = f"[lift<{child.M3_index}>: {self.ring}<[{child.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, child.lifted_variables))}]>]({','.join(child.lifted_variables)})"
                    target = f"{child.M3ViewName(self.ring, self.vars)}<Local> += "
                    if len(resi[key]) == 0:
                        resi[key].append(target)
                        if child.lifted_variables:
                            product = f"({'-' if operator == '-' else ''}1 * {lift})"
                        else:
                            product = f"{'-' if operator == '-' else ''}1"
                        resi[key][-1] += product
                    else:
                        product = f"({resi[key][-1].split('=')[1]})"
                        for sibling in child.children:
                            if not key in sibling.all_relations():
                                product = f"({product} * {sibling.M3ViewName(self.ring, self.vars)}<Local>)"
                        resi[key].append(f"{target} {product} * {lift}")


                res.update(resi)
        else:
            resi: "dict[Relation,list[str]]" = {}
            for rel in join_tree_node.relations:
                resi[rel] = []
                # res[rel] = f"ON {operator} {rel} ({', '.join(rel.free_variables)}) {{ \n "
            res.update(resi)

        return res
    def generate(self, join_tree_node: "JoinOrderNode"):
        self.assign_index(join_tree_node)
        res = '''---------------- TYPE DEFINITIONS ---------------
CREATE DISTRIBUTED TYPE RingFactorizedRelation
FROM FILE 'ring/ring_factorized.hpp'
WITH PARAMETER SCHEMA (dynamic_min);

-------------------- SOURCES --------------------
'''
        for rel in self.relations:
            res += rel.generate_source(self.dataset)
            res += "\n"
        res += '''\n-------------------- MAPS --------------------\n'''
        res += self.generate_maps(join_tree_node)
        print(self.generate_tmp_maps(join_tree_node))
        res += '''\n-------------------- QUERIES --------------------\n'''
        res += self.generate_queries(join_tree_node)
        res += '''\n-------------------- TRIGGERS --------------------\n'''
        res += self.generate_triggers(join_tree_node)
        with open("output.m3", "w") as f:
            f.write(res)
        # print(res)




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