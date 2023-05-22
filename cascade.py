from Helpers import find_compatible_reductions, is_homomorphism
from Query import Query, QuerySet
from Relation import Relation
from ordered_set import OrderedSet


def run(queries: "list[Query]"):
    q_hierarchical = set()
    non_q_hierarchical = set()
    for query in queries:
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
                past_comparisons.add((q_hierarchical_query, non_q_hierarchical_query))
                q_dependant_on = set()
                q_hierarchical_query.dependant_on_deep(q_dependant_on)
                if non_q_hierarchical_query.name in map(lambda x: x.name, q_dependant_on):
                    continue
                q_hierarchical_query_relation_names = {x.name for x in q_hierarchical_query.relations}
                non_q_hierarchical_query_relation_names = {x.name for x in non_q_hierarchical_query.relations}
                if not q_hierarchical_query_relation_names.issubset(non_q_hierarchical_query_relation_names):
                    continue
                new_query = is_homomorphism(q_hierarchical_query, non_q_hierarchical_query)
                if new_query:
                    new_query.dependant_on.add(q_hierarchical_query)
                    new_query.dependant_on.update(non_q_hierarchical_query.dependant_on)
                    if new_query.is_q_hierarchical():
                        new_q_hierarchical.add(new_query)
                        break
                    else:
                        new_non_q_hierarchical.add(new_query)

        res.update(new_q_hierarchical)
        if len(queries) <= len(res):
            compatible = list(map(lambda x: QuerySet(x), filter(lambda x: len(x) == len(queries), find_compatible_reductions(list(res)))))
            if len(compatible) > 0:
                return compatible[0]

        if len(new_q_hierarchical) + len(new_non_q_hierarchical) == 0:
            return None
        non_q_hierarchical.update(new_non_q_hierarchical)   # todo could this lead to double solutions?
        q_hierarchical.update(new_q_hierarchical)



