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