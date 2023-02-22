import itertools

from graphviz import Digraph

from JoinOrderNode import JoinOrderNode
from VariableOrder import VariableOrderNode
from Relation import Relation

class Query:

    def __init__(self, name: str, relations: "set[Relation]", free_variables: "set[str]"):
        self.views: "list[Relation]" = []
        self.name = name
        self.free_variables = free_variables
        self.relations = relations
        self._variable_order: "VariableOrderNode | None" = None
        self.hash_key = hash(f"{self.name}-{'/'.join(sorted(map(lambda x: str(hash(x)), relations)))}")
        self._dependant_on_deep = set()
        self._dependant_on_non_deep = set()
        self._is_q_hierarchical: bool|None = None


    @property
    def variable_order(self):
        if not self._variable_order:
            self.generate_variable_order()
        return self._variable_order

    def generate_variable_order(self):
        self._variable_order = VariableOrderNode.generate(self.relations, self.free_variables)

    def is_q_hierarchical(self) -> bool:
        if self._is_q_hierarchical is not None:
            return self._is_q_hierarchical
        variables = []
        all_relations = list(self.relations)
        for rel in all_relations:
            variables.extend(rel.free_variables)
        join_variables = list(filter(lambda x: variables.count(x) > 1, variables))

        bit_set: "dict[str, int]" = {}
        for join_variable in join_variables:
            bitset = 0
            for index, relation in enumerate(all_relations):
                if join_variable in relation.free_variables:
                    bitset += 2**index
            bit_set[join_variable] = bitset



        def check_combination(_variables):
            variable_a = _variables[0]
            variable_b = _variables[1]

            c1 = bit_set[variable_a] | bit_set[variable_b] == bit_set[variable_a]
            c2 = bit_set[variable_a] | bit_set[variable_b] == bit_set[variable_b]
            c3 = bit_set[variable_a] & bit_set[variable_b] == 0

            if bit_set[variable_a] | bit_set[variable_b] == bit_set[variable_b] and bit_set[variable_a] != bit_set[variable_b]  and variable_a in self.free_variables and variable_b not in self.free_variables:
                self._is_q_hierarchical = False
                return False
            if not (c1 or c2 or c3):
                self._is_q_hierarchical = False
                return False
            return True

        self._is_q_hierarchical = all(map(check_combination, itertools.combinations(join_variables, 2)))
        return self._is_q_hierarchical

    def generate_views(self):
        self.views = self.variable_order.generate_views(self)

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
        self.hash_key = hash(",".join(sorted(map(lambda x: str(hash(x)), self.queries))))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def graph_viz(self, name = 0):
        graph = Digraph(name="base", graph_attr={"compound": "true", "spline":"false"})
        ress= []
        for query in self.queries:
            res = Digraph(name=f"cluster_{query.name}", graph_attr={"label": f"{query.name}({','.join(sorted(query.free_variables))})"})
            join_order = JoinOrderNode.generate(query.variable_order, query)
            join_order.viz(res, query)
            res.node(query.name, style="invis")

            ress.append(res)
        for res in ress:
            graph.subgraph(res)
        for query in self.queries:
            dependant_on = query.dependant_on(False)
            for dep in dependant_on:
                graph.edge(query.name, dep.name, _attributes={"ltail": f"cluster_{query.name}", "lhead": f"cluster_{dep.name}"})
        graph.view(f"Viz_{name}")
        #print(graph.source)