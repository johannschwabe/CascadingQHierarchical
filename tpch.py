from typing import TYPE_CHECKING

from ordered_set import OrderedSet

from M3MultiQueryGenerator import M3MultiQueryGenerator
from cascade import run
from Query import Query, QuerySet
from Relation import Relation

dataset_version = ["_unordered10"]
base_dataset = "tpch"
# base_dataset = "jcch"
view = False

Part = Relation("part", OrderedSet(
    ["PARTKEY", "P_NAME", "P_MFGR", "P_BRAND", "P_TYPE", "P_SIZE", "P_CONTAINER", "P_RETAILPRICE", "P_COMMENT"]))
Supplier = Relation("supplier",
                    OrderedSet(["SUPPKEY", "S_NAME", "S_ADDRESS", "NATIONKEY", "S_PHONE", "S_ACCTBAL", "S_COMMENT"]))
PartSupp = Relation("partsupp", OrderedSet(["PARTKEY", "SUPPKEY", "PS_AVAILQTY", "PS_SUPPLYCOST", "PS_COMMENT"]))
Customer = Relation("customer", OrderedSet(
    ["CUSTKEY", "C_NAME", "C_ADDRESS", "NATIONKEY", "C_PHONE", "C_ACCTBAL", "C_MKTSEGMENT", "C_COMMENT"]))
Orders = Relation("orders", OrderedSet(
    ["ORDERKEY", "CUSTKEY", "O_ORDERSTATUS", "O_TOTALPRICE", "O_ORDERDATE", "O_ORDERPRIORITY", "O_CLERK", "O_SHIPPRIORITY",
     "O_COMMENT"]))
LineItem = Relation("lineitem", OrderedSet(
    ["ORDERKEY", "PARTKEY", "SUPPKEY", "L_LINENUMBER", "L_QUANTITY", "L_EXTENDEDPRICE", "L_DISCOUNT", "L_TAX", "L_RETURNFLAG",
     "L_LINESTATUS", "L_SHIPDATE", "L_COMMITDATE", "L_RECEIPTDATE", "L_SHIPINSTRUCT", "L_SHIPMODE", "L_COMMENT"]))
Nation = Relation("nation", OrderedSet(["NATIONKEY", "N_NAME", "REGIONKEY", "N_COMMENT"]))
Region = Relation("region", OrderedSet(["REGIONKEY", "R_NAME", "R_COMMENT"]))

datatypes: dict[str, str] = {
    "PARTKEY": "int",
    "P_NAME": "string",
    "P_MFGR": "string",
    "P_BRAND": "string",
    "P_TYPE": "string",
    "P_SIZE": "int",
    "P_CONTAINER": "string",
    "P_RETAILPRICE": "double",
    "P_COMMENT": "string",
    "SUPPKEY": "int",
    "S_NAME": "string",
    "S_ADDRESS": "string",
    "NATIONKEY": "int",
    "S_PHONE": "string",
    "S_ACCTBAL": "double",
    "S_COMMENT": "string",
    "PS_AVAILQTY": "int",
    "PS_SUPPLYCOST": "double",
    "PS_COMMENT": "string",
    "CUSTKEY": "int",
    "C_NAME": "string",
    "C_COMMENT": "string",
    "C_ADDRESS": "string",
    "C_PHONE": "string",
    "C_ACCTBAL": "double",
    "C_MKTSEGMENT": "string",
    "ORDERKEY": "int",
    "O_ORDERSTATUS": "string",
    "O_TOTALPRICE": "double",
    "O_ORDERDATE": "string",
    "O_ORDERPRIORITY": "string",
    "O_CLERK": "string",
    "O_SHIPPRIORITY": "int",
    "O_COMMENT": "string",
    "L_LINENUMBER": "int",
    "L_QUANTITY": "double",
    "L_EXTENDEDPRICE": "double",
    "L_DISCOUNT": "double",
    "L_TAX": "double",
    "L_RETURNFLAG": "string",
    "L_LINESTATUS": "string",
    "L_SHIPDATE": "string",
    "L_COMMITDATE": "string",
    "L_RECEIPTDATE": "string",
    "L_SHIPINSTRUCT": "string",
    "L_SHIPMODE": "string",
    "L_COMMENT": "string",
    "N_NAME": "string",
    "REGIONKEY": "int",
    "N_COMMENT": "string",
    "R_NAME": "string",
    "R_COMMENT": "string",

}
# for rel in [Part, Supplier, PartSupp, Customer, Orders, LineItem, Nation, Region]:
#     attribute_list = [f"\"{variable}\": \"{datatypes[variable]}\"" for variable in rel.free_variables]
#     print(f"\"{rel.name}\", {{{', '.join(attribute_list)}}}")
#

def example_1():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, LineItem, Supplier]),
               OrderedSet(["P_NAME", "S_NAME", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY"]))
    Q2 = Query("Q2", OrderedSet([PartSupp, LineItem, Supplier]),
               OrderedSet(["S_NAME", "PS_AVAILQTY", "L_QUANTITY", "PS_SUPPLYCOST", "PARTKEY", "SUPPKEY"]))
    print(Q1.is_q_hierarchical())
    print(Q2.is_q_hierarchical())
    res = run([Q1, Q2])
    if res:
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "3",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz("TPCH_3", join_order=True)
    else:
        print("No result")

def example_2():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, LineItem, Orders]),
               OrderedSet(["P_NAME", "O_TOTALPRICE", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY", "ORDERKEY"]))
    Q2 = Query("Q2", OrderedSet([LineItem, Orders]),
               OrderedSet([ "O_TOTALPRICE", "L_QUANTITY", "PARTKEY", "SUPPKEY", "ORDERKEY"]))
    print(Q1.is_q_hierarchical())
    print(Q2.is_q_hierarchical())
    res = run([Q1, Q2])
    if res:
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "1",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz("TPCH_1", join_order=True)
        print("Success")
    else:
        print("No result")

def example_3():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, LineItem, Orders]),
               OrderedSet(["P_NAME", "O_TOTALPRICE", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY", "ORDERKEY"]))
    Q2 = Query("Q2", OrderedSet([Part, PartSupp, LineItem]),
               OrderedSet([ "P_NAME", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY", "ORDERKEY"]))
    print(Q1.is_q_hierarchical())
    print(Q2.is_q_hierarchical())
    res = run([Q1, Q2])
    if res:
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "2",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz("TPCH_2", join_order=True)
        print("Success")

    else:
        print("No result")

def example_4():
    Q1 = Query("Q1", OrderedSet([PartSupp, LineItem, Orders, Customer, Supplier]), OrderedSet(["SUPPKEY", "PARTKEY", "ORDERKEY", "CUSTKEY", "NATIONKEY"]))
    Q2 = Query("Q2", OrderedSet([PartSupp, LineItem, Supplier]), OrderedSet(["SUPPKEY", "PARTKEY", "ORDERKEY", "NATIONKEY", "L_QUANTITY", "PS_SUPPLYCOST", "PS_AVAILQTY", "S_NAME"]))
    Q3 = Query("Q3", OrderedSet([Customer, Orders]), OrderedSet(["CUSTKEY", "ORDERKEY", "NATIONKEY"]))
    res = run([Q1, Q2, Q3])
    if res:
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "4",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz("TPCH_4", join_order=True)
        print("Success")

    else:
        print("No result")

def example_5():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, Supplier, Customer, Nation]), OrderedSet(["PARTKEY", "NATIONKEY", "SUPPKEY", "N_NAME", "S_NAME", "P_NAME", "PS_AVAILQTY"]))
    Q2 = Query("Q2", OrderedSet([Supplier, Customer, Nation]), OrderedSet(["NATIONKEY","SUPPKEY", "S_NAME", "N_NAME", "S_ADDRESS", "CUSTKEY"]))
    Q3 = Query("Q3", OrderedSet([Part, PartSupp]), OrderedSet(["PARTKEY","SUPPKEY", "PS_AVAILQTY", "P_NAME"]))
    res = run([Q1, Q2, Q3])
    if res:
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "5",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz("TPCH_5", join_order=True)
        print("Success")

    else:
        print("No result")

def example_6():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, LineItem, Supplier]),
               OrderedSet(["P_NAME", "S_NAME", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY"]))
    Q2 = Query("Q3", OrderedSet([PartSupp, Supplier]),
               OrderedSet(["S_NAME", "PS_AVAILQTY", "PS_SUPPLYCOST", "PARTKEY", "SUPPKEY"]))
    print(Q1.is_q_hierarchical())
    print(Q2.is_q_hierarchical())
    res = run([Q1, Q2])
    if res:
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "6",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz("TPCH_6", join_order=True)
    else:
        print("No result")

def example_7():
    Q2 = Query("Q2", OrderedSet([PartSupp, Supplier]),
               OrderedSet(["P_NAME", "PS_AVAILQTY", "PS_SUPPLYCOST", "PARTKEY", "SUPPKEY"]))
    RQ2 = Relation("Q3", OrderedSet(["P_NAME", "PS_AVAILQTY", "PS_SUPPLYCOST", "PARTKEY", "SUPPKEY"]), None, Q2)
    Q3 = Query("Q3", OrderedSet([PartSupp,Supplier, LineItem]),
               OrderedSet([ "P_NAME", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY", "ORDERKEY"]), OrderedSet([RQ2, LineItem]))

    res = QuerySet({Q2, Q3})
    multigenerator = M3MultiQueryGenerator(
        base_dataset,
        "7",
        "_unordered10",
        'RingFactorizedRelation',
        res,
        datatypes,
        "tbl"
    )
    multigenerator.generate(batch=True)
    if view:
        res.graph_viz("TPCH_7", join_order=True)

def tpch_haozhe():
    Q1 = Query("Q1", OrderedSet([PartSupp, LineItem]),
               OrderedSet(["PS_AVAILQTY", "PARTKEY", "SUPPKEY", "L_LINENUMBER", "ORDERKEY"]))
    Q1Relation = Relation("Q1", OrderedSet(["PS_AVAILQTY", "PARTKEY", "SUPPKEY", "L_LINENUMBER", "ORDERKEY"]), None, Q1)
    Q4 = Query("Q4", OrderedSet([PartSupp, LineItem, Part]),
               OrderedSet(["PS_AVAILQTY", "PARTKEY", "SUPPKEY", "L_LINENUMBER", "ORDERKEY", "P_NAME"]),
               OrderedSet([Q1Relation, Part]))
    res = QuerySet({Q1, Q4})
    if res:
        multigenerator = M3MultiQueryGenerator(
            base_dataset,
            "7",
            "1",
            'RingFactorizedRelation',
            res,
            datatypes,
            "tbl"
        )
        multigenerator.generate(batch=True)
        res.graph_viz("TPCH_6", join_order=True)
def example_9():
    Q2 = Query("Q2", OrderedSet([Orders, Customer]),
               OrderedSet(["O_ORDERSTATUS", "C_NAME", "ORDERKEY", "CUSTKEY"]))
    Q2Relation = Relation("Q2", OrderedSet(
        ["O_ORDERSTATUS", "C_NAME", "ORDERKEY", "CUSTKEY"]), None, Q2)
    Q1 = Query("Q1", OrderedSet([Orders, LineItem]),
               OrderedSet(["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER"]))
    Q1Relation = Relation("Q1", OrderedSet(
        ["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER"]), None, Q1)
    Q3 = Query("Q3", OrderedSet([Orders, LineItem, Customer]),
               OrderedSet(["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER", "CUSTKEY", "C_NAME"]),
               OrderedSet([Q1Relation, Q2Relation]))
    Q3.dependant_on.update({Q1, Q2})
    res = QuerySet({Q1, Q2, Q3})
    res_list = [res]

    for (i, res) in enumerate(res_list):
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                f"9_{i}",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz(f"TPCH_9_{i}")

    if len(res_list) == 0:
        print("No result")
def example_10():
    Q1 = Query("Q1", OrderedSet([Orders, LineItem]),
               OrderedSet(["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER", "PARTKEY", "SUPPKEY", "CUSTKEY"]))
    Q1Relation = Relation("Q1", OrderedSet(
        ["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER", "PARTKEY", "SUPPKEY", "CUSTKEY"]), None, Q1)

    Q2 = Query("Q2", OrderedSet([Orders, LineItem, Customer]),
               OrderedSet(["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER",
                           "PARTKEY", "SUPPKEY", "CUSTKEY", "C_NAME"]),
               OrderedSet([Q1Relation, Customer]))
    Q2.dependant_on.update({Q1})

    Q3 = Query("Q3", OrderedSet([Orders, LineItem, PartSupp]),
               OrderedSet(["O_ORDERSTATUS", "ORDERKEY", "L_LINENUMBER",
                           "PARTKEY", "SUPPKEY", "PS_AVAILQTY"]),
               OrderedSet([Q1Relation, PartSupp]))
    Q3.dependant_on.update({Q1})

    res = QuerySet({Q1, Q2, Q3})
    res_list = [res]

    for (i, res) in enumerate(res_list):
        for tpch in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                f"10_{i}",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        if view:
            res.graph_viz(f"TPCH_10_{i}")

    if len(res_list) == 0:
        print("No result")

if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()
    # example_5()
    example_6()
    example_7()
    # tpch_haozhe()
    # example_9()
    # example_10()