from typing import TYPE_CHECKING

from ordered_set import OrderedSet

from M3MultiQueryGenerator import M3MultiQueryGenerator
from cascade import run
from Query import Query
from Relation import Relation

TPCH_sizes = [1,10]

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
        for tpch in TPCH_sizes:
            multigenerator = M3MultiQueryGenerator(
                'tpch',
                "3",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        #res.graph_viz("TPCH_3")
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
        for tpch in TPCH_sizes:
            multigenerator = M3MultiQueryGenerator(
                'tpch',
                "1",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        #res.graph_viz("TPCH_1")
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
        for tpch in TPCH_sizes:
            multigenerator = M3MultiQueryGenerator(
                'tpch',
                "2",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        #res.graph_viz("TPCH_2")
        print("Success")

    else:
        print("No result")

def example_4():
    Q1 = Query("Q1", OrderedSet([PartSupp, LineItem, Orders, Customer, Supplier]), OrderedSet(["SUPPKEY", "PARTKEY", "ORDERKEY", "CUSTKEY", "NATIONKEY"]))
    Q2 = Query("Q2", OrderedSet([PartSupp, LineItem, Supplier]), OrderedSet(["SUPPKEY", "PARTKEY", "ORDERKEY", "NATIONKEY", "L_QUANTITY", "PS_SUPPLYCOST", "PS_AVAILQTY", "S_NAME"]))
    Q3 = Query("Q3", OrderedSet([Customer, Orders]), OrderedSet(["CUSTKEY", "ORDERKEY", "NATIONKEY"]))
    res = run([Q1, Q2, Q3])
    if res:
        for tpch in TPCH_sizes:
            multigenerator = M3MultiQueryGenerator(
                'tpch',
                "4",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        # res.graph_viz("TPCH_4")
        print("Success")

    else:
        print("No result")

def example_5():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, Supplier, Customer, Nation]), OrderedSet(["PARTKEY", "NATIONKEY", "SUPPKEY", "N_NAME", "S_NAME", "P_NAME", "PS_AVAILQTY"]))
    Q2 = Query("Q2", OrderedSet([Supplier, Customer, Nation]), OrderedSet(["NATIONKEY","SUPPKEY", "S_NAME", "N_NAME", "S_ADDRESS", "CUSTKEY"]))
    Q3 = Query("Q3", OrderedSet([Part, PartSupp]), OrderedSet(["PARTKEY","SUPPKEY", "PS_AVAILQTY", "P_NAME"]))
    res = run([Q1, Q2, Q3])
    if res:
        for tpch in TPCH_sizes:
            multigenerator = M3MultiQueryGenerator(
                'tpch',
                "5",
                str(tpch),
                'RingFactorizedRelation',
                res,
                datatypes,
                "tbl"
            )
            multigenerator.generate(batch=True)

        # res.graph_viz("TPCH_5")
        print("Success")

    else:
        print("No result")

if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()
    example_5()
