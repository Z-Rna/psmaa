from .Criterion import Criterion


class CriterionTri(Criterion):
    def __init__(self, name, q, p, v, ascending=True, criterion_type="cardinal"):
        super().__init__(name, ascending, criterion_type)
        self.q: float = q
        self.p: float = p
        self.v: float = v
