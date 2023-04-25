import itertools

from graphviz import Digraph

from JoinOrderNode import JoinOrderNode
from VariableOrder import VariableOrderNode
from Relation import Relation
from VisOrderNode import VisOrderNode


class Query:

    def __init__(self, name: str, relations: "set[Relation]", free_variables: "set[str]", atoms: "set[Relation]|None" = None):
        self.name = name
        self.free_variables = free_variables
        self.relations: "set[Relation]" = relations
        self.atoms: "set[Relation]" = atoms if atoms else relations
        self._variable_order: "VariableOrderNode | None" = None
        self.hash_key = hash(f"{self.name}-{'/'.join(sorted(map(lambda x: str(hash(x)), self.atoms)))}")
        self._is_q_hierarchical: bool|None = None
        self.dependant_on: "set[Query]" = set()

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
        self._variable_order = VariableOrderNode.generate(self.atoms, self.free_variables)

    def is_q_hierarchical(self) -> bool:
        if self._is_q_hierarchical is not None:
            return self._is_q_hierarchical
        variables = []
        all_atoms = list(self.atoms)
        for rel in all_atoms:
            variables.extend(rel.free_variables)
        join_variables = set(filter(lambda x: variables.count(x) > 1, variables)).union(self.free_variables)

        variable_sets: "dict[str, set[Relation]]" = {}
        for join_variable in join_variables:
            variable_sets[join_variable] = set(filter(lambda x: join_variable in x.free_variables, self.atoms))

        def check_combination(_variables):
            variable_a = _variables[0]
            variable_b = _variables[1]

            c1 = variable_sets[variable_b].issubset(variable_sets[variable_a])
            c2 = variable_sets[variable_a].issubset(variable_sets[variable_b])
            c3 = variable_sets[variable_a].isdisjoint(variable_sets[variable_b])

            different_relations = variable_a != variable_b
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


    def clean_copy(self):
        for rel in self.relations:
            rel._root_sources = set()
        return Query(self.name, self.relations, self.free_variables, self.atoms)

    def __str__(self):
        return self.name + "(" + ",".join(sorted(self.free_variables)) +")" + " = " + ", ".join(sorted(map(lambda x: str(x), self.atoms)))

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
        roots: "dict[Query, VisOrderNode]" = {}
        for query in self.queries:
            join_order = JoinOrderNode.generate(query.variable_order, query)
            vis_order = VisOrderNode.generate(join_order)
            roots[query] = vis_order
        done = set()
        while True:
            next_queries = filter(lambda x: x not in done and x.dependant_on.issubset(done), self.queries)
            for query in next_queries:
                QGraph = Digraph(name=f"cluster_{query.name}", graph_attr={"label":str(query)})
                roots[query].viz(QGraph, query, roots)
                graph.subgraph(QGraph)
                done.add(query)
            if len(done) == len(self.queries):
                break
        graph.view(f"Viz_{name}", "./viz")

        # print(graph.source)
