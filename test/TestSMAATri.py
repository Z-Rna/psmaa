import unittest
import src
import numpy as np


class TestSMAATri(unittest.TestCase):

    def setUp(self):
        alt1 = src.Alternative("alt1")
        alt2 = src.Alternative("alt2")
        alt3 = src.Alternative("alt3")
        cri1 = src.CriterionTri("cri1", 0.1, 0.15, 0.2)
        cri2 = src.CriterionTri("cri2", 1., 2., 5.)
        cat1 = src.Category("Cat1")
        cat2 = src.Category("Cat2")
        pro1 = src.Profile("Cat1-Cat2")
        alternatives = np.array([alt1, alt2, alt3])
        criterions = np.array([cri1, cri2])
        catregories = np.array([cat1, cat2])
        profiles = np.array([pro1])
        data = np.array([[0.5, 15.0], [0.3, 16.0], [0.4, 14.0]], dtype=float)
        profile_data = np.array([[120.0, 140.0], [0.0, 0.0]], dtype=float)
        impact_matrix = src.ImpactMatrixTri(alternatives, criterions, data)
        profile_matrix = src.ProfileMatrix(profiles, criterions, catregories, profile_data)
        lambda_value = [0.5,1.]

        self.model = src.SMAATri(impact_matrix,profile_matrix,lambda_value)

    def test_compute_pi_no_preference_pass(self):
        pi = np.array([[0., 0., 1.], [0., 0., 1.], [0., 0., 1.]])

        self.model.compute_pi(src.no_preference)
        np.testing.assert_allclose(pi, self.model.pi, atol=0.01)

    def test_compute_pi_wrong_lambda(self):
        pi = None

        self.model.lambda_value = np.array([0.8,0.5])
        self.model.compute_pi(src.no_preference)
        self.assertEqual(pi, self.model.pi)

    def test_compute_pi_ordinal_preference_pass(self):
        pi = np.array([[0., 0., 1.], [0., 0., 1.], [0., 0., 1.]])

        self.model.compute_pi(src.ordinal_preference, [2,1])
        np.testing.assert_allclose(pi, self.model.pi, atol=0.01)

    def test_compute_pi_ordinal_preference_wrong_preference_vector(self):
        pi = None

        self.model.compute_pi(src.ordinal_preference, [2, 1, 3])
        self.assertEqual(pi, self.model.pi)

    def test_compute_pi_cardinal_preference_pass(self):
        pi = np.array([[0., 0., 1.], [0., 0., 1.], [0., 0., 1.]])

        self.model.compute_pi(src.cardinal_preference, [[0.6], [0.4]])
        np.testing.assert_allclose(pi, self.model.pi, atol=0.01)

    def test_compute_pi_cardinal_preference_wrong_preference_vector(self):
        pi = None

        self.model.compute_pi(src.cardinal_preference, [[1.0]])
        self.assertEqual(pi, self.model.pi)

    def test_compute_pi_cardinal_preference_wrong_interval(self):
        pi = None

        self.model.compute_pi(src.cardinal_preference, [[0.6,0.4], [0.5, 0.5]])
        self.assertEqual(pi, self.model.pi)

    def test_compute_pi_cardinal_preference_wrong_no_return_valuel(self):
        pi = None

        self.model.compute_pi(src.cardinal_preference, [[0.1, 0.1], [0.8, 0.9]])
        self.assertEqual(pi, self.model.pi)





if __name__ == '__main__':
    unittest.main()
