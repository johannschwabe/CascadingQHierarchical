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
             seed: int
             ):
    res = []
    relation_dist = statistics.NormalDist(avg_nr_relations, std_nr_relations)
    total_relation_dist = statistics.NormalDist(avg_total_relations, std_total_relations)
    variable_dist = statistics.NormalDist(avg_nr_variables, std_nr_variables)
    total_vars_dist = statistics.NormalDist(avg_total_variables, std_total_variables)

    total_relations = max(2, int(total_relation_dist.samples(1, seed=seed)[0]))
    total_vars = max(2, int(total_vars_dist.samples(1,seed=seed+1)[0]))
    possible_vars = list(range(0, total_vars))

    rels = set()
    nr_variables_samples = variable_dist.samples(total_relations, seed=seed+2)
    for i in range(total_relations):
        nr_variables = max(int(nr_variables_samples[i]), 2)
        variables = []
        random.shuffle(possible_vars)
        selected_vars = possible_vars[:nr_variables]
        for selected_var in selected_vars:
            if total_vars <= len(var_names):
                variable_name = f"{var_names[selected_var]}"
            else:
                variable_name = f"{var_names[selected_var % len(var_names)]}_{selected_var // len(var_names)}"
            variables.append(variable_name)
        rels.add(Relation(f"R{i}", variables))
    rel_list = list(sorted(rels, key=lambda x: x.name))

    relation_dist_samples = relation_dist.samples(nr_queries, seed=seed+3)
    for i in range(nr_queries):
        count = 0
        while True:
            random.shuffle(rel_list)
            nr_rels = max(2,int(relation_dist_samples[i]))
            selected_rels = rel_list[:nr_rels]
            variables = set()
            var_list = []
            for rel in selected_rels:
                variables.update(rel.free_variables)
                var_list.extend(rel.free_variables)
            join_variables: "set[str]" = set(filter(lambda x: var_list.count(x) > 1, variables))
            connected = any(map(lambda x: join_variables.isdisjoint(x.free_variables), selected_rels))
            # if connected:
            #     print("gugus")
            if not connected:
                break
            count += 1
            if count % 20 == 0:
                for selected_rel in selected_rels:
                    selected_rel.free_variables.append(random.choice(list(sorted(variables))))
        variable_list = list(sorted(variables))
        random.shuffle(variable_list)
        #print(len(variable_list))
        free_variables = set(variable_list[:random.randint(0, len(variable_list))])
        # print(free_variables)
        new_query = Query(f"Q{i}", set(selected_rels), free_variables)
        res.append(new_query)
    return res
