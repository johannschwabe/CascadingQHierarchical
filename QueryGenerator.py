import itertools
import random
import statistics

from Query import Query
from Relation import Relation

var_names = "abcdefghijklmnopqrstuvwxyz"

def generate(nr_queries: int,
             avg_nr_relations: float,
             std_nr_relations: float,
             avg_total_relations: float,
             std_total_relations: float,
             avg_nr_variables: float,
             std_nr_variables:float,
             avg_total_variables: float,
             std_total_variables: float,
             ):
    res = []
    relation_dist = statistics.NormalDist(avg_nr_relations, std_nr_relations)
    total_relation_dist = statistics.NormalDist(avg_total_relations, std_total_relations)
    variable_dist = statistics.NormalDist(avg_nr_variables, std_nr_variables)
    total_vars_dist = statistics.NormalDist(avg_total_variables, std_total_variables)

    total_relations = max(2, int(total_relation_dist.samples(1)[0]))
    total_vars = max(2, int(total_vars_dist.samples(1)[0]))
    possible_vars = list(range(0, total_vars))

    rels = set()
    for i in range(total_relations):
        nr_variables = max(int(variable_dist.samples(1)[0]), 2)
        variables = set()
        random.shuffle(possible_vars)
        selected_vars = possible_vars[:nr_variables]
        for selected_var in selected_vars:
            if total_vars <= len(var_names):
                variable_name = f"{var_names[selected_var]}"
            else:
                variable_name = f"{var_names[selected_var % len(var_names)]}_{selected_var // len(var_names)}"
            variables.add(variable_name)
        rels.add(Relation(f"R{i}", variables))
    rel_list = list(rels)

    for i in range(nr_queries):
        random.shuffle(rel_list)
        nr_rels = max(2,int(relation_dist.samples(1)[0]))
        selected_rels = rel_list[:nr_rels]

        variables = set()
        for rel in selected_rels:
            variables.update(rel.free_variables)

        variable_list = list(variables)
        random.shuffle(variable_list)
        free_variables = set(variable_list[:random.randint(0, len(variable_list))])


        res.append(Query(f"Q{i}", set(selected_rels), free_variables))
    return res
