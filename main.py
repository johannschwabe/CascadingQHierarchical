import random

from graphviz import Digraph

from BitSet import BitSet
from JoinOrderNode import JoinOrderNode
from QueryGenerator import generate
from Relation import Relation
from Query import Query, QuerySet
from backward import backward_search
from cascade import run
#from greedy import greedy

random.seed(22)

def test_queries(queries: "list[Query]", var_tree = False):
    run_1_queries = [q.clean_copy() for q in queries]
    res_run_1 = run(run_1_queries)
    if res_run_1:
        print('forward success')
        res_run_1.graph_viz("success")
    else:
        print('Forward Failed')
    run_2_queries = [q.clean_copy() for q in queries]
    res_run_2 = backward_search(run_2_queries)
    if res_run_2:
        print("backward success")
        res_run_2.graph_viz("Backward")
        if var_tree:
            for q in res_run_2.queries:
                graphy = Digraph()
                q.variable_order.graph_viz(graphy, q.name)
                graphy.view(q.name)
    else:
        print("Backward Failed")


def example_0():
    R1 = Relation("R1", {"x", "y"})
    R2 = Relation("R2", {"y", "z"})
    R3 = Relation("R3", {"z", "w"})
    Q1 = Query("Q1", {R1, R2}, {'y','z'})
    Q2 = Query("Q2", {R1, R2, R3}, { 'y','z', 'w'})

    res = run([Q1, Q2])
    # res = greedy([Q2, Q1])
    # res = backward_search([Q2, Q1])
    res.graph_viz("ex0")
    return res

def example_1():
    R1 = Relation("R1", {"a","b"})
    R2 = Relation("R2", {"b","c"})
    R3 = Relation("R3", {"c","d"})
    R4 = Relation("R4", {"b","e"})
    R5 = Relation("R5", {"e","f"})

    Q1 = Query("Q1", {R1, R2}, {'a', 'b', 'c'})
    Q2 = Query("Q2", {R1, R2, R3}, {'a', 'b', 'c', 'd'})
    Q3 = Query("Q3", {R1, R2, R3, R4}, {'a', 'b','c','d', 'e'})
    # Q3 = Query("Q3", {R1, R2, R3, R4}, {'a', 'b', 'c', 'd', 'e'})
    res = run([Q1, Q2, Q3])
    # res = greedy([Q1, Q2, Q3])
    # QS = QuerySet({Q1, Q2, Q3})
    # QS.graph_viz()
    # res = backward_search([Q2, Q1, Q3])
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
    res = backward_search([Q1, Q2, Q3])
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
    res = run([Q1, Q2, Q3, Q4, Q5])
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
    res = run([Q1, Q2, Q3])
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
    res = run([Q1, Q2])
    res.graph_viz()
    # Q1.variable_order.generate_views(Q1)
    # qs = QuerySet()
    # qs.add(Q1)
    # qs.graph_viz()
    return

def example_6(nr_attempts: int, seed_base = 23445, _print = False, _break = False):
    nr_valid = 0
    nr_run_success = 0
    nr_greedy_success = 0
    random.seed(seed_base)
    for _ in range(nr_attempts):
        resi: "list[Query]" = generate(nr_queries=3,
                        avg_nr_relations=3,
                        std_nr_relations=2,
                        avg_total_relations=5,
                        std_total_relations=2,
                        avg_nr_variables=4,
                        std_nr_variables=1,
                        avg_total_variables=7,
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
            for q in resi:
                for rel in q.relations:
                    rel.index = -1
            res_run_1 = run(resi)
            if res_run_1:
                nr_run_success += 1
                if _print:
                    print(f"Success on {_}")
                    res_run_1.graph_viz(_)

    print(f"{nr_attempts} groups generated, {nr_valid} valid, {nr_run_success} successfull reduction")

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
    res = run([Q0, Q1, Q2, Q3, Q4])
    res.graph_viz("??")

def example_10():
    R0 = Relation("R0", {"a","c"})
    R1 = Relation("R1", {"a","b","c"})
    Q0 = Query("Q0", {R0, R1}, {"b", "c"})
    res = run([Q0])
    res.graph_viz("sdf")

def example_11():
    R0 = Relation("R0", {"a","b","c","d","e"})
    R1 = Relation("R1", {"a","b","c","d","e"})
    R2 = Relation("R2", {"a","b","c","d","e"})
    R3 = Relation("R3", {"b", "c", "d", "e"})
    R4 = Relation("R4", {"a", "c", "d", "e"})
    R5 = Relation("R5", {"a","b","c","d","e"})
    R6 = Relation("R6", {"a","b","c","d","e"})
    R7 = Relation("R7", {"a","b","c","d","e"})
    R8 = Relation("R8", {"a","b","c","d","e"})
    R9 = Relation("R9", {"a","b","c","d","e"})
    R10 = Relation("R10", {"a","b","c","d","e"})

    Q0 = Query("Q0", {R1, R3, R4, R7}, {'d', 'e'})
    Q1 = Query("Q1", {R1, R2, R3, R7}, {'b'})
    Q2 = Query("Q2", {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10}, set())

    res_1 = run([Q0, Q1, Q2])
    if res_1:
        res_1.graph_viz(1)
    else:
        print("res_1 failed")

    R0 = Relation("R0", {"a", "b", "c", "d", "e"})
    R1 = Relation("R1", {"a", "b", "c", "d", "e"})
    R2 = Relation("R2", {"a", "b", "c", "d", "e"})
    R3 = Relation("R3", {"b", "c", "d", "e"})
    R4 = Relation("R4", {"a", "c", "d", "e"})
    R5 = Relation("R5", {"a", "b", "c", "d", "e"})
    R6 = Relation("R6", {"a", "b", "c", "d", "e"})
    R7 = Relation("R7", {"a", "b", "c", "d", "e"})
    R8 = Relation("R8", {"a", "b", "c", "d", "e"})
    R9 = Relation("R9", {"a", "b", "c", "d", "e"})
    R10 = Relation("R10", {"a", "b", "c", "d", "e"})

    Q0 = Query("Q0", {R1, R3, R4, R7}, {'d', 'e'})
    Q1 = Query("Q1", {R1, R2, R3, R7}, {'b'})
    Q2 = Query("Q2", {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10}, set())
    res_2 = run([Q2, Q1, Q0])
    if res_2:
        res_2.graph_viz(2)
    else:
        print("res_2 failed")

def example_12():
    R0 = Relation("R0", {'a', 'b',  'c'})
    R1 = Relation("R1", {'a', 'b',  'c'})
    R2 = Relation("R2", {'a', 'b',  'c'})
    R3 = Relation("R3", {'a', 'b',  'c'})
    R4 = Relation("R4", {'a', 'b',  'c'})
    R5 = Relation("R5", {'a', 'b',  'c'})
    R6 = Relation("R6", {'a', 'b',  'c'})
    R7 = Relation("R7", {'a', 'b',  'c'})
    R8 = Relation("R8", {'a', 'b',  'c'})
    R9 = Relation("R9", {'a', 'b',  'c'})
    R10 = Relation("R10", {'a', 'b',  'c'})
    R11 = Relation("R11", {'a', 'b',  'c'})
    R12 = Relation("R12", {'a', 'b'})
    R13 = Relation("R13", {'a', 'b',  'c'})
    R14 = Relation("R14", {'a', 'b',  'c'})


    Q0 = Query("Q0", {R0, R1, R10, R11, R12, R13, R14, R2, R4, R5, R6, R7, R8, R9}, {'a', 'b', 'c'})
    # Q1 = Query("Q1", {R0, R1, R11, R6, R7, R8, R9}, set())
    Q2 = Query("Q2", {R0, R10, R12, R13, R2, R3, R6, R7, R8}, {'b', 'c'})

    queries = [Q0, Q2]
    run_1_queries = [q.clean_copy() for q in queries]
    run_2_queries = [q.clean_copy() for q in queries]
    res_run_2 = backward_search(run_2_queries)
    print("Back Done")
    res_run_1 = run(run_1_queries)
    if res_run_1:
        res_run_1.graph_viz("success")
    if res_run_2:
        print("backward success")
        res_run_2.graph_viz("Backward")
    else:
        print("Backward Failed")
def example_13():
    R1 = Relation('R1', {'a', 'b'})
    R2 = Relation('R2', {'c', 'b'})
    R3 = Relation('R3', {'a', 'b', 'd', 'e'})
    Q0 = Query('Q0', {R1, R2, R3}, {'a', 'b', 'c'})
    graph = Digraph()
    Q0.variable_order.graph_viz(graph)
    graph.view()
    QS = QuerySet({Q0})
    QS.graph_viz("View Tree")

def example_14():
    R1 = Relation('R1', {'a', 'b', 'c'})
    R2 = Relation('R2', {'a', 'b', 'd'})
    R3 = Relation('R3', {'a', 'e'})
    Q1 = Query('Q1', {R1, R2, R3}, {'a', 'b', 'c', 'd', 'e'})
    graph = Digraph()
    Q1.variable_order.graph_viz(graph)
    graph.view()
    QS = QuerySet({Q1})
    QS.graph_viz("View Tree")

def example_15():
    R1 = Relation('R1', {'x','y'})
    R2 = Relation('R2', {'x','y'})
    R3 = Relation('R3', {'x', 'y', 'a'})
    R4 = Relation('R4', {'x', 'y', 'b'})
    R5 = Relation('R5', {'x', 'y', 'a', 'c'})
    R6 = Relation('R6', {'x', 'y', 'b', 'd'})

    Q1 = Query('Q1', {R1, R2, R3, R4, R5, R6,}, {'x', 'y','a', 'b', 'c', 'd'})
    graph = Digraph()
    Q1.variable_order.graph_viz(graph)
    graph.view()
    # QS = QuerySet({Q1})
    # QS.graph_viz("View Tree")

def example_16(nr_attempts: int, seed_base = 23445, _print = False):
    random.seed(seed_base)
    for _ in range(nr_attempts):
        resi: "list[Query]" = generate(nr_queries=6,
                        avg_nr_relations=3,
                        std_nr_relations=1,
                        avg_total_relations=5,
                        std_total_relations=3,
                        avg_nr_variables=4,
                        std_nr_variables=1,
                        avg_total_variables=7,
                        std_total_variables=2,
                        seed=seed_base + _
                        )
        for query in resi:
            for rel in query.relations:
                rel.index = -1
            bs = BitSet([query])
            query.bitset = bs
            if not query.is_q_hierarchical():
                graph = Digraph()
                query.variable_order.graph_viz(graph)
                graph.view()
                query.resolving_views()
def example_17():
    R0 = Relation("R0", {'a', 'c', 'd'})
    R1 = Relation("R1", {'c', 'e'})
    R2 = Relation("R2", {'a', 'b', 'c', 'f', 'e'})
    Q0 = Query("Q0", {R0, R1}, {'a', 'c', 'd', 'e'})
    Q1 = Query("Q1", {R0, R1, R2}, {'c', 'd', 'e'})
    Q2 = Query("Q2", {R0, R1, R2}, {'b', 'd'})
    Q3 = Query("Q3", {R0, R1, R2}, {'e', 'f'})
    Q4 = Query("Q4", {R0, R1, R2}, {'a', 'c', 'd', 'f', 'e'})
    Q5 = Query("Q5", {R0, R1, R2, }, {'b', 'f'})

    test_queries([Q0,Q1,Q2, Q3, Q4, Q5])


def example_18():
    R0 = Relation("R0", {'a', 'b', 'c', 'd'}, index=0)
    R1 = Relation("R1", {'b', 'c', 'd'}, index=1)
    R2 = Relation("R2", {'a','b', 'c', 'd'}, index=2)
    R3 = Relation("R3", {'d','e'}, index=3)
    R4 = Relation("R4", {'a', 'b', 'd', 'e', 'f'}, index=4)

    Q0 = Query("Q0", {R3, R4}, {'a', 'b', 'd', 'e', 'f'})
    Q1 = Query("Q1", {R0, R1}, {'a', 'b', 'c', 'd'})
    Q2 = Query("Q2", {R0, R1, R2, R3, R4}, {'a', 'b', 'c', 'd', 'f'})

    test_queries([Q0,Q1,Q2])

def example_19():
    R0 = Relation("R0", {'b', 'c', 'f', 'g', 'h'}, index=0)
    R1 = Relation("R1", {'c', 'd', 'e'}, index=1)
    Q0 = Query('Q0', {R0, R1}, {'c'})
    Q1 = Query('Q1', {R0, R1}, {'b', 'd', 'e', 'g', 'h'})
    Q2 = Query('Q2', {R0, R1}, set())
    test_queries([Q0,Q1,Q2])

def example_20():
    R0 = Relation('R0', {'e', 'f', 'h', 'i'}, index=0)
    R1 = Relation('R1', {'b', 'e', 'h'}, index=1)
    R2 = Relation('R2', {'b', 'c', 'd', 'f', 'i'}, index=2)
    R3 = Relation('R3', {'d', 'e', 'g'}, index=3)
    Q0 = Query('Q0', {R2, R3}, {'d', 'c', 'e', 'f', 'g', 'i'})
    Q1 = Query('Q1', {R0,R1,R3}, {'b', 'd', 'e', 'f', 'g','h','i'})
    Q2 = Query('Q2', {R1,R3}, {'d'})

    test_queries([Q0,Q1,Q2])

def example_21():
    R0 = Relation('R0', {'b', 'f'}, index=3)
    R1 = Relation('R1', {'b', 'c', 'f'}, index=1)
    R2 = Relation('R2', {'a', 'd'}, index=4)
    R3 = Relation('R3', {'a', 'b', 'c', 'f'}, index=2)
    R4 = Relation('R4', {'d', 'f'}, index=0)

    Q0 = Query('Q0', {R0, R1, R2, R3, R4}, {'b', 'c', 'd'})
    Q2 = Query('Q2', {R0, R2, R3, R4}, {'a', 'b', 'd', 'f'})
    Q1 = Query('Q1', {R0, R3}, set())

    test_queries([Q0,Q1,Q2])

def example_22():
    R0 = Relation('R0', {'a', 'b', 'f', 'g', 'h'})
    R1 = Relation('R1', {'a', 'g', 'i'})
    R2 = Relation('R2', {'d', 'g', 'i'})
    R3 = Relation('R3', {'e', 'i', 'j'})
    R4 = Relation('R4', {'a', 'g', 'i'})

    Q0 = Query('Q0', {R0, R1, R3, R4} ,{'a', 'f'})
    Q1 = Query('Q1', {R1, R3} ,{'a', 'd', 'g', 'i'})
    Q2 = Query('Q2', {R0, R1, R2, R3} ,{'a', 'e', 'f', 'g', 'h', 'i', 'j'})

    test_queries([Q0,Q1,Q2])


def example_23():
    R0 = Relation("R0", {'a', 'd'})
    R1 = Relation("R1", {'a', 'b', 'd', 'e'})
    R2 = Relation("R2", {'a', 'e'})

    Q0 = Query('Q0', {R0, R1, R2}, set())
    Q1 = Query('Q1', {R0, R2}, {'a', 'e'})
    Q2 = Query('Q2', {R0, R1, R2}, {'b'})


    test_queries([Q0,Q1,Q2])


def example_24():
    R0 = Relation("R0", {'a', 'b','d'}, index=0)
    R1 = Relation("R1", {'c', 'e','g', 'j'}, index=1)
    R2 = Relation("R2", { 'e','g', 'l'}, index=2)
    R3 = Relation("R3", { 'e','f'}, index=3)
    R4 = Relation("R4", { 'c','d','g', 'h', 'k'}, index=4)
    R5 = Relation("R5", { 'd','e', 'f', 'i'}, index=5)

    Q0 = Query("Q0", {R0, R4, R5 }, {'a','b','c','d','e','f','g','h','k'})
    Q1 = Query("Q1", {R0, R1, R4 }, {'b', 'c'})
    Q2 = Query("Q2", {R0, R1, R2,R3, R4, R5 }, set())

    test_queries([Q0,Q1,Q2])

def example_25():
    R0 = Relation("R0", {'c', 'f'})
    R1 = Relation("R1", {'a', 'b', 'c', 'd', 'f'})
    R2 = Relation("R2", {'a','b', 'd'})
    R3 = Relation("R3", {'a','e'})

    Q0 = Query('Q0', {R0, R1}, {'a','c','f'})
    Q1 = Query('Q1', {R1, R2}, {'a', 'b', 'c','d','f'})
    Q2 = Query('Q2', {R0, R1, R2, R3}, {'a','c','d','e'})

    test_queries([Q0,Q1,Q2])

def example_26():
    R0 = Relation('R0', {'a', 'b', 'c','d','e'}, index=0)
    R1 = Relation('R1', {'a', 'd'}, index=1)
    R2 = Relation('R2', {'a','b','c', 'd'}, index=2)
    R3 = Relation('R3', {'a','b','c', 'd'}, index=3)
    R4 = Relation('R4', {'c', 'd'}, index=4)

    Q0 = Query('Q0', {R1, R2, R3, R4}, {'d'})
    Q1 = Query('Q1', {R2, R4}, {'a','b','c', 'd'})
    Q2 = Query('Q2', {R0, R1, R2, R3, R4}, set())

    test_queries([Q0,Q1,Q2])

def example_27():
    R0 = Relation('R0', {'a', 'b', 'c', 'e','f'}, index=0)
    R1 = Relation('R1', { 'd', 'e'}, index=1)
    R2 = Relation('R2', { 'a', 'c', 'e','f'}, index=2)

    Q0 = Query('Q0', {R1, R2}, set())
    Q1 = Query('Q1', {R0, R1, R2}, {'a', 'b', 'd', 'f'})
    Q2 = Query('Q2', {R0, R1, R2}, {'a'})

    test_queries([Q0,Q1,Q2])

def example_28():
    R0 = Relation('R0', {'b', 'c'}, index=0)
    R1 = Relation('R1', {'a', 'c'}, index=1)
    R2 = Relation('R2', {'a','b', 'c'}, index=2)
    R3 = Relation('R3', {'a','b', 'c'}, index=3)
    R4 = Relation('R4', {'a','b', 'c'}, index=4)
    R5 = Relation('R5', {'a','b', 'c'}, index=5)
    R6 = Relation('R6', {'a','b', 'c'}, index=6)
    R7 = Relation('R7', {'a', 'c'}, index=7)

    Q0 = Query('Q0', {R5, R7}, {'a', 'b', 'c'})
    Q1 = Query('Q1', {R0, R1, R2, R3, R4, R5, R6, R7}, { 'b', 'c'})
    Q2 = Query('Q2', {R1, R2}, {'a', 'b', 'c'})

    test_queries([Q0,Q1,Q2])

def example_29():
    R0 = Relation('R0', {'a', 'b', 'd'}, index=0)
    R1 = Relation('R1', {'a', 'b','c', 'd', 'e'}, index=1)
    R2 = Relation('R2', {'a', 'b','d', 'e'}, index=2)

    Q0 = Query('Q0', {R0, R1, R2}, {'a', 'b','d'})
    Q1 = Query('Q1', {R0, R1, R2}, {'a', 'b','c'})
    Q2 = Query('Q2', {R0, R1, R2}, {'a', 'b','d','e'})

    test_queries([Q0,Q1,Q2])

# example_0()
# example_1()
# example_2()
# example_3()
# example_4()
# example_5()
example_6(30000, 89, _print=False, _break=True)
# example_7()
# example_8()
# example_9()
# example_10()
# example_11()
# example_12()
# example_13()
# example_15()
# example_16(30000, 99,)
# example_17()
# example_18()
# example_19()
# example_20()
# example_21()
# example_22()
# example_23()
# example_24()
# example_25()
# example_26()
# example_27()
# example_28()
# example_29()


print("done")