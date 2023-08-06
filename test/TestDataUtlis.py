import unittest
import smaa
from io import StringIO
import numpy as np


class TestDatautils(unittest.TestCase):
    def setUp(self):
        self.mock_csv_data = StringIO(
            "A,C1,C2\n"
            "A1,0.5,15.0\n"
            "A2,0.3,16.0\n"
            "A3,0.4,14.0\n"
        )
        self.mock_csv_cri_info = StringIO(
            "I,C1,C2\n"
            "ascending,True,True\n"
            "criterion_type,cardinal\n"
        )

    def test_create_impact_matrix_from_csv(self):
        alt1 = smaa.Alternative("alt1")
        alt2 = smaa.Alternative("alt2")
        alt3 = smaa.Alternative("alt3")
        cri1 = smaa.Criterion("cri1")
        cri2 = smaa.Criterion("cri2")
        alternatives = np.array([alt1, alt2, alt3])
        criterions = np.array([cri1, cri2])
        data = np.array([[0.5, 15.0], [0.3, 16.0], [0.4, 14.0]], dtype=float)
        impact_matrix = smaa.ImpactMatrix(alternatives, criterions, data)

        result = smaa.create_impact_matrix_from_csv(self.mock_csv_data, self.mock_csv_cri_info)

        a = 15



if __name__ == '__main__':
    unittest.main()
