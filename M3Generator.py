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
        child_names, res = self.generate_tmp_maps_recursive(join_tree_node)
        return res

    def generate_tmp_maps_recursive(self, join_tree_node: "JoinOrderNode"):
        lifted_variables = join_tree_node.aggregated_variables.intersection(self.query.free_variables)
        res = ""
        new_child_names = []
        for child in join_tree_node.children:
            child_names, resi = self.generate_tmp_maps_recursive(child)
            res += resi
            view_names = list(map(lambda x: f'{x.M3ViewName(self.ring, self.vars)}<Local>', join_tree_node.children.difference({child})))
            relation_names = list(map(lambda x: x.M3ViewName(), join_tree_node.relations))
            for child_name in child_names:
                joined_views = f"{child_name}<Local> * {' * '.join(view_names + relation_names)}"
                prefix = f"TMP_{child_name[4:].split('_')[0]}_"
                new_child_name = f"{prefix}{join_tree_node.M3ViewName(self.ring, self.vars, declaration=False)}"
                _map = f"DECLARE MAP {prefix}{join_tree_node.M3ViewName(self.ring, self.vars, declaration=True)} :=\n"
                new_child_names.append(new_child_name)
                if join_tree_node.aggregated_variables:
                    if lifted_variables:
                        lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, lifted_variables))}]>]({','.join(lifted_variables)})"
                        _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n (({joined_views}) * {lift})\n);\n"
                    else:
                        _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n ({joined_views})\n);\n"
                else:
                    _map += f"{joined_views};\n"
                res += _map

        for relation in join_tree_node.relations:
            view_names = list(map(lambda x: f'{x.M3ViewName(self.ring, self.vars)}<Local>', join_tree_node.children))
            relation_names = list(map(lambda x: x.M3ViewName(), join_tree_node.relations.difference({relation})))
            joined_views = ' * '.join([f"(DELTA {relation.name})({','.join(relation.free_variables)})"] + view_names + relation_names)
            new_child_name = f"TMP_{relation.name}_{join_tree_node.M3ViewName(self.ring, self.vars, declaration=False)}"
            new_child_names.append(new_child_name)
            _map = f"DECLARE MAP TMP_{relation.name}_{join_tree_node.M3ViewName(self.ring, self.vars, declaration=True)} :=\n"
            if join_tree_node.aggregated_variables:
                if lifted_variables:
                    lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, lifted_variables))}]>]({','.join(lifted_variables)})"
                    _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n (({joined_views}) * {lift})\n);\n"
                else:
                    _map += f"AggSum([{', '.join(join_tree_node.free_variables)}],\n ({joined_views})\n);\n"
            else:
                _map += f"{joined_views};\n"
            res += _map
        return new_child_names, res
    def generate_queries(self, join_tree_node: "JoinOrderNode"):
        res = f"DECLARE QUERY {join_tree_node.designation}_{join_tree_node.child_rel_names} := {join_tree_node.M3ViewName(self.ring, self.vars)}<Local>;\n"
        for child in join_tree_node.children:
            res += self.generate_queries(child)
        return res

    def generate_triggers_batch(self, join_tree_node: "JoinOrderNode"):
        res = ""
        names, additions = self.generate_triggers_batch_recursive(join_tree_node)
        for rel, value in additions.items():
            res += f"ON BATCH UPDATE OF {rel.name} {{ \n "
            for path in value['path']:
                res += f"{path}\n"
            for update in value['update']:
                res += f"{update}\n"
            res += "}\n"

        return res
    def generate_triggers_batch_recursive(self, join_tree_node: "JoinOrderNode"):
        res = {}
        new_child_names = {}

        if join_tree_node.children:
            join_tree_node_name = f"{join_tree_node.M3ViewName(self.ring, self.vars)}<Local>"
            for child in join_tree_node.children:
                child_names, child_res = self.generate_triggers_batch_recursive(child)
                res.update(child_res)
                for rel in child_res.keys():
                    tmp_child_name = child_names[rel]
                    lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, join_tree_node.lifted_variables))}]>]({','.join(join_tree_node.lifted_variables)})"
                    prefix = f"TMP_{rel.name}_"
                    tmp_join_tree_w_rel = f"{prefix}{join_tree_node.M3ViewName(self.ring, self.vars, declaration=False)}"
                    new_child_names[rel] = tmp_join_tree_w_rel
                    siblings = '*'.join(map(lambda x: f"{x.M3ViewName(self.ring, self.vars)}<Local>", join_tree_node.children.difference({child})))

                    if join_tree_node.lifted_variables:
                        product = f"({tmp_child_name} * {siblings}) * {lift}"
                    else:
                        product = f"{tmp_child_name} * {siblings}"
                    if join_tree_node.aggregated_variables:
                        product = f"AggSum([{', '.join(join_tree_node.free_variables)}], {product})"

                    path = f"{tmp_join_tree_w_rel}<Local> += {product};"

                    update = f"{join_tree_node_name} += {tmp_join_tree_w_rel};"
                    if rel in res:
                        res[rel]["path"].append(path)
                        res[rel]["update"].append(update)
                    else:
                        res[rel] = {"path": [path], "update": [update]}
                    print(update)

        else:
            for rel in join_tree_node.relations:
                lift = f"[lift<{join_tree_node.M3_index}>: {self.ring}<[{join_tree_node.M3_index}, {','.join(map(lambda x: self.vars[x].var_type, join_tree_node.lifted_variables))}]>]({','.join(join_tree_node.lifted_variables)})"
                tmp = f"TMP_{rel.name}_{join_tree_node.M3ViewName(self.ring, self.vars)}"
                new_child_names[rel] = tmp
                if join_tree_node.lifted_variables:
                    product = f"((DELTA {rel.name})({', '.join(rel.free_variables)}) * {lift})"
                else:
                    product = f"(DELTA {rel.name})({', '.join(rel.free_variables)})"
                if join_tree_node.aggregated_variables:
                    product = f"AggSum([{', '.join(join_tree_node.free_variables)}], {product})"
                path = f"{tmp}<Local> += {product};"

                update = f"{join_tree_node.M3ViewName(self.ring, self.vars)}<Local> += {tmp};"
                res[rel] = {"path": [path], "update": [update]}
        return new_child_names, res
    def generate_triggers(self, join_tree_node: "JoinOrderNode"):
        top = JoinOrderNode(None, "", set(), set(), set(), "H")
        top.children = {join_tree_node}
        res = ""
        additions = self.generate_triggers_recursive(top, "+")
        for rel, value in additions.items():
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
    def generate(self, join_tree_node: "JoinOrderNode", batch: bool):
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
        if batch:
            res += self.generate_tmp_maps(join_tree_node)
        res += '''\n-------------------- QUERIES --------------------\n'''
        res += self.generate_queries(join_tree_node)
        res += '''\n-------------------- TRIGGERS --------------------\n'''
        if batch:
            res += self.generate_triggers_batch(join_tree_node)
        else:
            res += self.generate_triggers(join_tree_node)

        res += '''
ON SYSTEM READY {
  
}'''
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