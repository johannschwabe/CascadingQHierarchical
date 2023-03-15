from Relation import Relation


class RelationPattern:
    def __init__(self, required: int, optional: int, maximal: int, reason: str):
        self.required = required
        self.optional = optional
        self.maximal = maximal
        self.reason = reason

    def query_compatible(self, query_bitset: "int"):
        if query_bitset | self.required == query_bitset and (self.optional == 0 or self.optional & query_bitset > 0):  # feasible
            return True
        if self.optional != 0 and query_bitset & self.required > 0 and self.optional & query_bitset > 0: # Partial possible
            return True
        return False
    def __repr__(self):
        return f"{self.required:05b}-{self.optional:05b}-{self.maximal:05b}"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return hash(self) == hash(other)
