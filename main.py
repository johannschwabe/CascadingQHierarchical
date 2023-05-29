import random

from graphviz import Digraph
from ordered_set import OrderedSet

from JoinOrderNode import JoinOrderNode
from M3Generator import M3Generator
from M3MultiQueryGenerator import M3MultiQueryGenerator
from QueryGenerator import generate
from Relation import Relation
from Query import Query, QuerySet
from cascade import run

random.seed(22)

def example_0():
    R1_1 = Relation("R1", OrderedSet(["x", "y"]))
    R2_1 = Relation("R2", OrderedSet(["y", "z"]))
    R3 = Relation("R3", OrderedSet(["z", "w"]))
    Q1 = Query("Q1", OrderedSet([R1_1, R2_1]), OrderedSet(['y', 'z']))
    Q2 = Query("Q2", OrderedSet([R1_1, R2_1, R3]), OrderedSet(['y', 'z', 'w']))

    res = run([Q1, Q2])
    res.graph_viz("ex0")
    multigenerator = M3MultiQueryGenerator(
        'simple',
        'RingFactorizedRelation',
        'example_0',
        res,
        {'a': 'int', 's': 'int', 'd': 'int', 'w': 'int', 'x': 'int', 'y': 'int', 'z': 'int'},
    )
    multigenerator.generate(batch=True)
    return res


def example_1():
    R1_1 = Relation("R1", OrderedSet(["a", "b"]))
    R2_1 = Relation("R2", OrderedSet(["b", "c"]))
    R3_1 = Relation("R3", OrderedSet(["c", "d"]))
    R4_1 = Relation("R4", OrderedSet(["b", "e"]))

    Q1 = Query("Q1", OrderedSet([R1_1, R2_1]), OrderedSet(['a', 'b', 'c']))
    Q2 = Query("Q2", OrderedSet([R1_1, R2_1, R3_1]), OrderedSet(['a', 'b', 'c', 'd']))
    Q3 = Query("Q3", OrderedSet([R1_1, R2_1, R3_1, R4_1]), OrderedSet(['a', 'b', 'c', 'd', 'e']))
    res = run([Q1, Q2, Q3])
    multigenerator = M3MultiQueryGenerator(
        'simple',
        'RingFactorizedRelation',
        'example_1',
        res,
        {'a': 'int', 'b': 'int', 'c': 'int', 'd': 'int', 'e': 'int'},
    )
    multigenerator.generate(batch=True)

    res.graph_viz("ex1")
    return res


def example_2():
    R1 = Relation("R1", OrderedSet(["x", "y"]))
    R2 = Relation("R2", OrderedSet(["y", "z"]))
    R3 = Relation("R3", OrderedSet(["z", "w"]))
    R4 = Relation("R4", OrderedSet(["w", "q"]))
    R5 = Relation("R5", OrderedSet(["z"]))

    Q1 = Query("Q1", OrderedSet([R1, R2]), OrderedSet(['x', 'y', 'z']))
    Q2 = Query("Q2", OrderedSet([R3, R4]), OrderedSet(['z', 'w', 'q']))
    Q3 = Query("Q3", OrderedSet([R1, R2, R3, R4, R5]), OrderedSet(['x', 'y', 'z', 'w', 'q']))
    res = run([Q1, Q2, Q3])
    res.graph_viz(2)
    multigenerator = M3MultiQueryGenerator(
        'simple',
        'RingFactorizedRelation',
        'example_2',
        res,
        {'x': 'int', 'y': 'int', 'z': 'int', 'w': 'int', 'q': 'int'},
    )
    multigenerator.generate(batch=True)

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

    Q1 = Query("Q1", {R2_1, R3_1}, {'y', 'z', 'w'})
    Q2 = Query("Q2", {R4_2, R3_2}, {'a', 'g', 'y'})
    Q3 = Query("Q3", {R1_3, R2_3, R3_3}, {'1', '2', '3', '4', })
    Q4 = Query("Q4", {R3_4, R4_4, R5_4}, {'t', 'z', 'u', 'i'})
    Q5 = Query("Q5", {R1_5, R2_5, R3_5, R4_5, R5_5}, {'a', 's', 'd', 'f', 'g', 'h'})
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

    Q1 = Query("Q1", {R1_1, R2_1, R3_1}, {'x', 'y', 'z', 'w'})
    Q2 = Query("Q2", {R1_2, R2_2, R3_2, R4_2}, {'1', '2', '3'})
    Q3 = Query("Q3", {R2_3, R1_3}, {'z', 'u', 'i'})
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

    Q1 = Query("Q1", {R0, R1, R2, R3, R5, R6}, {"x", "y", "a"})
    graph = Digraph("View Example")
    Q1.variable_order.graph_viz(graph, "-")
    graph.view()
    Q2 = Query("Q2", {R1, R2, R3, R5, R6, R7}, {"x", "y", "a"})
    res = run([Q1, Q2])
    res.graph_viz()
    # Q1.variable_order.generate_views(Q1)
    # qs = QuerySet()
    # qs.add(Q1)
    # qs.graph_viz()
    return


def example_6(nr_attempts: int, seed_base=23445, _print=False, _break=False):
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


def example_30():
    House = Relation('House',
                     ['postcode',
                      'livingarea',
                      'price',
                      'nbbedrooms',
                      'nbbathrooms',
                      'kitchensize',
                      'house',
                      'flat',
                      'unknown',
                      'garden',
                      'parking'])
    Shop = Relation('Shop', ['postcode',
                             'openinghoursshop',
                             'pricerangeshop',
                             'sainsburys',
                             'tesco',
                             'ms'])
    Institution = Relation('Institution', ['postcode',
                                           'typeeducation',
                                           'sizeinstitution'])
    Restaurant = Relation('Restaurant', ['postcode',
                                         'openinghoursrest',
                                         'pricerangerest'])
    Demographics = Relation('Demographics',
                            ['postcode',
                             'averagesalary',
                             'crimesperyear',
                             'unemployment',
                             'nbhospitals'])
    Transport = Relation('Transport', ['postcode',
                                       'nbbuslines',
                                       'nbtrainstations',
                                       'distancecitycentre'])
    Q0 = Query('Q0', {House, Shop, Institution, Restaurant, Demographics, Transport}, set())
    M3Gen = M3Generator('/Users/johannschwabe/Documents/git/FIVM/examples/queries/housing/housing.txt', 'housing',
                        'RingFactorizedRelation')
    join_order_node_root = JoinOrderNode.generate_recursion(Q0.variable_order, Q0)
    QS = QuerySet({Q0})
    QS.graph_viz(1)
    M3Gen.generate(join_order_node_root)


def example_31():
    R = Relation('R', ['A', 'B'])
    S = Relation('S', ['A', 'C', 'E', 'extra'])
    T = Relation('T', ['A', 'C'])
    Q0 = Query('Q0', {R, S, T}, {'A', 'B', 'C'})
    M3Gen = M3Generator('/Users/johannschwabe/Documents/git/FIVM/examples/queries/simple/rst.txt', 'simple',
                        'RingFactorizedRelation', Q0)
    join_order_node_root = JoinOrderNode.generate_recursion(Q0.variable_order, Q0)
    QS = QuerySet({Q0})
    QS.graph_viz(1)
    M3Gen.generate(join_order_node_root)


def example_32():
    R = Relation('R', ['A', 'B'])
    S = Relation('S', ['A', 'C', 'E', 'extra'])
    T = Relation('T', ['A', 'C'])
    U = Relation('U', ['A', 'C', 'E'])
    Q0 = Query('Q0', {R, S, T, U}, {'A', 'B', 'C'})
    M3Gen = M3Generator('/Users/johannschwabe/Documents/git/FIVM/examples/queries/simple/rst2.txt', 'simple',
                        'RingFactorizedRelation', Q0)
    join_order_node_root = JoinOrderNode.generate_recursion(Q0.variable_order, Q0)
    QS = QuerySet({Q0})
    QS.graph_viz(1)
    M3Gen.generate(join_order_node_root, True)



print("done")
