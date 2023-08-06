from .Category import Category
from .CriterionTri import CriterionTri

class ProfileMatrix:
    def __init__(self, profiles, criterions, data):
        self.profiles = profiles
        self.criterions = criterions
        self.data = data

    def get_profiles_name(self):
        return [p.name for p in self.profiles]

    def get_criterions_names(self):
        return [c.name for c in self.criterions]

