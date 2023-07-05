from typing import TYPE_CHECKING

from ordered_set import OrderedSet

if TYPE_CHECKING:
    from JoinOrderNode import JoinOrderNode


class Relation:

    def __init__(self, name: str, variables: "OrderedSet[str]", source_relations: "OrderedSet[Relation]|None"=None, source_query: "Query | None" = None):
        self.free_variables: "OrderedSet[str]" = variables if variables else OrderedSet([])
        self.source_query: "Query | None" = source_query
        self.source_relations: "OrderedSet[Relation]" = source_relations if source_relations else OrderedSet([])
        self.name: str = name
        self.hash_val = hash(f"{'-'.join(self.free_variables)}:{','.join(map(lambda x: str(x), self.source_relations)) if self.source_relations else self.name}")
        self.disp_name = self.name + "(" + ",".join(self.free_variables) + ")"
        self._root_sources = set()

    def set_name(self, name: str):
        self.name = name
        self.disp_name = self.name + "(" + ",".join(self.free_variables) + ")"
    def root_sources(self):
        if self._root_sources:
            return self._root_sources
        res = set()
        if not self.source_relations:
            return {self}
        for source in self.source_relations:
            res.update(source.root_sources())
        self._root_sources = res
        return res

    def all_variables(self) -> "OrderedSet[str]":
        res = self.free_variables.copy()
        for source in self.source_relations:
            res.union(source.all_variables())
        return res

    def M3ViewName(self):
        return f"{self.name}({','.join(self.free_variables)})"

    def viz_label(self, minimized=False):
        if minimized:
            return f"{self.name}({','.join([var.capitalize() for var in self.free_variables[:4]])}...)"
        return self.disp_name

    def __eq__(self, other):
        return self.hash_val == other.hash_val

    def __hash__(self):
        return self.hash_val

    def __str__(self):
        return self.disp_name

    def __repr__(self):
        return str(self)