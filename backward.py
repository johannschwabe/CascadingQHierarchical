from BitSet import BitSet
from Helpers import find_compatible_reductions
from Query import Query, QuerySet
from RelationPattern import RelationPattern


def backward_search(queries: "list[Query]"):
    bitset = BitSet(queries)
    q_hierarchical = set()
    non_q_hierarchical = set()
    for query in queries:
        query.bitset = bitset
        if query.is_q_hierarchical():
            q_hierarchical.add(query)
        else:
            non_q_hierarchical.add(query)
    res = q_hierarchical.copy()
    past_comparisons: "set[tuple[Query, Query]]" = set()
    while True:
        new_q_hierarchical = set()
        new_non_q_hierarchical = set()
        for non_q_hierarchical_query in non_q_hierarchical:
            patterns = non_q_hierarchical_query.resolving_views()
            for q_hierarchical_query in q_hierarchical:
                if non_q_hierarchical_query.name == q_hierarchical_query.name or \
                        (non_q_hierarchical_query, q_hierarchical_query) in past_comparisons:
                    continue
                past_comparisons.add((non_q_hierarchical_query, q_hierarchical_query))
                for pattern in patterns:

                    q_dependant_on = set()
                    q_hierarchical_query.dependant_on_deep(q_dependant_on)
                    if non_q_hierarchical_query.name in map(lambda x: x.name, q_dependant_on):
                        continue

                    q_bs = bitset[q_hierarchical_query.name]
                    if q_bs | pattern.required == q_bs and (pattern.optional == 0 or pattern.optional & q_bs > 0): # feasible
                        new_replacement = q_hierarchical_query.variable_order.find_view(pattern, bitset, q_hierarchical_query)
                        if not new_replacement:
                            continue
                        if new_replacement in non_q_hierarchical_query.relations:
                            continue
                        new_relations = non_q_hierarchical_query.relations.difference(new_replacement.root_sources())
                        new_relations.add(new_replacement)

                        new_query = Query(non_q_hierarchical_query.name, new_relations,
                                          non_q_hierarchical_query.free_variables)
                        new_query.register_bitset(bitset)
                        # new_query.dependant_on = non_q_hierarchical_query.dependant_on.union(q_hierarchical_query.dependant_on)
                        new_query.dependant_on.add(q_hierarchical_query)
                        new_query.dependant_on.update(non_q_hierarchical_query.dependant_on)
                        if new_query.is_q_hierarchical():
                            new_q_hierarchical.add(new_query)
                            break
                        else:
                            new_non_q_hierarchical.add(new_query)
        res.update(new_q_hierarchical)
        if len(queries) <= len(res):
            compatible = list(map(lambda x: QuerySet(x),
                                  filter(lambda x: len(x) == len(queries), find_compatible_reductions(list(res)))))
            if len(compatible) > 0:
                return compatible[0]

        if len(new_q_hierarchical) + len(new_non_q_hierarchical) == 0:
            return None
        non_q_hierarchical.update(new_non_q_hierarchical)  # todo could this lead to double solutions?
        q_hierarchical.update(new_q_hierarchical)