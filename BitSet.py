from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Relation import Relation
    from Query import Query


class BitSet:
    def __init__(self, queries: "set[Query] | list[Query]"):
        self.bitset: "dict[str|int, int]" = {}
        self.next_index: int = 0
        for query in queries:
            self.add_query(query)

    def add_query(self, query: "Query"):
        for relation in query.relations:
            if relation.index == -1:
                relation.index = self.next_index
                self.next_index += 1
                for variable in relation.free_variables:
                    if variable not in self.bitset:
                        self.bitset[variable] = 0
                    self.bitset[variable] += 2**relation.index          # Var-name

                if relation.sources:
                    self.bitset[relation.name] = 0
                    for source in relation.sources:
                        self.bitset[relation.name] = 2 ** source.index  # View-name
        if query.name not in self.bitset:
            self.bitset[query.name] = 0
            for relation in query.relations:
                self.bitset[query.name] += 2**relation.index            # Query-name

        self.bitset[hash(query)] = 0
        for relation in query.relations:
            self.bitset[hash(query)] += 2 ** relation.index             # Query-hash


    def is_homomorphism(self, view: "Relation", non_q_query: "Query"):
        view_name = f"View_{view.name}"
        if view.name not in self.bitset:
            self.bitset[view_name] = 0
            for source in view.sources:
                self.bitset[view_name] += 2 ** source.index
        return self.bitset[non_q_query.name] | self.bitset[view_name] == self.bitset[non_q_query.name]

    def __getitem__(self, item):
        return self.bitset[item]
