from .ImpactMatrix import ImpactMatrix

class ImpactMatrixTri(ImpactMatrix):
    def __init__(self, alternatives, criterions, data):
        super().__init__(alternatives, criterions, data)