class ProfileMatrix:
    def __init__(self, profiles, criterions, categories, data):
        self.profiles = profiles
        self.criterions = criterions
        self.categories = categories
        self.data = data

    def get_profiles_name(self):
        return [p.name for p in self.profiles]

    def get_criterions_names(self):
        return [c.name for c in self.criterions]

    def get_categories_names(self):
        return [c.name for c in self.categories]

