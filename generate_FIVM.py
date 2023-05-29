from typing import List

class Relation:
    def __init__(self, name: str, variables: dict[str, str], private_keys: set[str]):
        self.name: str = name
        self.variables: dict[str, str] = variables
        self.private_keys: set[str] = private_keys
        self.last_variable: "VariableOrderNode | None" = None

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class VariableOrderNode:
    def __init__(self, name: str, data_type:str = "int"):
        self.name: str = name
        self.children: "List[VariableOrderNode]" = []
        self.parent: "VariableOrderNode | None" = None
        self.id = -1
        self.data_type = data_type


    def add_child(self, child: "VariableOrderNode"):
        self.children.append(child)
        child.parent = self

    def child_variables(self):
        res: set[str] = set()
        for child in self.children:
            res.update(child.child_variables())
            res.add(child.name)
        return res

    def parent_variables(self):
        if self.parent is None:
            return set()
        return self.parent.parent_variables().union({self.parent.name})

    def parent_ids(self):
        if self.parent is None:
            return set()
        return self.parent.parent_ids().union({self.parent.id})

    def set_id(self, _id):
        self.id = _id
        next_id = _id + 1
        for child in self.children:
            next_id = child.set_id(next_id)
        return next_id

    def generate_config(self):
        res = f"{self.id} {self.name} {self.data_type} {self.parent.id if self.parent is not None else -1} {{{','.join([str(x) for x in self.parent_ids()])}}} 0\n"
        for child in self.children:
            res += child.generate_config()
        return res

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

Inventory = Relation("INVENTORY", {"locn": "int", "dateid": "int", "ksn": "int", "inventoryunits": "int"}, {"locn", "dateid", "ksn"})
Location = Relation("LOCATION",
                    {"locn": "int", "zip": "int", "rgn_cd": "int", "clim_zn_nbr": "int", "tot_area_sq_ft": "int",
                     "sell_area_sq_ft": "int", "avghhi": "int", "supertargetdistance": "double",
                     "supertargetdrivetime": "double", "targetdistance": "double", "targetdrivetime": "double",
                     "walmartdistance": "double", "walmartdrivetime": "double",
                     "walmartsupercenterdistance": "double", "walmartsupercenterdrivetime": "double"}, {"locn"})
Census = Relation("CENSUS", {"zip": "int", "population": "int", "white": "int", "asian": "int", "pacific": "int",
                             "blackafrican": "int", "medianage": "double", "occupiedhouseunits": "int",
                             "houseunits": "int", "families": "int", "households": "int", "husbwife": "int",
                             "males": "int", "females": "int", "householdschildren": "int", "hispanic": "int"},{"zip"})
Item = Relation("ITEM", {"ksn": "int", "subcategory": "int", "category": "int", "categoryCluster": "int",
                         "prize": "double"},{"ksn"})
Weather = Relation("WEATHER", {"locn": "int", "dateid": "int", "rain": "int", "snow": "int", "maxtemp": "int",
                                "mintemp": "int", "meanwind": "double", "thunder": "int"},{"locn", "dateid"})
Retailer_1_Q2 = Relation("q2", {"ksn": "int", "locn": "int", "dateid": "int", "maxtemp": "int", "zip": "int", "rain":"int"}, {"ksn"})


Part = Relation("part", {"partkey": "int", "p_name": "string", "p_mfgr": "string", "p_brand": "string", "p_type": "string", "p_size": "int", "p_container": "string", "p_retailprice": "double", "p_comment": "string"}, {"partkey"})
Supplier= Relation("supplier", {"suppkey": "int", "s_name": "string", "s_address": "string", "nationkey": "int", "s_phone": "string", "s_acctbal": "double", "s_comment": "string"},{"suppkey"})
PartSupp= Relation("partsupp", {"partkey": "int", "suppkey": "int", "ps_availqty": "int", "ps_supplycost": "double", "ps_comment": "string"}, {"partkey", "suppkey"})
Customer= Relation("customer", {"o_custkey": "int", "c_name": "string", "c_address": "string", "nationkey": "int", "c_phone": "string", "c_acctbal": "double", "c_mktsegment": "string", "c_comment": "string"},{"custkey"})
Orders= Relation("orders", {"orderkey": "int", "o_custkey": "int", "o_orderstatus": "char", "o_totalprice": "double", "o_orderdate": "string", "o_orderpriority": "string", "o_clerk": "string", "o_shippriority": "int", "o_comment": "string"}, {"orderkey"})
Lineitem= Relation("lineitem", {"orderkey": "int", "partkey": "int", "suppkey": "int", "l_linenumber": "int", "l_quantity": "double", "l_extendedprice": "double", "l_discount": "double", "l_tax": "double", "l_returnflag": "char", "l_linestatus": "char", "l_shipdate": "string", "l_commitdate": "string", "l_receiptdate": "string", "l_shipinstruct": "string", "l_shipmode": "string", "l_comment": "string"},{"orderkey", "partkey", "suppkey"})
Nation= Relation("nation", {"nationkey": "int", "n_name": "string", "regionkey": "int", "n_comment": "string"}, {"nationkey"}  )
Region= Relation("region", {"regionkey": "int", "r_name": "string", "r_comment": "string"}, {"regionkey"}  )
TPCH_1_Q2 = Relation("q2", {"orderkey": "int", "partkey": "int", "suppkey": "int", "l_quantity": "double", "o_totalprice": "double"}, {"partkey", "suppkey"})
def generate_txt(all_relations: "List[Relation]", root: "VariableOrderNode", free_variables: set[str]):
    for relation in all_relations:
        iterator = root
        while True:
            found = False
            for child in iterator.children:
                if (child.child_variables().union({child.name})).intersection(relation.private_keys):
                    iterator = child
                    found = True
                    break
            if not found:
                variables_to_add = set(relation.variables.keys()).difference(iterator.parent_variables().union({iterator.name}))
                for variable in variables_to_add.intersection(free_variables):
                    new_node = VariableOrderNode(variable, relation.variables[variable])
                    iterator.add_child(new_node)
                    iterator = new_node
                for variable in variables_to_add.difference(free_variables):
                    new_node = VariableOrderNode(variable, relation.variables[variable])
                    iterator.add_child(new_node)
                    iterator = new_node
                relation.last_variable = iterator
                break
    root.set_id(0)
    all_vars = set()
    for rel in all_relations:
        all_vars.update(rel.variables.keys())
    config_start = f"{len(all_vars)} {len(all_relations)}\n"
    config_file = config_start + root.generate_config()
    for relation in all_relations:
        config_file += f"{relation.name} {relation.last_variable.id} {','.join(relation.variables.keys())}\n"
    print(config_file)

    return config_file

def generate_retailer_all():
    root = VariableOrderNode("locn")
    dateid = VariableOrderNode("dateid")
    ksn = VariableOrderNode("ksn")
    zip = VariableOrderNode("zip")
    root.add_child(dateid)
    dateid.add_child(ksn)
    root.add_child(zip)
    relations = [Inventory, Location, Census, Item, Weather]
    free_vars = {"locn", "dateid", "ksn", "zip", "category", "snow"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_retailer_3():
    root = VariableOrderNode("ksn")
    relations = [Item, Inventory]
    free_vars = {"locn", "dateid", "ksn", "category", "price"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_retailer_4Q1a():
    root = VariableOrderNode("ksn")
    locn = VariableOrderNode("locn")
    root.add_child(locn)
    relations = [Item, Inventory, Location]
    free_vars = {"locn", "ksn", "category", "zip"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_retailer_4Q1b():
    ksn = VariableOrderNode("ksn")
    root = VariableOrderNode("locn")
    root.add_child(ksn)
    relations = [Item, Inventory, Location]
    free_vars = {"locn", "ksn", "category", "zip"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_retailer_4Q2():
    root = VariableOrderNode("ksn")
    relations = [Item, Inventory]
    free_vars = {"locn", "ksn", "category", "price"}
    res = generate_txt(relations, root, free_vars)
    return res
def generate_retailer_1Q1b():
    root = VariableOrderNode("ksn")
    locn = VariableOrderNode("locn")
    root.add_child(locn)
    dateid = VariableOrderNode("dateid")
    locn.add_child(dateid)
    relations = [Item, Inventory, Location, Weather]
    free_vars = {"locn", "ksn", "category", "price"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_retailer_1Q1c():
    root = VariableOrderNode("ksn")
    relations = [Item, Retailer_1_Q2]
    free_vars = {"locn", "ksn", "category", "dateid", "rain", "zip"}
    res = generate_txt(relations, root, free_vars)
    return res
def generate_TPCH_3Q2():
    root = VariableOrderNode("suppkey")
    part = VariableOrderNode("partkey")
    root.add_child(part)
    relations = [Supplier, PartSupp, Lineitem]
    free_vars = {"suppkey", "partkey", "l_quantity", "ps_availqty", "ps_supplycost", "s_name"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_TPCH_1Q1b():
    root = VariableOrderNode("partkey")
    supp = VariableOrderNode("suppkey")
    order = VariableOrderNode("orderkey")
    root.add_child(supp)
    supp.add_child(order)
    relations = [Part, PartSupp, Lineitem, Orders]
    free_vars = {"orderkey","suppkey", "partkey", "l_quantity", "ps_availqty", "p_name", "o_totalprice"}
    res = generate_txt(relations, root, free_vars)
    return res

def generate_TPCH_1Q1c():
    root = VariableOrderNode("partkey")
    supp = VariableOrderNode("suppkey")
    root.add_child(supp)
    relations = [Part, PartSupp, TPCH_1_Q2]
    free_vars = {"orderkey","suppkey", "partkey", "l_quantity", "ps_availqty", "p_name", "o_totalprice"}
    res = generate_txt(relations, root, free_vars)
    return res

# generate_retailer_4Q1a()
# generate_retailer_4Q1b()
# generate_retailer_4Q2()
# generate_retailer_1Q1b()
generate_retailer_1Q1c()
# generate_TPCH_3Q2()
# generate_TPCH_1Q1b()
# generate_TPCH_1Q1c()
print("done")