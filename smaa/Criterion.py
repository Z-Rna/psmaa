class Criterion:
    def __init__(self, name, ascending=True, criterion_type="cardinal"):
        self.name: str = name
        self.ascending: bool = ascending
        self.criterion_type = criterion_type
