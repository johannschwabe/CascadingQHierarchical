from BitSet import BitSet
from Query import Query, QuerySet
from VariableOrder import VariableOrderNode


def run(queries: "set[Query]"):
    bitset = BitSet(queries)
    q_hierarchical = set()
    non_q_hierarchical = set()
    for query in queries:
        query.bitset = bitset
        if query.is_q_hierarchical():
            q_hierarchical.add(query)
        else:
            non_q_hierarchical.add(query)
    #for query in q_hierarchical: #todo move somewhere?
    #    query.views = list(filter(lambda _view: any(map(lambda x: _view.sources.issubset(x.variable_order.all_relations()), non_q_hierarchical)), query.views))
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
                    new_query.dependant_on = q_hierarchical_query
                    if new_query.is_q_hierarchical():
                        new_q_hierarchical.add(new_query)
                        past_comparisons.add((q_hierarchical_query, non_q_hierarchical_query))
                        break
                    else:
                        new_non_q_hierarchical.add(new_query)
                past_comparisons.add((q_hierarchical_query, non_q_hierarchical_query))

        res.update(new_q_hierarchical)
        if len(queries) == len(res):
            return QuerySet(res)
        if len(new_q_hierarchical) + len(new_non_q_hierarchical) == 0:
            return None
        non_q_hierarchical.update(new_non_q_hierarchical)   # todo could this lead to double solutions?
        q_hierarchical.update(new_q_hierarchical)

def find_replacements(non_q_hierarchical_query: "Query", q_hierarchical_query: "Query", node: "VariableOrderNode"):
    res = []
    nr_children = len(node.children)
    v = 1
    views = node.views(q_hierarchical_query)
    if not views:
        return res
    for i in range(0, nr_children):
        for j in range(0, v):
            if v + j > len(views):
                break
            if non_q_hierarchical_query.bitset.view_homomorphism(views[v + j - 1], non_q_hierarchical_query):
                res.append(views[v + j - 1])
        if res:
            return res
        v *= nr_children - i
    for child in node.children:
        res.extend(find_replacements(non_q_hierarchical_query, q_hierarchical_query, child))

    return res
