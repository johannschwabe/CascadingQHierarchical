import random

from graphviz import Graph, Digraph

from VariableOrder import VariableOrderNode
from Relation import Relation
import graphviz
import colors
from random import shuffle

class Query:

    def __init__(self, name: str, relations: "set[Relation]", free_variables: "set[str]"):
        self.views: "list[Relation]" = []
        self.name = name
        self.free_variables = free_variables
        self.variable_order: "VariableOrderNode" = VariableOrderNode.generate(relations, free_variables)
        self.hash_key = hash(f"{self.name}-{'/'.join(sorted(map(lambda x: str(hash(x)), self.variable_order.all_relations())))}")
        self._dependant_on_deep = set()
        self._dependant_on_non_deep = set()


    def is_q_hierarchical(self) -> bool:
        variables = set()
        all_relations = self.variable_order.all_relations()
        for rel in all_relations:
            variables = variables.union(rel.free_variables)
        for variable_a in variables:
            for variable_b in variables:
                if variable_a == variable_b:
                    continue
                atoms_a = set(filter(lambda x: variable_a in x.free_variables, all_relations))
                atoms_b = set(filter(lambda x: variable_b in x.free_variables, all_relations))
                c1 = atoms_a.issubset(atoms_b)
                c2 = atoms_b.issubset(atoms_a)
                c3 = atoms_a.isdisjoint(atoms_b)

                if atoms_a < atoms_b and variable_a in self.free_variables and variable_b not in self.free_variables:
                    return False
                if not (c1 or c2 or c3):
                    return False
        return True

    def generate_views(self):
        self.views = self.variable_order.generate_views(self)
        a = 0

    def dependant_on(self, deep:bool = True):
        if self._dependant_on_deep and deep: return self._dependant_on_deep
        if self._dependant_on_non_deep and not deep: return self._dependant_on_deep
        res: "set[Query]" = set()
        for relation in self.variable_order.all_relations(False):
            if relation.dependentOn:
                res.add(relation.dependentOn)
                if deep:
                    res.update(relation.dependentOn.dependant_on())
        if deep:
            self._dependant_on_deep = res
        else:
            self._dependant_on_non_deep = res
        return res

    def __str__(self):
        return self.name + "(" + ",".join(sorted(self.free_variables)) +")" + " = " + "*".join(sorted(map(lambda x: str(x), self.variable_order.all_relations())))

    def __hash__(self):
        return self.hash_key

    def __eq__(self, other):
        return hash(self) == hash(other)


class QuerySet:
    def __init__(self):
        self.queries: "set[Query]" = set()
        self.hash_key = hash(",".join(sorted(map(lambda x: str(hash(x)), self.queries))))

    def __hash__(self):
        return self.hash_key

    def __repr__(self):
        return ",".join(sorted(map(lambda x: str(x), self.queries)))

    def add(self, other: "Query"):
        self.queries.add(other)


    def __eq__(self, other):
        return hash(self) == hash(other)

    def graph_viz(self, name = 0):
        graph = Digraph(name="base", graph_attr={"compound": "true", "spline":"false"})
        ress= []
        for query in self.queries:
            res = Digraph(name=f"cluster_{query.name}", graph_attr={"label": f"{query.name}({','.join(query.free_variables)})"})
            query.variable_order.graph_viz_2(res, query)
            ress.append(res)
        for res in ress:
            graph.subgraph(res)
        for query in self.queries:
            dependant_on = query.dependant_on(False)
            for dep in dependant_on:
                graph.edge(query.name, dep.name, _attributes={"ltail": f"cluster_{query.name}", "lhead": f"cluster_{dep.name}"})
        graph.view(f"Viz_{name}")
        #print(graph.source)