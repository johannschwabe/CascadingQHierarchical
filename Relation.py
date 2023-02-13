from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Query import Query


class Relation:


    def __init__(self, name: str, variables: "set[str]", dependantOn = None, sources: "set[Relation] | None" = None):
        self.variables = variables if variables else set()
        self.dependentOn: "Query|None" = dependantOn
        self.sources = sources
        self.name = name

    def root_sources(self):
        res = set()
        if not self.sources:
            return {self}
        for source in self.sources:
            res.update(source.root_sources())
        return res

    def __eq__(self, other):
        if not self.sources and not other.sources:
            return self.variables == other.variables and self.name == other.name
        return self.variables == other.variables and self.sources == other.sources

    def __hash__(self):
        if not self.sources:
            return hash(f"{self.name}{','.join(self.variables)}")
        return hash(",".join(self.variables) + "".join(list(map(lambda x: str(hash(x) if x != self else "GUGUS"), self.sources))))

    def __str__(self):
        return self.name + "(" + ",".join(self.variables) + ")"

    def __repr__(self):
        return str(self)