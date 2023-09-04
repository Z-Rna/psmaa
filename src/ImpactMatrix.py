import numpy as np

from .Alternative import Alternative
from .Criterion import Criterion


class ImpactMatrix:
    def __init__(self, alternatives, criterions, data):
        self.alternatives = alternatives
        self.criterions = criterions
        self.impact_matrix = data

    def add_alternative(self, values: list, name: str, pos: int = 0):
        if not pos in range(len(self.alternatives) + 1):
            raise ValueError(f"Given position: {pos} is out of range: (0,{len(self.alternatives)}).")
        if not len(self.criterions) == len(values):
            raise ValueError(f"Length of given array should be {len(self.criterions)}, rather than {len(values)}.")

        alt_names = self.get_alternatives_names()

        if name in alt_names:
            raise ValueError(f"There is already alternative named {name}. Choose other name.")

        alternative = Alternative(name)
        self.alternatives = np.insert(self.alternatives, pos, alternative)
        self.impact_matrix = np.insert(self.impact_matrix, pos, values, axis=0)

    def add_criterion(self, values: list, name, criterion_type = "cardinal", pos: int = 0, ascending: bool = True, *args, **kwargs):
        if not pos in range(len(self.criterions) + 1):
            raise ValueError(f"Given position is out of range: (0,{len(self.criterions)})")
        if not len(self.alternatives) == len(values):
            raise ValueError(f"Length of given array should be {len(self.alternatives)}, rather than {len(values)}.")

        cri_names = self.get_criterions_names()

        if name in cri_names:
            raise ValueError(f"There is already criterion named {name}. Choose other name.")

        criterion = Criterion(name, ascending, criterion_type)
        self.criterions = np.insert(self.criterions, pos, criterion)
        self.impact_matrix = np.insert(self.impact_matrix, pos, values, axis=1)

    def delete_alternative(self, name):
        alt_names = self.get_alternatives_names()
        if name not in alt_names:
            raise ValueError(f"There is no alternative named {name}")

        pos = np.where(np.array(alt_names) == name)[0][0]
        self.alternatives = np.delete(self.alternatives, pos)
        self.impact_matrix = np.delete(self.impact_matrix, pos, axis=0)

    def delete_criterion(self, name):
        cri_names = self.get_criterions_names()
        if name not in cri_names:
            raise ValueError(f"There is no criterion named {name}")

        pos = np.where(np.array(cri_names) == name)[0][0]
        self.criterions = np.delete(self.criterions, pos)
        self.impact_matrix = np.delete(self.impact_matrix, pos, axis=1)

    def change_alternatives_name(self, old_name, new_name):
        alt_names = self.get_alternatives_names()
        if old_name not in alt_names:
            raise ValueError(f"There is no alternative named {old_name}")
        if new_name in alt_names:
            raise ValueError(f"There is alternative named {new_name}. Choose other name.")

        pos = np.where(np.array(alt_names) == old_name)[0][0]
        self.alternatives[pos].name = new_name

    def change_criterion_name(self, old_name, new_name):
        cri_names = self.get_criterions_names()
        if old_name not in cri_names:
            raise ValueError(f"There is no criterion named {old_name}")
        if new_name in cri_names:
            raise ValueError(f"There is criterion named {new_name}. Choose other name.")

        pos = np.where(np.array(cri_names) == old_name)[0][0]
        self.criterions[pos].name = new_name

    def get_alternatives_names(self):
        return [a.name for a in self.alternatives]

    def get_criterions_names(self):
        return [c.name for c in self.criterions]
