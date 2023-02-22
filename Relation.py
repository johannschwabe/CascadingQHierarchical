from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Query import Query


class Relation:

    def __init__(self, name: str, variables: "set[str]",index: int, dependantOn = None, sources: "List[Relation] | None" = None):
        self.index = index
        self.free_variables = variables if variables else set()
        self.dependentOn: "Query|None" = dependantOn
        self.sources = sources
        self.name = name
        self.hash_val = hash(f"{'-'.join(sorted(self.free_variables))}:{','.join(map(lambda x: str(x), self.sources)) if self.sources else self.name}")
        self.disp_name = self.name + "(" + ",".join(sorted(self.free_variables)) + ")"
        self._root_sources = set()

    def set_name(self, name: str):
        self.name = name
        self.disp_name = self.name + "(" + ",".join(sorted(self.free_variables)) + ")"

    def root_sources(self):
        if self._root_sources:
            return self._root_sources
        res = set()
        if not self.sources:
            return {self}
        for source in self.sources:
            res.update(source.root_sources())
        self._root_sources = res
        return res

    def all_variables(self):
        res = self.free_variables.copy()
        for source in self.sources:
            res.update(source.free_variables)
        return res

    def __eq__(self, other):
        return self.hash_val == other.hash_val

    def __hash__(self):
        return self.hash_val

    def __str__(self):
        return self.disp_name

    def __repr__(self):
        return str(self)