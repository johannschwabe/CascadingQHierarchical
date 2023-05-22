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


Part = Relation("PART", {"PARTKEY": "int", "P_NAME": "string", "P_MFGR": "string", "P_BRAND": "string", "P_TYPE": "string", "P_SIZE": "int", "P_CONTAINER": "string", "P_RETAILPRICE": "double", "P_COMMENT": "string"}, {"PARTKEY"})
Supplier= Relation("SUPPLIER", {"SUPPKEY": "int", "S_NAME": "string", "S_ADDRESS": "string", "NATIONKEY": "int", "S_PHONE": "string", "S_ACCTBAL": "double", "S_COMMENT": "string"},{"SUPPKEY"})
PartSupp= Relation("PARTSUPP", {"PARTKEY": "int", "SUPPKEY": "int", "PS_AVAILQTY": "int", "PS_SUPPLYCOST": "double", "PS_COMMENT": "string"}, {"PARTKEY", "SUPPKEY"})
Customer= Relation("CUSTOMER", {"CUSTKEY": "int", "C_NAME": "string", "C_ADDRESS": "string", "NATIONKEY": "int", "C_PHONE": "string", "C_ACCTBAL": "double", "C_MKTSEGMENT": "string", "C_COMMENT": "string"},{"CUSTKEY"})
Orders= Relation("ORDERS", {"ORDERKEY": "int", "CUSTKEY": "int", "O_ORDERSTATUS": "string", "O_TOTALPRICE": "double", "O_ORDERDATE": "string", "O_ORDERPRIORITY": "string", "O_CLERK": "string", "O_SHIPPRIORITY": "int", "O_COMMENT": "string"}, {"ORDERKEY"})
LineItem= Relation("LINEITEM", {"ORDERKEY": "int", "PARTKEY": "int", "SUPPKEY": "int", "L_LINENUMBER": "int", "L_QUANTITY": "double", "L_EXTENDEDPRICE": "double", "L_DISCOUNT": "double", "L_TAX": "double", "L_RETURNFLAG": "string", "L_LINESTATUS": "string", "L_SHIPDATE": "string", "L_COMMITDATE": "string", "L_RECEIPTDATE": "string", "L_SHIPINSTRUCT": "string", "L_SHIPMODE": "string", "L_COMMENT": "string"},{"ORDERKEY", "PARTKEY", "SUPPKEY"})
Nation= Relation("NATION", {"NATIONKEY": "int", "N_NAME": "string", "REGIONKEY": "int", "N_COMMENT": "string"}, {"NATIONKEY"}  )
Region= Relation("REGION", {"REGIONKEY": "int", "R_NAME": "string", "R_COMMENT": "string"}, {"REGIONKEY"}  )
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

def generate_TPCH_3Q2():
    root = VariableOrderNode("suppkey")
    part = VariableOrderNode("partkey")
    root.add_child(part)
    relations = [Supplier, PartSupp, LineItem]
    free_vars = {"suppkey", "partkey", "l_quantity", "ps_availqty", "ps_supplycost", "s_name"}
    res = generate_txt(relations, root, free_vars)
    return res

# generate_retailer_4Q1a()
# generate_retailer_4Q1b()
# generate_retailer_4Q2()
# generate_retailer_1Q1b()
generate_TPCH_3Q2()
print("done")