from BitSet import BitSet
from Query import Query, QuerySet
def run(queries: "set[Query]"):
    bitset = BitSet(queries)
    q_hierarchical = set()
    non_q_hierarchical = set()
    for query in queries:
        query._bitset = bitset
        if query.is_q_hierarchical():
            query.generate_views()
            q_hierarchical.add(query)
        else:
            non_q_hierarchical.add(query)
    for query in q_hierarchical:
        query.views = list(filter(lambda _view: any(map(lambda x: _view.sources.issubset(x.variable_order.all_relations()), non_q_hierarchical)), query.views))

    while True:
        new_q_hierarchical = set()
        new_non_q_hierarchical = set()
        for non_q_hierarchical_query in non_q_hierarchical:
            for q_hierarchical_query in q_hierarchical:
                if non_q_hierarchical_query.name == q_hierarchical_query.name:
                    continue

                non_q_dependants = non_q_hierarchical_query.dependant_on()
                non_q_dependants.add(non_q_hierarchical_query)
                q_dependants = q_hierarchical_query.dependant_on()
                invalid = False
                for non_q_dependant in non_q_dependants:
                    if any(map(lambda x: x != non_q_dependant and x.name == non_q_dependant.name, q_dependants)):
                        invalid = True
                        break
                if invalid:
                    continue
                for view in q_hierarchical_query.views:
                    if bitset.view_homomorphism(view, non_q_hierarchical_query.name):
                        old_relations = non_q_hierarchical_query.variable_order.all_relations()
                        new_relations = old_relations.difference(view.root_sources())
                        if any(map(lambda x: x not in view.free_variables and (any(map(lambda y: x in y.free_variables, new_relations)) or x in non_q_hierarchical_query.free_variables), view.all_variables())):
                            continue
                        new_relations.add(view)
                        if len(new_relations) >= len(old_relations): # todo check if relation is subsumed
                            continue
                        new_query = Query(non_q_hierarchical_query.name, new_relations, non_q_hierarchical_query.free_variables)
                        if new_query in q_hierarchical or new_query in non_q_hierarchical:
                            continue
                        new_query._bitset = bitset
                        if new_query.is_q_hierarchical():
                            #print(f".. {new_query}")
                            new_query.generate_views()
                            new_q_hierarchical.add(new_query)
                        else:
                            new_non_q_hierarchical.add(new_query)
        if len(new_q_hierarchical) == 0 and len(new_non_q_hierarchical) == 0 or len(non_q_hierarchical) + len(q_hierarchical) > 2000:
            if len(non_q_hierarchical) + len(q_hierarchical) > 2000:
                print("Cutoff hit")
            compatible_solutions = find_compatible_reductions(list(q_hierarchical))
            return list(filter(lambda x: len(x.queries) == len(queries), compatible_solutions))
        q_hierarchical.update(new_q_hierarchical)
        non_q_hierarchical.update(new_non_q_hierarchical)

def find_compatible(chosen: "Query", options: list[Query]):
    res = []
    for option in options:
        if option.name == chosen.name:
            continue
        dependant_ons = option.dependant_on()
        if any(map(lambda x: x.name == chosen.name and x != chosen, dependant_ons)):
            continue
        res.append(option)
    return res

def find_compatible_reductions(options: list[Query]) -> list[QuerySet]:
    res = []
    if len(options) == 0:
        return []
    next_query_name = list(set(map(lambda x: x.name,options)))[0]
    next_queries = filter(lambda x: x.name == next_query_name, options)
    for option in next_queries:
        compatible = find_compatible(option, options)
        sub_solutions = find_compatible_reductions(compatible)
        if len(sub_solutions) == 0:
            new_query_set = QuerySet()
            new_query_set.add(option)
            res.append(new_query_set)
        else:
            for sub_solution in sub_solutions:
                sub_solution.add(option)
        res.extend(sub_solutions)
    return list(set(res))
