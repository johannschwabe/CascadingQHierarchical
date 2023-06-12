import random

from ordered_set import OrderedSet

from M3MultiQueryGenerator import M3MultiQueryGenerator
from Query import Query
from Relation import Relation
from cascade import run

random.seed(22)
base_dataset = "retailer"
dataset_version = ["_unordered"]

Census = Relation("Census", OrderedSet([
    "Zip",
    "Population",
    "White",
    "Asian",
    "Pacific",
    "Blackafrican",
    "MedianAge",
    "OccupiedHouseUnits",
    "HouseUnits",
    "Families",
    "Housholds",
    "HusbWife",
    "Males",
    "Females",
    "HousholdsChildren",
    "Hispanic",
]))
Item = Relation("Item", OrderedSet([
    "Ksn",
    "SubCategory",
    "Category",
    "CategoryCluster",
    "Prize"
]))
Inventory = Relation("Inventory", OrderedSet([
    "Locn",
    "DateId",
    "Ksn",
    "InventoryUnits",
]))
Weather = Relation("Weather", OrderedSet([
    "Locn",
    "DateId",
    "Rain",
    "Snow",
    "MaxTemp",
    "MinTemp",
    "MeanWind",
    "Thunder",
]))
Location = Relation("Location", OrderedSet([
    "Locn",
    "Zip",
    "RgnCd",
    "ClimbZnNbr",
    "TotalAreaSqFt",
    "SellAreaSqFt",
    "AvgHigh",
    "SuperTargetDistance",
    "SuperTargetDriveTime",
    "TargetDistance",
    "TargetDriveTime",
    "WalmartDistance",
    "WalmartDriveTime",
    "WalmartSuperCenterDistance",
    "WalmartSuperCenterDriveTime"
]))

datatypes ={
                "Zip": "int",
                "Population": "int",
                "White": "int",
                "Asian": "int",
                "Pacific": "int",
                "Hispanic": "int",
                "Males": "int",
                "Females": "int",
                "Blackafrican": "int",
                "HusbWife": "int",
                "MedianAge": "int",
                "HouseUnits": "int",
                "OccupiedHouseUnits": "int",
                "Families": "int",
                "Housholds": "int",
                "HousholdsChildren": "int",
                "Ksn": "int",
                "SubCategory": "int",
                "Category": "int",
                "CategoryCluster": "int",
                "Prize": "double",
                "InventoryUnits": "int",
                "DateId": "int",
                "Locn": "int",
                "MaxTemp": "int",
                "MinTemp": "int",
                "MeanWind": "double",
                "Snow": "int",
                "Rain": "int",
                "Thunder": "int",
                "RgnCd": "int",
                "ClimbZnNbr": "int",
                "TotalAreaSqFt": "int",
                "SellAreaSqFt": "int",
                "AvgHigh": "int",
                "SuperTargetDistance": "double",
                "SuperTargetDriveTime": "double",
                "TargetDistance": "double",
                "TargetDriveTime": "double",
                "WalmartDistance": "double",
                "WalmartDriveTime": "double",
                "WalmartSuperCenterDistance": "double",
                "WalmartSuperCenterDriveTime": "double",
            }

def retailer_1():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Weather, Location]), OrderedSet([
        "Ksn",
        "DateId",
        "Locn",
        "Category",
        "Zip",
        "Rain"
    ]))
    Q2 = Query("Q2", OrderedSet([Inventory, Weather, Location]), OrderedSet([
        "Ksn",
        "Locn",
        "DateId",
        "MaxTemp",
        "Zip",
        "Rain"
    ]))

    res = run([Q1, Q2])
    if res:
        for version in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "1",
                version,
                'RingFactorizedRelation',
                res,
                datatypes
            )
            multigenerator.generate(batch=True)

        # res.graph_viz("Retailer_1", join_order=True)
    else:
        print("No result")


def retailer_2():
    Q1 = Query("Q1", OrderedSet([Census, Weather, Location]),
               OrderedSet(["Locn",
                           "DateId",
                           "Rain",
                           "Snow",
                           "MaxTemp",
                           "MinTemp",
                           "MeanWind",
                           "Thunder",
                           "Zip",
                           "RgnCd",
                           "ClimbZnNbr",
                           "TotalAreaSqFt",
                           "SellAreaSqFt",
                           "AvgHigh",
                           "SuperTargetDistance",
                           "SuperTargetDriveTime",
                           "TargetDistance",
                           "TargetDriveTime",
                           "WalmartDistance",
                           "WalmartDriveTime",
                           "WalmartSuperCenterDistance",
                           "WalmartSuperCenterDriveTime",
                           "Population",
                           "White",
                           "Asian",
                           "Pacific",
                           "Blackafrican",
                           "MedianAge",
                           "OccupiedHouseUnits",
                           "HouseUnits",
                           "Families",
                           "Housholds",
                           "HusbWife",
                           "Males",
                           "Females",
                           "HousholdsChildren",
                           "Hispanic",
                           ]))
    Q2 = Query("Q2", OrderedSet([Weather, Location]), OrderedSet([
        "Locn",
        "DateId",
        "Rain",
        "Snow",
        "MaxTemp",
        "MinTemp",
        "MeanWind",
        "Thunder",
        "Zip",
        "RgnCd",
        "ClimbZnNbr",
        "TotalAreaSqFt",
        "SellAreaSqFt",
        "AvgHigh",
        "SuperTargetDistance",
        "SuperTargetDriveTime",
        "TargetDistance",
        "TargetDriveTime",
        "WalmartDistance",
        "WalmartDriveTime",
        "WalmartSuperCenterDistance",
        "WalmartSuperCenterDriveTime"
    ]))

    res = run([Q1, Q2])
    if res:
        for version in dataset_version:

            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "2",
                version,
                'RingFactorizedRelation',
                res,
                datatypes
            )
            multigenerator.generate(batch=True)

        #res.graph_viz("Retailer_2")
    else:
        print("No result")

def retailer_3():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Weather, Location]), OrderedSet([
        "Ksn",
        "DateId",
        "Locn",
        "Category",
        "Zip",
        "Rain"
    ]))
    Q2 = Query("Q2", OrderedSet([Inventory, Item]), OrderedSet([
        "Ksn",
        "Locn",
        "DateId",
        "Prize",
        "Category",
    ]))
    res = run([Q1, Q2])
    if res:
        for version in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "3",
                version,
                'RingFactorizedRelation',
                res,
                datatypes
            )
            multigenerator.generate(batch=True)

        # res.graph_viz("Retailer_3", join_order=True)
    else:
        print("No result")


def retailer_4():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Location]), OrderedSet([
        "Ksn",
        "Locn",
        "Category",
        "Zip",
    ]))
    Q2 = Query("Q2", OrderedSet([Inventory, Item]), OrderedSet([
        "Ksn",
        "Locn",
        "Prize",
        "Category",
    ]))
    res = run([Q1, Q2])
    if res:
        for version in dataset_version:
            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "4",
                version,
                'RingFactorizedRelation',
                res,
                datatypes
            )
            multigenerator.generate(batch=True)

        #res.graph_viz("Retailer_4", join_order=True)
    else:
        print("No result")

def retailer_5():
    Q1 = Query("Q1", OrderedSet([Inventory, Item, Weather, Location]), OrderedSet([
        "Ksn",
        "DateId",
        "Locn",
    ]))
    Q2 = Query("Q2", OrderedSet([Inventory, Weather, Location]), OrderedSet([
        "Ksn",
        "Locn",
        "DateId",
    ]))

    res = run([Q1, Q2])
    if res:
        for version in dataset_version:

            multigenerator = M3MultiQueryGenerator(
                base_dataset,
                "5",
                version,
                'RingFactorizedRelation',
                res,
                datatypes
            )
            multigenerator.generate(batch=True)

        # res.graph_viz("Retailer_5", join_order=True)
    else:
        print("No result")


if __name__ == "__main__":
    retailer_1()
    retailer_2()
    retailer_3()
    retailer_4()
    retailer_5()