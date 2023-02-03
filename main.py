import itertools
from typing import TYPE_CHECKING

from Relation import Relation
from Query import Query
from VariableOrder import VariableOrderNode


def run(queries: "set[Query]"):
    q_hierarchical = set()
    non_q_hierarchical = set()
    for query in queries:
        query.generate_views(query.variable_order)
        if query.is_q_hierarchical():
            q_hierarchical.add(query)
        else:
            non_q_hierarchical.add(query)

    while True:
        new_q_hierarchical = set()
        new_non_q_hierarchical = set()
        for non_q_hierarchical_query in non_q_hierarchical:
            for q_hierarchical_query in q_hierarchical:
                if non_q_hierarchical_query.name == q_hierarchical_query.name:
                    continue
                for view in q_hierarchical_query.views:
                    all_relations = non_q_hierarchical_query.variable_order.all_relations(True)     # Resolve sub views # Verify different query origin
                    if view.root_sources().issubset(all_relations):
                        new_relations = all_relations.difference(view.root_sources())
                        new_relations.add(view)
                        new_query = Query(non_q_hierarchical_query.name, VariableOrderNode.generate(new_relations))
                        if new_query in q_hierarchical or new_query in non_q_hierarchical:
                            continue
                        if new_query.is_q_hierarchical():
                            new_query.generate_views(new_query.variable_order)
                            new_q_hierarchical.add(new_query)
                        else:
                            new_non_q_hierarchical.add(new_query)
        if len(new_q_hierarchical) == 0 and len(new_q_hierarchical) == 0:
            return q_hierarchical
        q_hierarchical.update(new_q_hierarchical)
        non_q_hierarchical.update(new_non_q_hierarchical)

R1 = Relation("R1", {"x","y"})
R2 = Relation("R2", {"z","y"})
R3 = Relation("R3", {"z","w"})
R4 = Relation("R4", {"q","w"})

VOQ1 = VariableOrderNode.generate({R1, R2})
VOQ2 = VariableOrderNode.generate({R1, R2, R3})
VOQ3 = VariableOrderNode.generate({R1, R2, R3, R4})
Q1 = Query("Q1", VOQ1)
Q2 = Query("Q2", VOQ2)
Q3 = Query("Q3", VOQ3)
res = run({Q1, Q2, Q3})
print("done")