from typing import TYPE_CHECKING

from M3Generator import M3Variable

if TYPE_CHECKING:
    from Query import Query


class Relation:

    def __init__(self, name: str, variables: "list[str]", sources: "list[Relation] | None" = None, index=-1):
        self.index = index
        self.free_variables = variables if variables else []
        self.sources: "list[Relation]" = sources if sources else []
        self.name = name
        self.hash_val = hash(f"{'-'.join(self.free_variables)}:{','.join(map(lambda x: str(x), self.sources)) if self.sources else self.name}")
        self.disp_name = self.name + "(" + ",".join(self.free_variables) + ")"
        self._root_sources = set()

    def set_name(self, name: str):
        self.name = name
        self.disp_name = self.name + "(" + ",".join(self.free_variables) + ")"

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
            res.extend(source.all_variables())
        return res

    def M3ViewName(self, ring: str, vars: "dict[str, M3Variable]"):
        return f"{self.name}({ring}<[]>)[][{','.join(map(lambda x: vars[x].var_type, self.free_variables))}]"

    def __eq__(self, other):
        return self.hash_val == other.hash_val

    def __hash__(self):
        return self.hash_val

    def __str__(self):
        return self.disp_name

    def __repr__(self):
        return str(self)