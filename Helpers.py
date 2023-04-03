import itertools

from Query import Query
from Relation import Relation


def find_compatible(chosen: "Query", options: list[Query]):
    res = []
    for option in options:
        if option.name == chosen.name:
            continue
        dependant_ons = set()
        option.dependant_on_deep(dependant_ons)
        if any(map(lambda x: x.name == chosen.name and x != chosen, dependant_ons)):
            continue
        res.append(option)
    return res

def find_compatible_reductions(options: list[Query]) -> list[set[Query]]:
    res = []
    if len(options) == 0:
        return []
    next_query_name = sorted(list(set(map(lambda x: x.name,options))))[0]
    next_queries = filter(lambda x: x.name == next_query_name, options)
    for option in next_queries:
        compatible = find_compatible(option, options)
        sub_solutions = find_compatible_reductions(compatible)
        if len(sub_solutions) == 0:
            res.append({option})
        else:
            for sub_solution in sub_solutions:
                sub_solution.add(option)
        res.extend(sub_solutions)
    return res

def is_homomorphism(q_query: "Query", nq_query: "Query"):
    q_query_vars: "dict[str, list[str]]" = {}
    posi_to_q_var_name: "dict[str, str]" = {}
    for rel in q_query.relations:
        for free_var in rel.free_variables:
            posi_to_q_var_name[f"{rel.name}.{rel.free_variables.index(free_var)}"] = free_var
            if free_var in q_query_vars:
                q_query_vars[free_var].append(f"{rel.name}.{rel.free_variables.index(free_var)}")
            else:
                q_query_vars[free_var]=[f"{rel.name}.{rel.free_variables.index(free_var)}"]
    q_query_join_positions = set()
    for posis in q_query_vars.values():
        q_query_join_positions.update(map(lambda x: '='.join(sorted(x)), itertools.combinations(posis, 2)))
    nq_query_vars: "dict[str, list[str]]" = {}
    q_var_to_nq_var: "dict[str,str]" = {}
    required_vars: "set[str]" = nq_query.free_variables
    for rel in nq_query.relations:
        for free_var in rel.free_variables:
            posi = f"{rel.name}.{rel.free_variables.index(free_var)}"
            if posi in posi_to_q_var_name:
                q_var_to_nq_var[posi_to_q_var_name[posi]] = free_var
            if free_var in nq_query_vars:
                required_vars.add(free_var)
                nq_query_vars[free_var].append(posi)
            else:
                nq_query_vars[free_var] = [posi]
    nq_query_join_positions = set()
    for posis in nq_query_vars.values():
        nq_query_join_positions.update(map(lambda x: '='.join(sorted(x)), itertools.combinations(posis, 2)))
    homomorphism = q_query_join_positions.issubset(nq_query_join_positions)
    if not homomorphism:
        return None

    q_query_rel_names = set(map(lambda x: x.name, q_query.relations))
    replaced_rels = list(filter(lambda x: x.name in q_query_rel_names, nq_query.relations))

    replaced_rels_vars: "set[str]" = set()
    for rel in replaced_rels:
        replaced_rels_vars.update(rel.free_variables)

    required_view_vars: "set[str]" = required_vars.intersection(replaced_rels_vars)

    new_view_free_vars: "set[str]" = {q_var_to_nq_var[q_var] for q_var in filter(lambda x:x in q_var_to_nq_var, q_query.free_variables) }
    if required_view_vars.issubset(new_view_free_vars):
        remaining_rels = nq_query.atoms.difference(replaced_rels)
        remaining_rels.add(Relation(f"V_{q_query.name}", list(new_view_free_vars), replaced_rels))
        return Query(nq_query.name, nq_query.relations, nq_query.free_variables, remaining_rels)

    return None



