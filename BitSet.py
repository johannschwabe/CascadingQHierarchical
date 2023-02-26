from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Relation import Relation
    from Query import Query


class BitSet:
    def __init__(self, queries: "set[Query] | list[Query]"):
        self.variable_bitset: "dict[str, int]" = {}
        self.query_bitset: "dict[int, int]" = {}
        self.view_bitset: "dict[str, int]" = {}
        self.next_index: int = 0
        relations = set()
        for query in queries:
            self.query_bitset[hash(query)] = 0
            for relation in query.relations:
                if relation.index == -1:
                    relation.index = self.next_index
                    self.next_index += 1
                self.query_bitset[hash(query)] += 2 ** relation.index
                relations.add(relation)
        for relation in relations:
            for variable in relation.free_variables:
                if variable not in self.variable_bitset:
                    self.variable_bitset[variable] = 0
                self.variable_bitset[variable] += 2**relation.index

    def var_bitset_query(self, vari: str, query: "Query"):
        return self.query_bitset[hash(query)] & self.variable_bitset[vari]

    def rel_bitset(self, query: "Query"):
        return self.query_bitset[hash(query)]

    def add_query(self, query: "Query"):
        self.query_bitset[hash(query)] = 0
        for relation in query.relations:
            if relation.index == -1:
                relation.index = self.next_index
                self.next_index += 1
                for variable in relation.free_variables:
                    self.variable_bitset[variable] += 2 ** relation.index
            self.query_bitset[hash(query)] += 2 ** relation.index

    def add_view(self, view: "Relation"):
        self.view_bitset[view.name] = 0
        for relation in view.root_sources():
            self.view_bitset[view.name] += 2 ** relation.index

    def view_homomorphism(self, view: "Relation", query: "Query"):
        if not view.name in self.view_bitset:
            self.add_view(view)
        return self.query_bitset[hash(query)] | self.view_bitset[view.name] == self.query_bitset[hash(query)]
    #Gugus: root sources for homomorphism, direct sources for q-hierarchical