from graphviz import Digraph
from ordered_set import OrderedSet

from JoinOrderNode import JoinOrderNode
from Query import Query, QuerySet
from Relation import Relation
from tpch import Part, PartSupp, LineItem, Orders
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

# retailer_3Q1()

# retailer_1Q1a()
# retailer_1Q1b()
# retailer_1Q1c()
