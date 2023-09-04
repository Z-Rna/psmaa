import numpy as np

from .CriterionTri import CriterionTri
from .ImpactMatrix import ImpactMatrix


class ImpactMatrixTri(ImpactMatrix):
    def __init__(self, alternatives, criterions, data):
        super().__init__(alternatives, criterions, data)

    def add_criterion(self, values: list, name, q=0, p=0, v=0, criterion_type="cardinal", pos: int = 0,
                      ascending: bool = True, *args, **kwargs):
        if not pos in range(len(self.criterions) + 1):
            raise ValueError(f"Given position is out of range: (0,{len(self.criterions)})")
        if not len(self.alternatives) == len(values):
            raise ValueError(f"Length of given array should be {len(self.alternatives)}, rather than {len(values)}.")

        cri_names = self.get_criterions_names()

        if name in cri_names:
            raise ValueError(f"There is already criterion named {name}. Choose other name.")

        criterion = CriterionTri(name, q, p,v, ascending)
        self.criterions = np.insert(self.criterions, pos, criterion)
        self.impact_matrix = np.insert(self.impact_matrix, pos, values, axis=1)
