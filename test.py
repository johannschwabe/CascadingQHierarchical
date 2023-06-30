from graphviz import Digraph, Graph
from ordered_set import OrderedSet

from JoinOrderNode import JoinOrderNode
from Query import Query, QuerySet
from Relation import Relation
from VariableOrder import VariableOrderNode
from tpch import Part, PartSupp, LineItem, Orders, Supplier
from retailer import Inventory, Item, Weather, Location, Census

def tpch_1():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, LineItem, Orders]),
                   OrderedSet(["P_NAME", "O_TOTALPRICE", "PS_AVAILQTY", "L_QUANTITY", "PARTKEY", "SUPPKEY", "ORDERKEY"]))

    o1 = JoinOrderNode(Q1,"orders", OrderedSet([Orders]), OrderedSet(["ORDERKEY"]),OrderedSet(["O_TOTALPRICE","O_ORDERDATE","O_ORDERSTATUS","O_CLERK","O_SHIPPRIORITY","O_COMMENT","O_ORDERPRIORITY","CUSTKEY"]))
    p1 = JoinOrderNode(Q1,"part", OrderedSet([Part]), OrderedSet(["PARTKEY"]),OrderedSet(["P_NAME","P_MFGR","P_BRAND","P_TYPE","P_SIZE","P_CONTAINER","P_RETAILPRICE","P_COMMENT"]))
    ps1 = JoinOrderNode(Q1, "partsupp", OrderedSet([PartSupp]), OrderedSet(["PARTKEY", "SUPPKEY"]),OrderedSet(["PS_AVAILQTY","PS_SUPPLYCOST","PS_COMMENT"]))
    l1 = JoinOrderNode(Q1, "lineitem", OrderedSet([LineItem]), OrderedSet(["ORDERKEY", "PARTKEY", "SUPPKEY"]),OrderedSet(["L_LINENUMBER","L_QUANTITY","L_EXTENDEDPRICE","L_DISCOUNT","L_TAX","L_RETURNFLAG","L_LINESTATUS","L_SHIPDATE","L_COMMITDATE","L_RECEIPTDATE","L_SHIPINSTRUCT","L_SHIPMODE","L_COMMENT"]))
    lps1 = JoinOrderNode(Q1, "lineitempartsupp", OrderedSet([]), OrderedSet(["PARTKEY", "ORDERKEY"]),OrderedSet(["SUPPKEY"]))
    lpsp1 = JoinOrderNode(Q1, "lineitempartsupppart", OrderedSet([]), OrderedSet(["ORDERKEY"]),OrderedSet(["PARTKEY"]))
    root = JoinOrderNode(Q1,"partpartsupplineitemorders", OrderedSet(), OrderedSet(),OrderedSet(["ORDERKEY"]))

    root.children = {o1, lpsp1}
    o1.parent = root
    lpsp1.parent = root
    lpsp1.children = {lps1, p1}
    lps1.parent = lpsp1
    p1.parent = lpsp1
    lps1.children = {l1, ps1}
    l1.parent = lps1
    ps1.parent = lps1

    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    root.viz(graph,Q1,{},minimized=True)
    graph.view("FIVM_tpch_1")


def tpch_1Q1b():
    Q1 = Query("Q1", OrderedSet([Part, PartSupp, LineItem, Orders]),
                   OrderedSet(["p_name", "o_totalprice", "ps_availqty", "l_quantity", "partkey", "suppkey", "orderkey"]))

    o1 = JoinOrderNode(Q1,"O", OrderedSet([Orders]), OrderedSet(["orderkey"]),OrderedSet(["o_totalprice","..."]))
    p1 = JoinOrderNode(Q1,"P", OrderedSet([Part]), OrderedSet(["partkey"]),OrderedSet(["p_name","..."]))
    ps1 = JoinOrderNode(Q1, "Ps", OrderedSet([PartSupp]), OrderedSet(["partkey", "suppkey"]),OrderedSet(["ps_availqty","..."]))
    l1 = JoinOrderNode(Q1, "L", OrderedSet([LineItem]), OrderedSet(["orderkey", "partkey", "suppkey"]),OrderedSet(["l_quantity","..."]))
    lo1 = JoinOrderNode(Q1, "LO", OrderedSet([]), OrderedSet(["partkey", "suppkey"]),OrderedSet(["orderkey"]))
    lops1 = JoinOrderNode(Q1, "LOPs", OrderedSet([]), OrderedSet(["partkey"]),OrderedSet(["suppkey"]))
    lopsp1 = JoinOrderNode(Q1, "LOPsP", OrderedSet([]), OrderedSet(),OrderedSet(["partkey"]))

    lopsp1.children = {lops1, p1}
    lops1.parent = lopsp1
    p1.parent = lopsp1
    lops1.children = {lo1, ps1}
    lo1.parent = lops1
    ps1.parent = lops1
    lo1.children = {l1, o1}
    l1.parent = lo1
    o1.parent = lo1

    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    lopsp1.viz(graph,Q1,{},minimized=True)
    graph.view("FIVM_tpch_1Q1b")

def retailer_1Q1a():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Weather, Location]), OrderedSet(["Locn", "DateId","Ksn","Zip","Category","Rain"]))
    L1 = JoinOrderNode(Q1, "Location", OrderedSet([Location]), OrderedSet(["Locn"]),OrderedSet(["Zip", "RgnCd", "ClimbZnNbr","TotalAreaSqFt","SellAreaSqFt","AvgHigh","SuperTargetDistance","SuperTargetDriveTime","TargetDistance","TargetDriveTime","WalmartDistance","WalmartDriveTime","WalmartSuperCenterDistance","WalmartSuperCenterDriveTime"]))
    W1 = JoinOrderNode(Q1, "Weather", OrderedSet([Weather]), OrderedSet(["Locn","DateId"]),OrderedSet(["MaxTemp","MinTemp","Rain","Snow","Thunder","MeanWind","Thunder"]))
    IN1 = JoinOrderNode(Q1, "Inventory", OrderedSet([Inventory]), OrderedSet(["Ksn","Locn","DateId"]),OrderedSet(["InventoryUnits"]))
    IT1 = JoinOrderNode(Q1, "Item", OrderedSet([Item]), OrderedSet(["Ksn"]),OrderedSet(["SubCategory", "Category","CategoryCluster","Prize"]))
    INIT1 = JoinOrderNode(Q1, "InventoryItem", OrderedSet([]), OrderedSet(["Locn", "DateId"]),OrderedSet(["Ksn"]))
    INITW1 = JoinOrderNode(Q1, "InventoryItemWeather", OrderedSet([]), OrderedSet(["Locn"]),OrderedSet(["DateId"]))
    INITWL1 = JoinOrderNode(Q1, "InventoryItemWeatherLocation", OrderedSet([]), OrderedSet(),OrderedSet(["Locn"]))

    INITWL1.children = {L1, INITW1}
    L1.parent = INITWL1
    INITW1.parent = INITWL1
    INITW1.children = {W1, INIT1}
    W1.parent = INITW1
    INIT1.parent = INITW1
    INIT1.children = {IN1, IT1}
    IN1.parent = INIT1
    IT1.parent = INIT1

    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    INITWL1.viz(graph,Q1,{},minimized=True)
    graph.view("FIVM_retailer_1_Q1a")

def retailer_1Q1b():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Weather, Location]), OrderedSet(["Locn", "DateId","Ksn","Zip","Category","Rain"]))
    L1 = JoinOrderNode(Q1, "Location", OrderedSet([Location]), OrderedSet(["Locn"]),OrderedSet(["Zip", "RgnCd", "ClimbZnNbr","TotalAreaSqFt","SellAreaSqFt","AvgHigh","SuperTargetDistance","SuperTargetDriveTime","TargetDistance","TargetDriveTime","WalmartDistance","WalmartDriveTime","WalmartSuperCenterDistance","WalmartSuperCenterDriveTime"]))
    W1 = JoinOrderNode(Q1, "Weather", OrderedSet([Weather]), OrderedSet(["Locn","DateId"]),OrderedSet(["MaxTemp","MinTemp","Rain","Snow","Thunder","MeanWind","Thunder"]))
    IN1 = JoinOrderNode(Q1, "Inventory", OrderedSet([Inventory]), OrderedSet(["Ksn","Locn","DateId"]),OrderedSet(["InventoryUnits"]))
    IT1 = JoinOrderNode(Q1, "Item", OrderedSet([Item]), OrderedSet(["Ksn"]),OrderedSet(["SubCategory", "Category","CategoryCluster","Prize"]))
    INW1 = JoinOrderNode(Q1, "InventoryWeather", OrderedSet([]), OrderedSet(["Locn", "Ksn"]),OrderedSet(["DateId"]))
    INWL1 = JoinOrderNode(Q1, "InventoryWeatherLocation", OrderedSet([]), OrderedSet(["Ksn"]),OrderedSet(["Locn"]))
    INWLI1 = JoinOrderNode(Q1, "InventoryWeatherLocationItem", OrderedSet([]), OrderedSet(),OrderedSet(["Ksn"]))

    INWLI1.children = {INWL1, IT1}
    INWL1.parent = INWLI1
    IT1.parent = INWLI1
    INWL1.children = {INW1, L1}
    INW1.parent = INWL1
    L1.parent = INWL1
    INW1.children = {IN1, W1}
    IN1.parent = INW1
    W1.parent = INW1


    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    INWLI1.viz(graph,Q1,{},minimized=True)
    graph.view("FIVM_retailer_1_Q1b")

def retailer_1Q1c():
    Q2 = Relation("Q2", OrderedSet(["Locn", "DateId","Ksn","Zip","MaxTemp","Rain"]))
    Q1 = Query("Q1", OrderedSet([Q2, Item]), OrderedSet(["Locn", "DateId","Ksn","Zip","Category","Rain"]))

    IT1 = JoinOrderNode(Q1, "Item", OrderedSet([Item]), OrderedSet(["Ksn"]),OrderedSet(["SubCategory", "Category","CategoryCluster","Prize"]))
    Q21 = JoinOrderNode(Q1, "Q2", OrderedSet([Q2]), OrderedSet(["Ksn"]),OrderedSet(["Locn","DateId","Zip","MaxTemp","Rain"]))
    ITQ21 = JoinOrderNode(Q1, "ItemQ2", OrderedSet([]), OrderedSet(),OrderedSet(["Ksn"]))
    ITQ21.children = {IT1, Q21}
    IT1.parent = ITQ21
    Q21.parent = ITQ21
    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    ITQ21.viz(graph,Q1,{}, minimized=True)
    graph.view("FIVM_retailer_1_Q1c")

def retailer_3Q1():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Weather, Location]), OrderedSet(["Locn", "DateId","Ksn","Zip","Category","Rain"]))
    L1 = JoinOrderNode(Q1, "Location", OrderedSet([Location]), OrderedSet(["Locn"]),OrderedSet(["Zip", "RgnCd", "ClimbZnNbr","TotalAreaSqFt","SellAreaSqFt","AvgHigh","SuperTargetDistance","SuperTargetDriveTime","TargetDistance","TargetDriveTime","WalmartDistance","WalmartDriveTime","WalmartSuperCenterDistance","WalmartSuperCenterDriveTime"]))
    W1 = JoinOrderNode(Q1, "Weather", OrderedSet([Weather]), OrderedSet(["Locn","DateId"]),OrderedSet(["MaxTemp","MinTemp","Rain","Snow","Thunder","MeanWind","Thunder"]))
    IN1 = JoinOrderNode(Q1, "Inventory", OrderedSet([Inventory]), OrderedSet(["Ksn","Locn","DateId"]),OrderedSet(["InventoryUnits"]))
    IT1 = JoinOrderNode(Q1, "Item", OrderedSet([Item]), OrderedSet(["Ksn"]),OrderedSet(["SubCategory", "Category","CategoryCluster","Prize"]))
    INIT1 = JoinOrderNode(Q1, "InventoryItem", OrderedSet([]), OrderedSet(["Locn", "DateId"]),OrderedSet(["Ksn"]))
    INITW1 = JoinOrderNode(Q1, "InventoryItemWeather", OrderedSet([]), OrderedSet(["Locn"]),OrderedSet(["DateId"]))
    INITWL1 = JoinOrderNode(Q1, "InventoryWeatherLocationItem", OrderedSet([]), OrderedSet(),OrderedSet(["Locn"]))

    INITWL1.children = {INITW1, L1}
    INITW1.parent = INITWL1
    L1.parent = INITWL1
    INITW1.children = {INIT1, W1}
    INIT1.parent = INITW1
    W1.parent = INITW1
    INIT1.children = {IN1, IT1}
    IN1.parent = INIT1
    IT1.parent = INIT1

    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    INITWL1.viz(graph, Q1, {}, minimized=True)
    graph.view("FIVM_retailer_3_Q1")

def example():
    y = VariableOrderNode("y", set(), OrderedSet([]), None)
    w = VariableOrderNode("w", set(), OrderedSet([]), y)
    x = VariableOrderNode("x", set(), OrderedSet([]), y)
    z = VariableOrderNode("z", set(), OrderedSet([]), w)
    v = VariableOrderNode("v", set(), OrderedSet([]), z)
    y.children = {w, x}
    w.children = {z}
    z.children = {v}

    R1 = Relation("R1", OrderedSet(["x", "y"]))
    R2 = Relation("R2", OrderedSet(["y", "z", "w", "v"]))
    R3 = Relation("R3", OrderedSet(["y", "w"]))
    query = Query("Q", OrderedSet([R1, R2, R3]), OrderedSet(["y", "z"]))
    query2 = Query("Q2", OrderedSet([R1, R2, R3]), OrderedSet(["y", "z"]))

    _y = JoinOrderNode(query, "R1R2R3", OrderedSet([]), OrderedSet([]), OrderedSet(["y"]))
    y_ = JoinOrderNode(query, "R1R2R3", OrderedSet([]), OrderedSet(["y"]), OrderedSet([]), "H")
    y_w = JoinOrderNode(query, "R2R3", OrderedSet([]), OrderedSet(["y"]), OrderedSet(["w"]))
    yw_ = JoinOrderNode(query, "R2R3", OrderedSet([]), OrderedSet(["y", "w"]), OrderedSet([]), "H")
    yw_2 = JoinOrderNode(query, "R3", OrderedSet([R3]), OrderedSet(["y", "w"]), OrderedSet([]))
    yw_z = JoinOrderNode(query, "R2", OrderedSet([]), OrderedSet(["y", "w"]), OrderedSet(["z"]))
    ywz_v = JoinOrderNode(query, "R2", OrderedSet([R2]), OrderedSet(["y", "w", "z"]), OrderedSet(["v"]))
    y_x = JoinOrderNode(query, "R1", OrderedSet([R1]), OrderedSet(["y"]), OrderedSet(["x"]))

    _y.children = {y_}
    y_.parent = _y
    y_.children = {y_x, y_w}
    y_w.parent = y_
    y_x.parent = y_

    y_w.children = {yw_}
    yw_.parent = y_w
    yw_.children = {yw_2, yw_z}
    yw_z.parent = yw_
    yw_z.children = {ywz_v}
    ywz_v.parent = yw_z


    a_y = JoinOrderNode(query2, "R1R2R3", OrderedSet([]), OrderedSet([]), OrderedSet(["y"]))
    ay_w = JoinOrderNode(query2, "R1R2", OrderedSet([]), OrderedSet(["y"]), OrderedSet(["w"]))
    ayw_ = JoinOrderNode(query2, "R3", OrderedSet([R3]), OrderedSet(["y", "w"]), OrderedSet([]))
    ayw_z = JoinOrderNode(query2, "R2", OrderedSet([R2]), OrderedSet(["y", "w"]), OrderedSet(["z", "v"]))
    ay_x = JoinOrderNode(query2, "R1", OrderedSet([R1]), OrderedSet(["y"]), OrderedSet(["x"]))

    a_y.children = {ay_x, ay_w}
    ay_w.parent = a_y
    ay_x.parent = a_y
    ay_w.children = {ayw_, ayw_z}
    ayw_.parent = ay_w
    ayw_z.parent = ay_w

    graph = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    graph2 = Graph(name="base", graph_attr={"compound": "true", "spline": "false"})
    graph3 = Graph(name="base", graph_attr={"compound": "true", "spline": "false"})

    y.graph_viz(graph)
    _y.viz(graph2, query, {}, minimized=False)
    a_y.viz(graph3, query, {}, minimized=False)
    #graph.view("FIVM_example")

    #graph2 = Digraph(name="base", graph_attr={"compound": "true", "spline": "false"})
    graph.view("variable_order")
    graph2.view("unoptimized_viewtree")
    graph3.view("optimized_viewtree")

def tpch_6():
    Q3 = Query("Q3", OrderedSet([PartSupp, Supplier]), OrderedSet(["PARTKEY", "SUPPKEY", "PS_AVAILQTY", "PS_SUPPLYCOST", "S_NAME"]))
    supp = JoinOrderNode(Q3, "Supplier", OrderedSet([Supplier]), OrderedSet(["SUPPKEY"]), OrderedSet(["S_NAME"]))





# retailer_3Q1()
# example()
# retailer_1Q1a()
# retailer_1Q1b()
# retailer_1Q1c()
# tpch_1Q1b()
