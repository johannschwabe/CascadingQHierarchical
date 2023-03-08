from BitSet import BitSet
from Helpers import find_replacements
from Query import Query, QuerySet
from VariableOrder import VariableOrderNode


def run(queries: "list[Query]"):
    bitset = BitSet(queries)
    q_hierarchical = set()
    non_q_hierarchical = set()
    for query in queries:
        query.bitset = bitset
        if query.is_q_hierarchical():
            # print(f"{query.name}: q-hierarchical")
            q_hierarchical.add(query)
        else:
            # print(f"{query.name}: non-q-hierarchical")
            non_q_hierarchical.add(query)
    past_comparisons: "set[tuple[Query, Query]]" = set()
    res = q_hierarchical.copy()
    while True:
        new_q_hierarchical = set()
        new_non_q_hierarchical = set()
        for q_hierarchical_query in q_hierarchical:
            for non_q_hierarchical_query in non_q_hierarchical:
                if non_q_hierarchical_query.name == q_hierarchical_query.name or\
                        (q_hierarchical_query, non_q_hierarchical_query) in past_comparisons:
                    continue
                q_dependant_on = set()
                q_hierarchical_query.dependant_on_deep(q_dependant_on)
                if non_q_hierarchical_query.name in map(lambda x: x.name, q_dependant_on):
                    past_comparisons.add((q_hierarchical_query, non_q_hierarchical_query))
                    continue
                new_replacements  = find_replacements(non_q_hierarchical_query, q_hierarchical_query, q_hierarchical_query.variable_order)
                for new_replacement in new_replacements:
                    new_relations = non_q_hierarchical_query.relations.difference(new_replacement.root_sources())
                    new_relations.add(new_replacement)
                    if len(new_relations) >= len(non_q_hierarchical_query.relations):
                        continue
                    new_query = Query(non_q_hierarchical_query.name, new_relations,
                                      non_q_hierarchical_query.free_variables)
                    new_query.register_bitset(bitset)
                    # new_query.dependant_on = non_q_hierarchical_query.dependant_on.union(q_hierarchical_query.dependant_on)
                    new_query.dependant_on.add(q_hierarchical_query)
                    new_query.dependant_on.update(non_q_hierarchical_query.dependant_on)
                    if new_query.is_q_hierarchical():
                        new_q_hierarchical.add(new_query)
                        past_comparisons.add((q_hierarchical_query, non_q_hierarchical_query))
                        break
                    else:
                        new_non_q_hierarchical.add(new_query)
                past_comparisons.add((q_hierarchical_query, non_q_hierarchical_query))

        res.update(new_q_hierarchical)
        if len(queries) <= len(res):
            compatible = list(map(lambda x: QuerySet(x), filter(lambda x: len(x) == len(queries), find_compatible_reductions(list(res)))))
            if len(compatible) > 0:
                return compatible[0]

        if len(new_q_hierarchical) + len(new_non_q_hierarchical) == 0:
            return None
        non_q_hierarchical.update(new_non_q_hierarchical)   # todo could this lead to double solutions?
        q_hierarchical.update(new_q_hierarchical)



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