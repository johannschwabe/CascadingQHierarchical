from Relation import Relation


class RelationPattern:
    def __init__(self, required: int, optional: int, maximal: int, reason: str):
        self.required = required
        self.optional = optional
        self.maximal = maximal
        self.reason = reason

    def __repr__(self):
        return f"{format(self.required, 'b')}-{format(self.optional, 'b')}-{format(self.maximal, 'b')}"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return hash(self) == hash(other)
