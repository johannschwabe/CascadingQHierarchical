from Query import Query
from VariableOrder import VariableOrderNode


def find_replacements(non_q_hierarchical_query: "Query", q_hierarchical_query: "Query", node: "VariableOrderNode"):
    res = []
    nr_children = len(node.children) + len(node.relations)
    v = 1
    views = node.views(q_hierarchical_query)
    for i in range(0, nr_children):
        for j in range(0, v):
            if v + j > len(views):
                break
            if non_q_hierarchical_query.bitset.is_homomorphism(views[v + j - 1], non_q_hierarchical_query):
                res.append(views[v + j - 1])
        if res:
            return res
        v *= nr_children - i
    for child in node.children:
        res.extend(find_replacements(non_q_hierarchical_query, q_hierarchical_query, child))

    return res