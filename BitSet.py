from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Relation import Relation
    from Query import Query


class BitSet:
    def __init__(self, queries: "set[Query] | list[Query]"):
        self.variable_bitset: "dict[str, int]" = {}
        self.query_bitset: "dict[str, int]" = {}
        self.view_bitset: "dict[str, int]" = {}
        relations = set()
        for query in queries:
            self.query_bitset[query.name] = 0
            for relation in query.relations:
                self.query_bitset[query.name] += 2 ** relation.index
                relations.add(relation)
        for relation in relations:
            for variable in relation.free_variables:
                if variable not in self.variable_bitset:
                    self.variable_bitset[variable] = 0
                self.variable_bitset[variable] += 2**relation.index

    def var_bitset_query(self, vari: str, query: str):
        return self.query_bitset[query] & self.variable_bitset[vari]

    def rel_bitset(self, query: str):
        return self.query_bitset[query]

    def add_view(self, view: "Relation"):
        self.view_bitset[view.name] = 0
        for relation in view.root_sources():
            self.view_bitset[view.name] += 2 ** relation.index

    def view_homomorphism(self, view: "Relation", query_name: "str"):
        if not view.name in self.view_bitset:
            self.add_view(view)
        return self.query_bitset[query_name] | self.view_bitset[view.name] == self.query_bitset[query_name]