from typing import TYPE_CHECKING

from JoinOrderNode import JoinOrderNode
from M3Generator import M3Generator, M3Relation

if TYPE_CHECKING:
    from Query import Query, QuerySet
    from Relation import Relation

class M3MultiQueryGenerator:
    def __init__(self, dataset: str, ring:str, query_set: "QuerySet", var_types: "dict[str,str]"):
        self.dataset: str = dataset
        self.join_order_nodes: "dict[Query, JoinOrderNode]" = {query: JoinOrderNode.generate(query.variable_order, query) for query in query_set.queries}
        self.m3_generators = [M3Generator(dataset, ring, query) for query in self.join_order_nodes.keys()]
        for generator in self.m3_generators:
            generator.self_init(var_types)

    def assign_index(self):
        start = 0
        for generator in self.m3_generators:
            generator.var_index = start
            generator.assign_index(self.join_order_nodes[generator.query])
            start = generator.var_index

    def generate_sources(self):
        relations: "set[M3Relation]" = set()
        for generator in self.m3_generators:
            relations.update(generator.relations)
        sources = ""
        for relation in relations:
            sources += relation.generate_source(self.dataset)
        return sources

    def generate_maps(self):
        res = ""
        for generator in self.m3_generators:
            res += f"-- {generator.query.name}\n"
            res += generator.generate_maps(self.join_order_nodes[generator.query])
        return res
    def generate_tmp_maps(self):
        res = ""
        for generator in self.m3_generators:
            res += f"-- {generator.query.name}\n"
            res += generator.generate_tmp_maps(self.join_order_nodes[generator.query])
        return res

    # Assemble queries from the queryset
    def generate_queries(self):
        res = ""
        for generator in self.m3_generators:
            res += f"-- {generator.query.name}\n"
            res += generator.generate_queries(self.join_order_nodes[generator.query])
        return res
    def generate_triggers(self, batch: bool):
        res = ""
        for generator in self.m3_generators:
            res += f"-- {generator.query.name}\n"
            if batch:
                res += generator.generate_triggers_batch(self.join_order_nodes[generator.query])
            else:
                res += generator.generate_triggers(self.join_order_nodes[generator.query])

        return res
    def generate(self, batch: bool):
        self.assign_index()
        res = '''---------------- TYPE DEFINITIONS ---------------
CREATE DISTRIBUTED TYPE RingFactorizedRelation
FROM FILE 'ring/ring_factorized.hpp'
WITH PARAMETER SCHEMA (dynamic_min);

-------------------- SOURCES --------------------\n'''
        res += self.generate_sources()
        res += '''\n-------------------- MAPS --------------------\n'''
        res += self.generate_maps()
        if batch:
            res += self.generate_tmp_maps()
        res += '''\n-------------------- QUERIES --------------------\n'''
        res += self.generate_queries()
        res += '''\n-------------------- TRIGGERS --------------------\n'''
        res += self.generate_triggers(batch)

        res += '''
ON SYSTEM READY {

}'''
        with open("output.m3", "w") as f:
            f.write(res)

