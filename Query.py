import itertools
import math
from typing import TYPE_CHECKING

from graphviz import Digraph

from RelationPattern import RelationPattern
from JoinOrderNode import JoinOrderNode
from VariableOrder import VariableOrderNode
from Relation import Relation
if TYPE_CHECKING:
    from BitSet import BitSet

class Query:

    def __init__(self, name: str, relations: "set[Relation]", free_variables: "set[str]"):
        self.views: "list[Relation]" = []
        self.name = name
        self.free_variables = free_variables
        self.relations = relations
        self._variable_order: "VariableOrderNode | None" = None
        self.hash_key = hash(f"{self.name}-{'/'.join(sorted(map(lambda x: str(hash(x)), relations)))}")
        self._is_q_hierarchical: bool|None = None
        self.bitset: "BitSet | None" = None
        self.dependant_on: "set[Query]" = set()
        self._resolving_views: "list[RelationPattern]" = []

    def dependant_on_deep(self, res: "set[Query]"):
        if not self.dependant_on:
            return
        if not self.dependant_on.issubset(res):
            for dep in self.dependant_on:
                if dep not in res:
                    res.add(dep)
                    dep.dependant_on_deep(res)

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
        join_variables = set(filter(lambda x: variables.count(x) > 1, variables)).union(self.free_variables)

        def check_combination(_variables):
            variable_a = _variables[0]
            variable_b = _variables[1]

            variable_a_bitset = self.bitset[variable_a] & self.bitset[hash(self)]
            variable_b_bitset = self.bitset[variable_b] & self.bitset[hash(self)]

            c1 = variable_a_bitset | variable_b_bitset == variable_a_bitset
            c2 = variable_a_bitset | variable_b_bitset == variable_b_bitset
            c3 = variable_a_bitset & variable_b_bitset == 0

            different_relations = variable_a_bitset != variable_b_bitset
            a_free = variable_a in self.free_variables
            b_free = variable_b in self.free_variables

            if (c2 and different_relations and a_free and not b_free) or \
                    (c1 and different_relations and b_free and not a_free):
                self._is_q_hierarchical = False
                return False
            if not (c1 or c2 or c3):
                self._is_q_hierarchical = False
                return False
            return True

        self._is_q_hierarchical = all(map(check_combination, itertools.combinations(join_variables, 2)))
        return self._is_q_hierarchical

    def register_bitset(self, bitset: "BitSet"):
        self.bitset = bitset
        bitset.add_query(self)

    def clean_copy(self):
        for rel in self.relations:
            rel._root_sources = set()
        return Query(self.name, self.relations, self.free_variables)

    def resolving_views(self):
        if self.is_q_hierarchical():
            return []
        if self._resolving_views:
            return self._resolving_views
        res = set()

        # Non-Hierarchical
        all_vars = set()
        for relation in self.relations:
            all_vars.update(relation.free_variables)

        bs_query = self.bitset[hash(self)]

        problematic_join_var_tuple = set()
        def check_two_join(var_a, var_b):
            rel_a = bs_query & self.bitset[var_a]
            rel_b = bs_query & self.bitset[var_b]
            a_sub_b = rel_a | rel_b == rel_b
            b_sub_a = rel_a | rel_b == rel_a
            disjoint = rel_a & rel_b == 0
            if not (a_sub_b or b_sub_a or disjoint):
                problematic_join_var_tuple.add((var_a, var_b))
                problematic_join_var_tuple.add((var_b, var_a))

        for comb in itertools.combinations(all_vars, 2):
            check_two_join(comb[0], comb[1])

        for prob_a, prob_b in problematic_join_var_tuple:
            rels = bs_query & self.bitset[prob_a]
            pattern = RelationPattern(rels, 0, bs_query)
            res.add(pattern)
            pattern_2 = RelationPattern( ~ rels & bs_query, rels, bs_query)
            res.add(pattern_2)

        # Non Q
        def check_non_q(free_var_a, bound_var_b):
            rel_a = bs_query & self.bitset[free_var_a]
            rel_b = bs_query & self.bitset[bound_var_b]
            a_sub_b = rel_a | rel_b == rel_b and rel_a != rel_b
            disjoint = rel_a & rel_b == 0
            if not (a_sub_b or disjoint):
                res.add(RelationPattern(rel_a ^ rel_b, rel_b, bs_query))

        for free_var in self.free_variables:
            for bound_var in all_vars.difference(self.free_variables):
                check_non_q(free_var, bound_var)
        self._resolving_views = list(res)
        return self._resolving_views


    def __str__(self):
        return self.name + "(" + ",".join(sorted(self.free_variables)) +")" + " = " + "*".join(sorted(map(lambda x: str(x), self.variable_order.all_relations())))

    def __hash__(self):
        return self.hash_key

    def __eq__(self, other):
        return hash(self) == hash(other)


class QuerySet:
    def __init__(self, queries: "set[Query]"):
        self.queries: "set[Query]" = queries
        self.hash_key = hash(",".join(sorted(map(lambda x: str(hash(x)), self.queries))))

    def __hash__(self):
        return self.hash_key

    def __repr__(self):
        return ",".join(sorted(map(lambda x: str(x), self.queries)))

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
            for dep in query.dependant_on:
                graph.edge(dep.name, query.name, _attributes={"ltail": f"cluster_{dep.name}", "lhead": f"cluster_{query.name}"})
        graph.view(f"Viz_{name}", "./viz")
        #print(graph.source)