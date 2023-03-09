from Query import Query
from VariableOrder import VariableOrderNode


def find_replacements(non_q_hierarchical_query: "Query", q_hierarchical_query: "Query", node: "VariableOrderNode"):
    res = []
    nr_children = len(node.children) + len(node.relations)
    v = 1
    views = node.views(q_hierarchical_query)
    for i in range(0, nr_children - 1):
        for j in range(0, v):
            if i + j >= len(views):
                break
            if non_q_hierarchical_query.bitset.is_homomorphism(views[i + j], non_q_hierarchical_query):
                res.append(views[i + j])
        if res:
            return res
        v *= nr_children - i
    for child in node.children:
        res.extend(find_replacements(non_q_hierarchical_query, q_hierarchical_query, child))

    return res

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