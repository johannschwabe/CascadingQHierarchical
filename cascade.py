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
    for query in q_hierarchical:
        query.views = list(filter(lambda _view: any(map(lambda x: _view.sources.issubset(x.variable_order.all_relations()), non_q_hierarchical)), query.views))

    res = q_hierarchical.copy()
    while True:
        new_q_hierarchical = set()
        new_non_q_hierarchical = set()
        for non_q_hierarchical_query in non_q_hierarchical:
            for q_hierarchical_query in q_hierarchical: #todo prevent self replacements and circular replacements
                new_replacements  = find_replacements(non_q_hierarchical_query, q_hierarchical_query, q_hierarchical_query.variable_order)
                for new_replacement in new_replacements:
                    new_relations = non_q_hierarchical_query.relations.difference(new_replacement.root_sources())
                    new_relations.add(new_replacement)
                    if len(new_relations) >= len(non_q_hierarchical_query.relations):  # todo check if relation is subsumed
                        continue
                    new_query = Query(non_q_hierarchical_query.name, new_relations,
                                      non_q_hierarchical_query.free_variables)
                    new_query.bitset = bitset
                    if new_query.is_q_hierarchical():
                        new_q_hierarchical.add(new_query)
                    else:
                        new_non_q_hierarchical.add(new_query)
        res.update(new_q_hierarchical)
        if len(new_q_hierarchical) == 0:  #Todo check early termination
            return res      #Todo assembly
        non_q_hierarchical.update(new_non_q_hierarchical)
        q_hierarchical = new_q_hierarchical

def find_replacements(non_q_hierarchical_query: "Query", q_hierarchical_query: "Query", variable_order_node: "VariableOrderNode"):
    res = []
    nr_children = len(variable_order_node.children)
    v = 1
    views = variable_order_node.views(q_hierarchical_query)
    for i in range(nr_children):
        v *= nr_children - i
        for j in range(0,v):
            if non_q_hierarchical_query.bitset.view_homomorphism(views[v+j], q_hierarchical_query.name):
                res.append(views[v+j])
        if res:
            return res
    return res

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
