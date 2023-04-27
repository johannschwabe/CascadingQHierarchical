from typing import TYPE_CHECKING

from JoinOrderNode import JoinOrderNode
from M3Generator import M3Generator, M3Relation

if TYPE_CHECKING:
    from Query import Query, QuerySet
    from Relation import Relation

class M3MultiQueryGenerator:
    def __init__(self, dataset: str, ring:str, example: str, query_set: "QuerySet", var_types: "dict[str,str]"):
        self.example: str = example
        self.dataset: str = dataset
        self.join_order_nodes: "dict[Query, JoinOrderNode]" = {query: JoinOrderNode.generate(query.variable_order, query) for query in query_set.queries}
        self.m3_generators = [M3Generator(dataset, ring, query) for query in self.join_order_nodes.keys()]
        self.base_dir = "/Users/johannschwabe/Documents/git/FIVM/examples/cavier"
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
    def generate_queries(self)->"str, dict[Query, list[str]]":
        res = ""
        query_names = {}
        for generator in self.m3_generators:
            res += f"-- {generator.query.name}\n"
            generator_res, generator_query_names = generator.generate_queries(self.join_order_nodes[generator.query])
            res += generator_res
            query_names[generator.query] = generator_query_names
        return res, query_names
    def generate_triggers(self, batch: bool):
        res = ""
        for generator in self.m3_generators:
            res += f"-- {generator.query.name}\n"
            if batch:
                res += generator.generate_triggers_batch(self.join_order_nodes[generator.query])
            else:
                res += generator.generate_triggers(self.join_order_nodes[generator.query])

        return res

    def generate_config(self, query_names: "dict[Query, list[str]]"):
        res = f"{self.example}\n"
        res += f"{self.dataset}\n"
        res += '|'.join([f"{query.name}|{len(query_names[query])}|{'1' if any(map(lambda x:query in x.dependant_on,query_names.keys())) else '0'}" for query in query_names]) + '\n'
        for query in query_names.keys():
            for query_name in query_names[query]:
                res += f"{query_name}\n"
        with open(f"{self.base_dir}/config/{self.example}/{self.example}.txt", "w") as f:
            f.write(res)
    def generate(self, batch: bool, file: str = "output.m3"):
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
        query_declarations, query_names = self.generate_queries()
        res += query_declarations
        res += '''\n-------------------- TRIGGERS --------------------\n'''
        res += self.generate_triggers(batch)

        res += '''
ON SYSTEM READY {

}'''
        with open(f"{self.base_dir}/m3/{self.example}/{self.example}_{'BATCH' if batch else 'SINGLE'}.m3", "w") as f:
            f.write(res)
        self.generate_config(query_names)

