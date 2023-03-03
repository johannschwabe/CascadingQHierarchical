import random

from graphviz import Digraph

from BitSet import BitSet
from JoinOrderNode import JoinOrderNode
from QueryGenerator import generate
from Relation import Relation
from Query import Query
from cascade import run
from greedy import greedy

random.seed(22)

def example_0():
    R1 = Relation("R1", {"x", "y"})
    R2 = Relation("R2", {"y", "z"})
    R3 = Relation("R3", {"z", "w"})
    Q1 = Query("Q1", {R1, R2}, {'x', 'y','z'})
    Q2 = Query("Q2", {R1, R2, R3}, {'x', 'y','z', 'w'})

    # res = run({Q1, Q2})
    res = greedy([Q2, Q1])
    res.graph_viz("ex0")
    return res

def example_1():
    R1 = Relation("R1", {"x","y"})
    R2 = Relation("R2", {"y","z"})
    R3 = Relation("R3", {"z","w"})
    R4 = Relation("R4", {"w","q"})

    Q1 = Query("Q1", {R1, R2}, {'x', 'y', 'z'})
    Q2 = Query("Q2", {R1, R2, R3}, {'x', 'y', 'z', 'w'})
    Q3 = Query("Q3", {R1, R2, R3, R4}, {'x', 'y', 'z', 'w', 'q'})
    # res = run({Q1, Q2, Q3})
    # res = greedy([Q1, Q2, Q3])
    res = greedy([Q3, Q2, Q1])
    res.graph_viz("ex1")
    return res

def example_2():
    R1 = Relation("R1", {"x", "y"})
    R2 = Relation("R2", {"y", "z"})
    R3 = Relation("R3", {"z", "w"})
    R4 = Relation("R4", {"w", "q"})

    Q1 = Query("Q1", {R1, R2},{'x', 'y', 'z'})
    Q2 = Query("Q2", {R3, R4},{'z', 'w', 'q'})
    Q3 = Query("Q3", {R1, R2, R3, R4},{'x', 'y', 'z', 'w', 'q'})
    res = run({Q1, Q2, Q3})
    res.graph_viz()

    return res
def example_3():
    R1 = Relation("R1", {"x", "y"})
    R2 = Relation("R2", {"y", "z"})
    R3 = Relation("R3", {"z", "w"})
    R4 = Relation("R4", {"w", "a"})
    R5 = Relation("R5", {"a", "b"})

    Q1 = Query("Q1", {R2,R3},{'y', 'z', 'w'})
    Q2 = Query("Q2", {R4,R3},{'z', 'w', 'a'})
    Q3 = Query("Q3", {R1,R2,R3},{'x', 'y', 'z', 'w',})
    Q4 = Query("Q4", {R3,R4,R5},{'z', 'w', 'a', 'b'})
    Q5 = Query("Q5", {R1,R2,R3,R4,R5},{'x', 'y', 'z', 'w', 'a', 'b'})
    res = run({Q1, Q2, Q3, Q4, Q5})
    res.graph_viz()

    return res

def example_4():
    R1 = Relation("R1", {"x", "y"})
    R2 = Relation("R2", {"y", "z"})
    R3 = Relation("R3", {"z", "w"})
    R4 = Relation("R4", {"w", "a"})

    Q1 = Query("Q1", {R1, R2, R3},{'x', 'y', 'z', 'w'})
    Q2 = Query("Q2", {R1, R2, R3, R4},{'x', 'y', 'z', 'w', 'a'})
    Q3 = Query("Q3", {R2, R1},{'x', 'y', 'z'})
    res = run({Q1, Q2, Q3})
    res.graph_viz()

    return res

# example_3()
def example_5():
    R0 = Relation("R0", {"x"})
    R1 = Relation("R1", {"x", "y"})
    R2 = Relation("R2", {"x", "y"})
    R3 = Relation("R3", {"x", "y", "a"})
    # R4 = Relation("R4", {"x", "y", "b"},4)
    R5 = Relation("R5", {"x", "y", "a", "c"})
    R6 = Relation("R6", {"x", "y", "b", "d", "e"})
    R7 = Relation("R7", {"f", "b"})

    Q1 = Query("Q1", {R0, R1, R2, R3, R5, R6},  {"x","y", "a"})
    graph = Digraph("View Example")
    Q1.variable_order.graph_viz(graph,"-")
    graph.view()
    Q2 = Query("Q2", {R1, R2, R3, R5, R6, R7},  {"x","y", "a"})
    res = run({Q1, Q2})
    res.graph_viz()
    # Q1.variable_order.generate_views(Q1)
    # qs = QuerySet()
    # qs.add(Q1)
    # qs.graph_viz()
    return

def example_6(nr_attempts: int, seed_base = 23445, _print = False):
    nr_valid = 0
    nr_run_success = 0
    nr_greedy_success = 0
    random.seed(seed_base)
    for _ in range(nr_attempts):
        resi: "list[Query]" = generate(nr_queries=5,
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
            for q in resi:
                for rel in q.relations:
                    rel.index = -1
            res_greedy = greedy(resi)
            res_run = run([q.clean_copy() for q in resi])
            queries = [q.clean_copy() for q in resi]
            random.shuffle(queries)
            res_run_2 = run(queries)
            if (res_run is None) != (res_run_2 is None):
                print("gugus happened")
            if res_run:

                nr_run_success += 1
                if _print:
                    print(f"Success on {_}")
                    res_run.graph_viz(_)
            if res_greedy:
                nr_greedy_success += 1



    print(f"{nr_attempts} groups generated, {nr_valid} valid, {nr_greedy_success}/{nr_run_success} successfull reduction")

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

    })
    Item = Relation("Item", {
        "Ksn",
        "SubCategory",
        "Category"
        "CategoryCluster",
        "Prize"
    })
    Inventory = Relation("Inventory", {
        "InventoryUnits",
        "Ksn",
        "DateId",
        "Locn"
    })
    Weather = Relation("Weather", {
        "DateId",
        "Locn",
        "MaxTemp",
        "Rain",
    })
    Location = Relation("Location", {
        "Locn",
        "Zip",
        "SellAreaSqFt",

    })
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
    res = run([Q1, Q2, Q3])
    if res:
        res.pop().graph_viz()
    else:
        print("no reduction")

def example_8():
    for i in range(1000,2000):
        seed_base =random.randint(16029,50000)
        print(seed_base)
        example_6(1, seed_base)

def example_9():
    R0 = Relation("R0", {"a","c"})
    R1 = Relation("R1", {"a","b","c"})
    R2 = Relation("R2", {"a","b","c"})
    R3 = Relation("R3", {"a","b","c"})
    R4 = Relation("R4", {"a","b","c"})
    R5 = Relation("R5", {"a","b","c"})
    R6 = Relation("R6", {"a","b","c"})
    R7 = Relation("R7", {"a","b","c"})

    Q0 = Query("Q0", {R0, R1, R2, R4, R5, R6, R7}, set())
    Q1 = Query("Q1", {R0, R1, R2,R3, R4, R5, R6}, {"a", "b", "c"})
    Q2 = Query("Q2", {R0, R1, R2,R3, R4, R5, R6, R7}, {"b", "c"})
    Q3 = Query("Q3", {R0, R1, R2, R3, R5, R6,}, {"a"})
    Q4 = Query("Q4", {R0, R4, R6}, {"a"})
    res = run({Q0,Q1,Q2,Q3,Q4})
    res.graph_viz("??")

def example_10():
    R0 = Relation("R0", {"a","c"})
    R1 = Relation("R1", {"a","b","c"})
    Q0 = Query("Q0", {R0, R1}, {"b", "c"})
    res = run({Q0})
    res.graph_viz("sdf")

# example_0()
# example_1()
# example_2()
# example_3()
# example_4()
# example_5()
example_6(30000, 900, _print=False)
# example_7()
# example_8()
# example_9()
# example_10()
print("done")