import random

from graphviz import Digraph

from JoinOrderNode import JoinOrderNode
from M3Generator import M3Generator
from QueryGenerator import generate
from Relation import Relation
from Query import Query, QuerySet
from cascade import run

random.seed(22)


def example_0():
    R1_1 = Relation("R1", ["x", "y"])
    R1_2 = Relation("R1", ["a", "s"])
    R2_1 = Relation("R2", ["y", "z"])
    R2_2 = Relation("R2", ["s", "d"])
    R3 = Relation("R3", ["d", "w"])
    Q1 = Query("Q1", {R1_1, R2_1}, {'y','z'})
    Q2 = Query("Q2", {R1_2, R2_2, R3}, { 's','d', 'w'})

    res = run([Q1, Q2])
    # res = greedy([Q2, Q1])
    # res = backward_search([Q2, Q1])
    res.graph_viz("ex0")
    return res

def example_1():
    R1_1 = Relation("R1", ["a", "b"])
    R2_1 = Relation("R2", ["b", "c"])
    R3_1 = Relation("R3", ["c", "d"])
    R4_1 = Relation("R4", ["b", "e"])

    R1_2 = Relation("R1", ["1", "2"])
    R2_2 = Relation("R2", ["2", "3"])
    R3_2 = Relation("R3", ["3", "4"])
    R4_2 = Relation("R4", ["4", "5"])

    R1_3 = Relation("R1", ["q", "w"])
    R2_3 = Relation("R2", ["w", "e"])
    R3_3 = Relation("R3", ["e", "r"])
    R4_3 = Relation("R4", ["r", "t"])

    Q1 = Query("Q1", {R1_1, R2_1}, {'a', 'b', 'c'})
    Q2 = Query("Q2", {R1_2, R2_2, R3_2}, {'1', '2', '3', '4'})
    Q3 = Query("Q3", {R1_3, R2_3, R3_3, R4_3}, {'q', 'w','e','r', 't'})
    # Q3 = Query("Q3", {R1, R2, R3, R4}, {'a', 'b', 'c', 'd', 'e'})
    res = run([Q1, Q2, Q3])
    # res = greedy([Q1, Q2, Q3])
    # QS = QuerySet({Q1, Q2, Q3})
    # QS.graph_viz()
    # res = backward_search([Q2, Q1, Q3])
    res.graph_viz("ex1")
    return res

def example_2():
    R1_1 = Relation("R1", ["x", "y"])
    R2_1 = Relation("R2", ["y", "z"])
    R3_1 = Relation("R3", ["z", "w"])
    R4_1 = Relation("R4", ["w", "q"])

    R1_2 = Relation("R1", ["a", "b"])
    R2_2 = Relation("R2", ["b", "c"])
    R3_2 = Relation("R3", ["c", "d"])
    R4_2 = Relation("R4", ["d", "e"])

    R1_3 = Relation("R1", ["1", "2"])
    R2_3 = Relation("R2", ["2", "3"])
    R3_3 = Relation("R3", ["3", "4"])
    R4_3 = Relation("R4", ["4", "5"])

    Q1 = Query("Q1", {R1_1, R2_1},{'x', 'y', 'z'})
    Q2 = Query("Q2", {R3_2, R4_2},{'c', 'd', 'e'})
    Q3 = Query("Q3", {R1_3, R2_3, R3_3, R4_3},{'1', '2', '3', '4', '5'})
    res = run([Q1, Q2, Q3])
    res.graph_viz()

    return res
def example_3():
    R2_1 = Relation("R2", ["y", "z"])
    R3_1 = Relation("R3", ["z", "w"])

    R3_2 = Relation("R3", ["a", "g"])
    R4_2 = Relation("R4", ["g", "y"])

    R1_3 = Relation("R1", ["1", "2"])
    R2_3 = Relation("R2", ["2", "3"])
    R3_3 = Relation("R3", ["3", "4"])

    R3_4 = Relation("R3", ["t", "z"])
    R4_4 = Relation("R4", ["z", "u"])
    R5_4 = Relation("R5", ["u", "i"])

    R1_5 = Relation("R1", ["a", "s"])
    R2_5 = Relation("R2", ["s", "d"])
    R3_5 = Relation("R3", ["d", "f"])
    R4_5 = Relation("R4", ["f", "g"])
    R5_5 = Relation("R5", ["g", "h"])

    Q1 = Query("Q1", {R2_1, R3_1},{'y', 'z', 'w'})
    Q2 = Query("Q2", {R4_2, R3_2},{'a', 'g', 'y'})
    Q3 = Query("Q3", {R1_3, R2_3, R3_3},{'1', '2', '3', '4',})
    Q4 = Query("Q4", {R3_4, R4_4, R5_4},{'t', 'z', 'u', 'i'})
    Q5 = Query("Q5", {R1_5, R2_5,R3_5, R4_5, R5_5},{'a', 's', 'd', 'f', 'g', 'h'})
    res = run([Q1, Q2, Q3, Q4, Q5])
    res.graph_viz()

    return res

def example_4():
    R1_1 = Relation("R1", ["x", "y"])
    R2_1 = Relation("R2", ["y", "z"])
    R3_1 = Relation("R3", ["z", "w"])

    R1_2 = Relation("R1", ["1", "2"])
    R2_2 = Relation("R2", ["2", "3"])
    R3_2 = Relation("R3", ["3", "4"])
    R4_2 = Relation("R4", ["4", "5"])

    R1_3 = Relation("R1", ["z", "u"])
    R2_3 = Relation("R2", ["u", "i"])


    Q1 = Query("Q1", {R1_1, R2_1, R3_1},{'x', 'y', 'z', 'w'})
    Q2 = Query("Q2", {R1_2, R2_2, R3_2, R4_2},{'1', '2', '3'})
    Q3 = Query("Q3", {R2_3, R1_3},{'z', 'u', 'i'})
    res = run([Q1, Q2, Q3])
    res.graph_viz()

    return res

# example_3()
def example_5():
    R0 = Relation("R0", ["x"])
    R1 = Relation("R1", ["x", "y"])
    R2 = Relation("R2", ["x", "y"])
    R3 = Relation("R3", ["x", "y", "a"])
    # R4 = Relation("R4", {"x", "y", "b"},4)
    R5 = Relation("R5", ["x", "y", "a", "c"])
    R6 = Relation("R6", ["x", "y", "b", "d", "e"])
    R7 = Relation("R7", ["f", "b"])

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
    Census = Relation("Census", [
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

    ])
    Item = Relation("Item", [
        "Ksn",
        "SubCategory",
        "Category"
        "CategoryCluster",
        "Prize"
    ])
    Inventory = Relation("Inventory", [
        "InventoryUnits",
        "Ksn",
        "DateId",
        "Locn"
    ])
    Weather = Relation("Weather", [
        "DateId",
        "Locn",
        "MaxTemp",
        "Rain",
    ])
    Location = Relation("Location", [
        "Locn",
        "Zip",
        "SellAreaSqFt",

    ])
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

    # Q1 = Query("Q1", {Inventory, Item, Weather, Location}, {"Ksn","Category", "Zip", "Rain"})          # Select Ksn, Category, Zip, Rain, Avg(Price)
    # Q2 = Query("Q2", {Inventory, Weather, Item}, {"Locn", "DateId", "Ksn", "Category"})
    # Q3 = Query("Q3", {Inventory, Weather, Location}, {"Ksn","Locn", "DateId", "MaxTemp", "Zip"})
    Q0 = Query('Q0', {Location, Census, Weather, Inventory},set())
    QS = QuerySet({Q0})
    QS.graph_viz("Retailer")
    # print(Q1.is_q_hierarchical())
    # print(Q2.is_q_hierarchical())
    # print(Q3.is_q_hierarchical())
    # res = run({Q1, Q3})
    # res = run([Q1, Q2, Q3])
    # if res:
    #     res.pop().graph_viz()
    # else:
    #     print("no reduction")

def example_8():
    for i in range(1000,2000):
        seed_base =random.randint(16029,50000)
        print(seed_base)
        example_6(1, seed_base)

def example_9():
    R0 = Relation("R0", ["a", "c"])
    R1 = Relation("R1", ["a", "b", "c"])
    R2 = Relation("R2", ["a", "b", "c"])
    R3 = Relation("R3", ["a", "b", "c"])
    R4 = Relation("R4", ["a", "b", "c"])
    R5 = Relation("R5", ["a", "b", "c"])
    R6 = Relation("R6", ["a", "b", "c"])
    R7 = Relation("R7", ["a", "b", "c"])

    Q0 = Query("Q0", {R0, R1, R2, R4, R5, R6, R7}, set())
    Q1 = Query("Q1", {R0, R1, R2,R3, R4, R5, R6}, {"a", "b", "c"})
    Q2 = Query("Q2", {R0, R1, R2,R3, R4, R5, R6, R7}, {"b", "c"})
    Q3 = Query("Q3", {R0, R1, R2, R3, R5, R6,}, {"a"})
    Q4 = Query("Q4", {R0, R4, R6}, {"a"})
    res = run([Q0, Q1, Q2, Q3, Q4])
    res.graph_viz("??")

def example_10():
    R0 = Relation("R0", ["a", "c"])
    R1 = Relation("R1", ["a", "b", "c"])
    Q0 = Query("Q0", {R0, R1}, {"b", "c"})
    res = run([Q0])
    res.graph_viz("sdf")

def example_11():
    R0 = Relation("R0", ["a", "b", "c", "d", "e"])
    R1 = Relation("R1", ["a", "b", "c", "d", "e"])
    R2 = Relation("R2", ["a", "b", "c", "d", "e"])
    R3 = Relation("R3", ["b", "c", "d", "e"])
    R4 = Relation("R4", ["a", "c", "d", "e"])
    R5 = Relation("R5", ["a", "b", "c", "d", "e"])
    R6 = Relation("R6", ["a", "b", "c", "d", "e"])
    R7 = Relation("R7", ["a", "b", "c", "d", "e"])
    R8 = Relation("R8", ["a", "b", "c", "d", "e"])
    R9 = Relation("R9", ["a", "b", "c", "d", "e"])
    R10 = Relation("R10", ["a", "b", "c", "d", "e"])

    Q0 = Query("Q0", {R1, R3, R4, R7}, {'d', 'e'})
    Q1 = Query("Q1", {R1, R2, R3, R7}, {'b'})
    Q2 = Query("Q2", {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10}, set())

    res_1 = run([Q0, Q1, Q2])
    if res_1:
        res_1.graph_viz(1)
    else:
        print("res_1 failed")

    R0 = Relation("R0", ["a", "b", "c", "d", "e"])
    R1 = Relation("R1", ["a", "b", "c", "d", "e"])
    R2 = Relation("R2", ["a", "b", "c", "d", "e"])
    R3 = Relation("R3", ["b", "c", "d", "e"])
    R4 = Relation("R4", ["a", "c", "d", "e"])
    R5 = Relation("R5", ["a", "b", "c", "d", "e"])
    R6 = Relation("R6", ["a", "b", "c", "d", "e"])
    R7 = Relation("R7", ["a", "b", "c", "d", "e"])
    R8 = Relation("R8", ["a", "b", "c", "d", "e"])
    R9 = Relation("R9", ["a", "b", "c", "d", "e"])
    R10 = Relation("R10", ["a", "b", "c", "d", "e"])

    Q0 = Query("Q0", {R1, R3, R4, R7}, {'d', 'e'})
    Q1 = Query("Q1", {R1, R2, R3, R7}, {'b'})
    Q2 = Query("Q2", {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10}, set())
    res_2 = run([Q2, Q1, Q0])
    if res_2:
        res_2.graph_viz(2)
    else:
        print("res_2 failed")

def example_12():
    R0 = Relation("R0", ['a', 'b', 'c'])
    R1 = Relation("R1", ['a', 'b', 'c'])
    R2 = Relation("R2", ['a', 'b', 'c'])
    R3 = Relation("R3", ['a', 'b', 'c'])
    R4 = Relation("R4", ['a', 'b', 'c'])
    R5 = Relation("R5", ['a', 'b', 'c'])
    R6 = Relation("R6", ['a', 'b', 'c'])
    R7 = Relation("R7", ['a', 'b', 'c'])
    R8 = Relation("R8", ['a', 'b', 'c'])
    R9 = Relation("R9", ['a', 'b', 'c'])
    R10 = Relation("R10", ['a', 'b', 'c'])
    R11 = Relation("R11", ['a', 'b', 'c'])
    R12 = Relation("R12", ['a', 'b'])
    R13 = Relation("R13", ['a', 'b', 'c'])
    R14 = Relation("R14", ['a', 'b', 'c'])


    Q0 = Query("Q0", {R0, R1, R10, R11, R12, R13, R14, R2, R4, R5, R6, R7, R8, R9}, {'a', 'b', 'c'})
    # Q1 = Query("Q1", {R0, R1, R11, R6, R7, R8, R9}, set())
    Q2 = Query("Q2", {R0, R10, R12, R13, R2, R3, R6, R7, R8}, {'b', 'c'})

    queries = [Q0, Q2]
    run_1_queries = [q.clean_copy() for q in queries]
    res_run_1 = run(run_1_queries)
    if res_run_1:
        res_run_1.graph_viz("success")

def example_13():
    R1 = Relation('R1', ['a', 'b'])
    R2 = Relation('R2', ['c', 'b'])
    R3 = Relation('R3', ['a', 'b', 'd', 'e'])
    Q0 = Query('Q0', {R1, R2, R3}, {'a', 'b', 'c'})
    graph = Digraph()
    Q0.variable_order.graph_viz(graph)
    graph.view()
    QS = QuerySet({Q0})
    QS.graph_viz("View Tree")

def example_14():
    R1 = Relation('R1', ['a', 'b', 'c'])
    R2 = Relation('R2', ['a', 'b', 'd'])
    R3 = Relation('R3', ['a', 'e'])
    Q1 = Query('Q1', {R1, R2, R3}, {'a', 'b', 'c', 'd', 'e'})
    graph = Digraph()
    Q1.variable_order.graph_viz(graph)
    graph.view()
    QS = QuerySet({Q1})
    QS.graph_viz("View Tree")

def example_15():
    R1 = Relation('R1', ['x', 'y'])
    R2 = Relation('R2', ['x', 'y'])
    R3 = Relation('R3', ['x', 'y', 'a'])
    R4 = Relation('R4', ['x', 'y', 'b'])
    R5 = Relation('R5', ['x', 'y', 'a', 'c'])
    R6 = Relation('R6', ['x', 'y', 'b', 'd'])

    Q1 = Query('Q1', {R1, R2, R3, R4, R5, R6,}, {'x', 'y','a', 'b', 'c', 'd'})
    graph = Digraph()
    Q1.variable_order.graph_viz(graph)
    graph.view()
    # QS = QuerySet({Q1})
    # QS.graph_viz("View Tree")

def example_16():
    R1 = Relation('R1', ['x','y','z','w'])
    R2 = Relation('R2', ['x','y','z','a'])
    R3 = Relation('R3', ['x','y','z'])

    Q1 = Query('Q1', {R1, R2, R3}, {'x','y'})
    QuerySet({Q1}).graph_viz(2)

def example_30():
    House = Relation('House',
                     ['postcode', 'livingarea', 'price', 'nbbedrooms', 'nbbathrooms', 'kitchensize', 'house', 'flat',
                      'unknown', 'garden', 'parking'])
    Shop = Relation('Shop', ['postcode', 'openinghoursshop', 'pricerangeshop', 'sainsburys', 'tesco', 'ms'])
    Institution = Relation('Institution', ['postcode', 'typeeducation', 'sizeinstitution'])
    Restaurant = Relation('Restaurant', ['postcode', 'openinghoursrest', 'pricerangerest'])
    Demographics = Relation('Demographics',
                            ['postcode', 'averagesalary', 'crimesperyear', 'unemployment', 'nbhospitals'])
    Transport = Relation('Transport', ['postcode', 'nbbuslines', 'nbtrainstations', 'distancecitycentre'])
    Q0 = Query('Q0', {House, Shop, Institution, Restaurant, Demographics,Transport}, set())
    M3Gen = M3Generator('/Users/johannschwabe/Documents/git/FIVM/examples/queries/housing/housing.txt', 'housing', 'RingFactorizedRelation')
    join_order_node_root = JoinOrderNode.generate(Q0.variable_order,Q0)
    QS = QuerySet({Q0})
    QS.graph_viz(1)
    M3Gen.generate(join_order_node_root)

def example_31():
    R = Relation('R', ['A', 'B'])
    S = Relation('S', ['A', 'C', 'E', 'extra'])
    T = Relation('T', ['A', 'C'])
    Q0 = Query('Q0', {R, S, T}, {'A', 'B', 'C'})
    M3Gen = M3Generator('/Users/johannschwabe/Documents/git/FIVM/examples/queries/simple/rst.txt', 'simple', 'RingFactorizedRelation', Q0)
    join_order_node_root = JoinOrderNode.generate(Q0.variable_order, Q0)
    QS = QuerySet({Q0})
    QS.graph_viz(1)
    M3Gen.generate(join_order_node_root)

# example_0()
# example_1()
# example_2()
# example_3()
# example_4()
# example_5()
# example_6(30000, 89, _print=True, _break=True)
# example_7()
# example_8()
# example_9()
# example_10()
# example_11()
# example_12()
# example_13()
# example_15()
# example_16()
# example_30()
example_31()


print("done")