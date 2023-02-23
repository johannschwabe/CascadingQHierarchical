import random

from graphviz import Digraph

from BitSet import BitSet
from JoinOrderNode import JoinOrderNode
from QueryGenerator import generate
from Relation import Relation
from Query import Query
from cascade import run

random.seed(22)

def example_0():
    R1 = Relation("R1", {"x", "y"},0)
    R2 = Relation("R2", {"y", "z"},1)
    R3 = Relation("R3", {"z", "w"},2)
    Q1 = Query("Q1", {R1, R2}, {'x', 'y','z'})
    Q2 = Query("Q2", {R1, R2, R3}, {'x', 'y','z', 'w'})
    res = run({Q1, Q2})
    res.graph_viz("ex0")
    return res

def example_1():
    R1 = Relation("R1", {"x","y"},0)
    R2 = Relation("R2", {"y","z"},1)
    R3 = Relation("R3", {"z","w"},2)
    R4 = Relation("R4", {"w","q"},3)

    Q1 = Query("Q1", {R1, R2}, {'x', 'y', 'z'})
    Q2 = Query("Q2", {R1, R2, R3}, {'x', 'y', 'z', 'w'})
    Q3 = Query("Q3", {R1, R2, R3, R4}, {'x', 'y', 'z', 'w', 'q'})
    res = run({Q1, Q2, Q3})
    res.graph_viz("ex1")
    return res

def example_2():
    R1 = Relation("R1", {"x", "y"},0)
    R2 = Relation("R2", {"y", "z"},1)
    R3 = Relation("R3", {"z", "w"},2)
    R4 = Relation("R4", {"w", "q"},3)

    Q1 = Query("Q1", {R1, R2},{'x', 'y', 'z'})
    Q2 = Query("Q2", {R3, R4},{'z', 'w', 'q'})
    Q3 = Query("Q3", {R1, R2, R3, R4},{'x', 'y', 'z', 'w', 'q'})
    res = run({Q1, Q2, Q3})
    return res
def example_3():
    R1 = Relation("R1", {"x", "y"},1)
    R2 = Relation("R2", {"y", "z"},2)
    R3 = Relation("R3", {"z", "w"},3)
    R4 = Relation("R4", {"w", "a"},4)
    R5 = Relation("R5", {"a", "b"},5)

    Q1 = Query("Q1", {R2,R3},{'y', 'z', 'w'})
    Q2 = Query("Q2", {R4,R3},{'z', 'w', 'a'})
    Q3 = Query("Q3", {R1,R2,R3},{'x', 'y', 'z', 'w',})
    Q4 = Query("Q4", {R3,R4,R5},{'z', 'w', 'a', 'b'})
    Q5 = Query("Q5", {R1,R2,R3,R4,R5},{'x', 'y', 'z', 'w', 'a', 'b'})
    res = run({Q1, Q2, Q3, Q4, Q5})
    return res

def example_4():
    R1 = Relation("R1", {"x", "y"},1)
    R2 = Relation("R2", {"y", "z"},2)
    R3 = Relation("R3", {"z", "w"},3)
    R4 = Relation("R4", {"w", "a"},4)

    Q1 = Query("Q1", {R1, R2, R3},{'x', 'y', 'z', 'w'})
    Q2 = Query("Q2", {R1, R2, R3, R4},{'x', 'y', 'z', 'w', 'a'})
    Q3 = Query("Q3", {R2, R1},{'x', 'y', 'z'})
    res = run({Q1, Q2, Q3})
    res.pop().graph_viz()

    return res

# example_3()
def example_5():
    R0 = Relation("R0", {"x"},0)
    R1 = Relation("R1", {"x", "y"},1)
    R2 = Relation("R2", {"x", "y"},2)
    R3 = Relation("R3", {"x", "y", "a"},3)
    # R4 = Relation("R4", {"x", "y", "b"},4)
    R5 = Relation("R5", {"x", "y", "a", "c"},5)
    R6 = Relation("R6", {"x", "y", "b", "d", "e"},6)
    Q1 = Query("Q1", {R0, R1, R2, R3, R5, R6},  {"x","y", "a"})
    res = JoinOrderNode.generate(Q1.variable_order, Q1)
    graphy = Digraph("Gugus")
    res.viz(graphy, Q1)
    graphy.view()
    # Q1.variable_order.generate_views(Q1)
    # qs = QuerySet()
    # qs.add(Q1)
    # qs.graph_viz()
    return

def example_6(nr_attempts: int, seed_base = 23445, _print = False):
    nr_valid = 0
    nr_success = 0
    random.seed(seed_base)
    for _ in range(nr_attempts):
        resi = generate(nr_queries=5,
                        avg_nr_relations=6,
                        std_nr_relations=3,
                        avg_total_relations=12,
                        std_total_relations=3,
                        avg_nr_variables=5,
                        std_nr_variables=1,
                        avg_total_variables=8,
                        std_total_variables=3,
                        seed=seed_base + _
                        )
        bs = BitSet(resi)
        for query in resi:
            query.bitset = bs
        q_hierarchical = map(lambda x: x.is_q_hierarchical(), resi)
        not_q_hierarchical = map(lambda x: not x, q_hierarchical)
        if any(q_hierarchical) and any(not_q_hierarchical):
            if _ % 100 == 0:
                print(_)
            nr_valid += 1
    #        print("=============")
    #        for query in resi:
    #            print(f"{query} - {query.is_q_hierarchical()}")
            res = run(resi)
            if res:
                nr_success += 1
                if _print:
                    print(f"Success on {_}")

                    # for i, query_set in enumerate(res_list[:1]):
                    res.graph_viz(_)
                    #break

        #            for reduction in res:
        #                print("-------------")
        #                for query in reduction.queries:
        #                    print(query)

    print(f"{nr_attempts} groups generated, {nr_valid} valid, {nr_success} successfull reduction")

def example_7():
    Census = Relation("Census", {
        "Zip",
        "Population",
        "White",
        "Asian",
        "Pacific",
        "Black",
        "Hispanic",
        "Males",
        "Females",
        "HusbWife",
        "MedianAge",
        "HouseUnits",
        "OccupiedHouseUnits",
        "Families",
        "Housholds",
        "HousholdsChildren"

    },0)
    Item = Relation("Item", {
        "Ksn",
        "SubCategory",
        "Category"
        "CategoryCluster",
        "Prize"
    },1)
    Inventory = Relation("Inventory", {
        "InventoryUnits",
        "Ksn",
        "DateId",
        "Locn"
    },2)
    Weather = Relation("Weather", {
        "DateId",
        "Locn",
        "MaxTemp",
        "Rain",
    },3)
    Location = Relation("Location", {
        "Locn",
        "Zip",
        "SellAreaSqFt",

    },4)
    # Census = Relation("Census", {
    #     "Zip",
    #     "Population",
    #     "White",
    #     "Asian",
    #     "Pacific",
    #     "Black",
    #     "Hispanic",
    #     "Males",
    #     "Females",
    #     "HusbWife",
    #     "MedianAge",
    #     "HouseUnits",
    #     "OccupiedHouseUnits",
    #     "Families",
    #     "Housholds",
    #     "HousholdsChildren"
    #
    # })
    # Item = Relation("Item",{
    #     "Ksn",
    #     "SubCategory",
    #     "Category"
    #     "CategoryCluster",
    #     "Prize"
    # })
    # Inventory = Relation("Inventory", {
    #     "InventoryUnits",
    #     "Ksn",
    #     "DateId",
    #     "Locn"
    # })
    # Weather = Relation("Weather", {
    #     "DateId",
    #     "Locn",
    #     "MaxTemp",
    #     "MinTemp",
    #     "MeanWind",
    #     "Snow",
    #     "Rain",
    #     "Thunder",
    # })
    # Location = Relation("Location", {
    #     "Locn",
    #     "Zip",
    #     "RgnCd",
    #     "ClimbZnNbr",
    #     "TotalAreaSqFt",
    #     "SellAreaSqFt",
    #     "AvgHigh",
    #     "SuperTargetDistance",
    #     "SuperTargetDriveTime",
    #     "TargetDistance",
    #     "TargetDriveTime",
    #     "WalmartDistance",
    #     "WalmartDriveTime",
    #     "WalmartSuperCenterDistance",
    #     "WalmartSuperCenterDriveTime"
    # })

    Q1 = Query("Q1", {Inventory, Item, Weather, Location}, {"Ksn","Category", "Zip", "Rain"})          # Select Ksn, Category, Zip, Rain, Avg(Price)
    Q2 = Query("Q2", {Inventory, Weather, Item}, {"Locn", "DateId", "Ksn", "Category"})
    Q3 = Query("Q3", {Inventory, Weather, Location}, {"Ksn","Locn", "DateId", "MaxTemp", "Zip"})

    print(Q1.is_q_hierarchical())
    print(Q2.is_q_hierarchical())
    print(Q3.is_q_hierarchical())
    # res = run({Q1, Q3})
    res = run({Q1, Q2, Q3})
    if res:
        res.pop().graph_viz()
    else:
        print("no reduction")

def example_8():
    for i in range(1000,2000):
        seed_base =random.randint(16029,50000)
        print(seed_base)
        example_6(1, seed_base)

# example_0()
# example_1()
# example_2()
# example_3()
# example_4()
# example_5()
example_6(3000, 432, _print=True)
# example_7()
# example_8()
print("done")