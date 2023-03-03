from BitSet import BitSet
from Helpers import find_replacements
from Query import Query, QuerySet


def greedy(queries: "list[Query]"):
    bitset = BitSet(queries)
    nr_queries = len(queries)
    q_hierarchical = []
    non_q_hierarchical = []
    for query in queries:
        query.bitset = bitset
        if query.is_q_hierarchical():
            q_hierarchical.append(query)
        else:
            non_q_hierarchical.append(query)
    h_idx = 0
    while h_idx < len(q_hierarchical):
        q_hierarchical_query = q_hierarchical[h_idx]
        nh_idx = 0
        while nh_idx < len(non_q_hierarchical):
            non_q_hierarchical_query = non_q_hierarchical[nh_idx]
            new_replacements = find_replacements(non_q_hierarchical_query, q_hierarchical_query,
                                                 q_hierarchical_query.variable_order)
            for new_replacement in new_replacements:
                new_relations = non_q_hierarchical_query.relations.difference(new_replacement.root_sources())
                new_relations.add(new_replacement)
                if len(new_relations) >= len(non_q_hierarchical_query.relations):
                    continue
                new_query = Query(non_q_hierarchical_query.name, new_relations,
                                  non_q_hierarchical_query.free_variables)
                new_query.register_bitset(bitset)
                new_query.dependant_on.add(q_hierarchical_query)
                new_query.dependant_on.update(non_q_hierarchical_query.dependant_on)
                if new_query.is_q_hierarchical():
                    q_hierarchical.append(new_query)
                    del non_q_hierarchical[nh_idx]
                else:
                    non_q_hierarchical[nh_idx] = new_query
                break
            nh_idx += 1
        h_idx += 1

    return QuerySet(set(q_hierarchical)) if nr_queries == len(q_hierarchical) else None