from Relation import Relation


class RelationPattern:
    def __init__(self, required: int, optional: int, maximal: int):
        self.required = required
        self.optional = optional
        self.maximal = maximal
