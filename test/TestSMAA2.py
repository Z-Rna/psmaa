import unittest

import numpy as np

import src


class TestSMAA2(unittest.TestCase):

    def setUp(self):
        alt1 = src.Alternative("alt1")
        alt2 = src.Alternative("alt2")
        alt3 = src.Alternative("alt3")
        cri1 = src.Criterion("cri1")
        cri2 = src.Criterion("cri2")
        alternatives = np.array([alt1, alt2, alt3])
        criterions = np.array([cri1, cri2])
        data = np.array([[0.5, 15.0], [0.3, 16.0], [0.4, 14.0]], dtype=float)
        impact_matrix = src.ImpactMatrix(alternatives, criterions, data)
        self.smaa2 = src.SMAA2(impact_matrix)

    def test_partial_utility_matrix(self):
        partial_utility_matrix = np.array([[1., 0.5], [0., 1.], [0.5, 0.]])
        result = self.smaa2.partial_utility_matrix()

        np.testing.assert_allclose(partial_utility_matrix, result)

    def test_compute_w_c_and_b_no_preference_pass(self):
        w_c = np.array([[0.66709716, 0.33290284], [0.16910029, 0.83089971], [0., 0.]])
        b = np.array([[0.6664, 0.3336, 0.], [0.3336, 0.3334, 0.333], [0., 0.333, 0.667]])

        self.smaa2.compute_w_c_and_b(src.no_preference)

        np.testing.assert_allclose(w_c, self.smaa2.w_c, atol=0.01)
        np.testing.assert_allclose(b, self.smaa2.b, atol=0.01)

    def test_compute_w_c_and_b_ordinal_preference_pass(self):
        w_c = np.array([[0.75029038, 0.24970962], [0., 0.], [0., 0.]])
        b = np.array([[1., 0., 0.], [0., 0.3334, 0.6666], [0., 0.6666, 0.3334]])

        self.smaa2.compute_w_c_and_b(src.ordinal_preference, [1, 2])

        np.testing.assert_allclose(w_c, self.smaa2.w_c, atol=0.01)
        np.testing.assert_allclose(b, self.smaa2.b, atol=0.01)

    def test_compute_w_c_and_b_ordinal_preference_wrong_preference_vector(self):
        w_c = None
        b = None

        self.smaa2.compute_w_c_and_b(src.ordinal_preference, [1, 2, 3])

        self.assertEqual(w_c, self.smaa2.w_c)
        self.assertEqual(b, self.smaa2.b)

    def test_compute_w_c_and_b_cardinal_preference_pass(self):
        w_c = np.array([[0.6, 0.4], [0., 0.], [0., 0.]])
        b = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])

        self.smaa2.compute_w_c_and_b(src.cardinal_preference, [[0.6], [0.4]])
        np.testing.assert_allclose(w_c, self.smaa2.w_c, atol=0.01)
        np.testing.assert_allclose(b, self.smaa2.b, atol=0.01)

    def test_compute_w_c_and_b_cardinal_preference_wrong_preference_vector(self):
        w_c = None
        b = None

        self.smaa2.compute_w_c_and_b(src.cardinal_preference, [[0.6], [0.3], [0.1]])
        self.assertEqual(w_c, self.smaa2.w_c)
        self.assertEqual(b, self.smaa2.b)

    def test_compute_w_c_and_b_cardinal_preference_wrong_interval(self):
        w_c = None
        b = None

        self.smaa2.compute_w_c_and_b(src.cardinal_preference, [[0.6, 0.4], [0.5, 0.5]])
        self.assertEqual(w_c, self.smaa2.w_c)
        self.assertEqual(b, self.smaa2.b)

    def test_compute_w_c_and_b_cardinal_preference_wrong_lower_bounds(self):
        w_c = None
        b = None

        self.smaa2.compute_w_c_and_b(src.cardinal_preference, [[0.6, 0.8], [0.5, 0.9]])
        self.assertEqual(w_c, self.smaa2.w_c)
        self.assertEqual(b, self.smaa2.b)

    def test_compute_w_c_and_b_cardinal_preference_wrong_no_return_value(self):
        w_c = None
        b = None

        self.smaa2.compute_w_c_and_b(src.cardinal_preference, [[0.1, 0.1], [0.8, 0.9]])
        self.assertEqual(w_c, self.smaa2.w_c)
        self.assertEqual(b, self.smaa2.b)

    def test_compute_p_pass(self):
        self.smaa2.w_c = np.array([[0.6, 0.4], [0., 0.], [0., 0.]])
        p = np.array([1., 1., 1.])

        self.smaa2.compute_p()

        np.testing.assert_allclose(p, self.smaa2.p, atol=0.01)

    def test_compute_p_wrong_wc(self):
        self.smaa2.w_c = None
        p = None

        self.smaa2.compute_p()

        self.assertEqual(p, self.smaa2.p)

if __name__ == '__main__':
    unittest.main()
