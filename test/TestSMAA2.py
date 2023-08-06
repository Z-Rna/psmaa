import unittest
import numpy as np
import smaa


class TestSMAA2(unittest.TestCase):

    def setUp(self):
        alt1 = smaa.Alternative("alt1")
        alt2 = smaa.Alternative("alt2")
        alt3 = smaa.Alternative("alt3")
        cri1 = smaa.Criterion("cri1")
        cri2 = smaa.Criterion("cri2")
        alternatives = np.array([alt1, alt2, alt3])
        criterions = np.array([cri1, cri2])
        data = np.array([[0.5, 15.0], [0.3, 16.0], [0.4, 14.0]], dtype=float)
        impact_matrix = smaa.ImpactMatrix(alternatives, criterions, data)
        self.smaa2 = smaa.SMAA2(impact_matrix)

    def test_partial_utility_matrix(self):
        partial_utility_matrix = np.array([[1.,0.5], [0., 1.], [0.5, 0.]])
        result = self.smaa2.partial_utility_matrix()
        self.assertTrue(np.allclose(partial_utility_matrix, result))

    def test_monte_carlo_simulation(self):
        '''problem ze stablinością symulacji mimo 10000 symulacji - do zbadania'''
        pass

    def test_compute_w_c_and_b(self):
        pass

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
