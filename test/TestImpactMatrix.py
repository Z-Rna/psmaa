import unittest
import smaa
import numpy as np


class TestImpactMatrix(unittest.TestCase):

    def setUp(self):
        alt1 = smaa.Alternative("alt1")
        alt2 = smaa.Alternative("alt2")
        alt3 = smaa.Alternative("alt3")
        cri1 = smaa.Criterion("cri1")
        cri2 = smaa.Criterion("cri2")
        alternatives = np.array([alt1, alt2, alt3])
        criterions = np.array([cri1, cri2])
        data = np.array([[0.5, 15.0], [0.3, 16.0], [0.4, 14.0]], dtype=float)
        self.impact_matrix = smaa.ImpactMatrix(alternatives, criterions, data)

    def test_get_alternatives_names(self):
        alt_names = self.impact_matrix.get_alternatives_names()
        self.assertEqual(["alt1", "alt2", "alt3"], alt_names)  # add assertion here

    def test_get_criterions_names(self):
        cri_names = self.impact_matrix.get_criterions_names()
        self.assertEqual(["cri1", "cri2"], cri_names)

    def test_add_alternative_pass(self):
        alt_values = [0.4, 16.]
        alt_name = "alt4"
        alt_pos = 2
        self.impact_matrix.add_alternative(alt_values, alt_name, alt_pos)

        alt_names = self.impact_matrix.get_alternatives_names()
        data = np.array([[0.5, 15.0], [0.3, 16.0], [0.4, 16.], [0.4, 14.0]], dtype=float)

        self.assertEqual(alt_names[alt_pos], alt_name)
        self.assertEqual(["alt1", "alt2", "alt4", "alt3"], alt_names)
        self.assertTrue((data == self.impact_matrix.impact_matrix).all())

    def test_add_alternative_pass_fail_wrong_position(self):
        alt_values = [0.4, 16.]
        alt_name = "alt4"
        alt_pos = 5
        alt_names = self.impact_matrix.get_alternatives_names()
        alt_len = len(alt_names)

        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.add_alternative(alt_values, alt_name, alt_pos)
        self.assertEqual(str(ar.exception),
                         f"Given position: {alt_pos} is out of range: (0,{alt_len}).")
        self.assertEqual(alt_names, self.impact_matrix.get_alternatives_names())
        self.assertTrue(alt_name not in alt_names)

    def test_add_alternative_pass_fail_wrong_values(self):
        alt_values = [0.4, 16., 15.]
        alt_name = "alt4"
        alt_pos = 2
        cri_len = len(self.impact_matrix.get_criterions_names())

        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.add_alternative(alt_values, alt_name, alt_pos)
        self.assertEqual(str(ar.exception),
                         f"Length of given array should be {cri_len}, rather than {len(alt_values)}.")

    def test_add_alternative_pass_fail_wrong_name(self):
        alt_values = [0.4, 16.]
        alt_name = "alt1"
        alt_pos = 2

        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.add_alternative(alt_values, alt_name, alt_pos)
        self.assertEqual(str(ar.exception),
                         f"There is already alternative named {alt_name}. Choose other name.")

    def test_change_alternatives_name_pass(self):
        alt_name_old = "alt1"
        alt_name_new = "alt1_change"
        self.impact_matrix.change_alternatives_name(alt_name_old, alt_name_new)
        alt_names = self.impact_matrix.get_alternatives_names()
        self.assertEqual(["alt1_change", "alt2", "alt3"], alt_names)

    def test_change_alternatives_name_fail_wrong_old_name(self):
        alt_name_old = "alt_wrong"
        alt_name_new = "alt1_change"
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.change_alternatives_name(alt_name_old, alt_name_new)
        self.assertEqual(str(ar.exception),
                         f"There is no alternative named {alt_name_old}")

    def test_change_alternatives_name_fail_wrong_new_name(self):
        alt_name_old = "alt1"
        alt_name_new = "alt2"
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.change_alternatives_name(alt_name_old, alt_name_new)
        self.assertEqual(str(ar.exception),
                         f"There is alternative named {alt_name_new}. Choose other name.")

    def test_delete_alternative_pass(self):
        alt_name = "alt1"
        alt_names = self.impact_matrix.get_alternatives_names()
        impact_matrix_values = np.array([[0.3, 16.0], [0.4, 14.0]], dtype=float)

        self.impact_matrix.delete_alternative(alt_name)

        new_alt_names = self.impact_matrix.get_alternatives_names()
        new_impact_matrix_values = self.impact_matrix.impact_matrix

        self.assertNotEqual(alt_names, new_alt_names)
        self.assertEqual(alt_names[1:], new_alt_names)
        self.assertTrue((impact_matrix_values == new_impact_matrix_values).all())

    def test_test_delete_alternative_fail_wrong_name(self):
        alt_name = "alt_wrong"
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.delete_alternative(alt_name)
        self.assertEqual(str(ar.exception),
                         f"There is no alternative named {alt_name}")

    def test_add_criterion_pass(self):
        cri_values = [160., 150., 140.]
        cri_name = "cri3"
        cri_pos = 1

        self.impact_matrix.add_criterion(cri_values, cri_name, "", cri_pos)

        cir_names = self.impact_matrix.get_criterions_names()
        data = np.array([[0.5, 160., 15.0], [0.3, 150.0, 16.0], [0.4, 140., 14.0]], dtype=float)

        self.assertEqual(cir_names[cri_pos], cri_name)
        self.assertEqual(["cri1", "cri3", "cri2"], cir_names)
        self.assertTrue((data == self.impact_matrix.impact_matrix).all())

    def test_add_criterion_fail_wrong_wrong_position(self):
        cri_values = [160., 150., 140.]
        cri_name = "cri3"
        cri_pos = 4
        cri_names = self.impact_matrix.get_criterions_names()
        cri_len = len(cri_names)
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.add_criterion(cri_values, cri_name, "", cri_pos)
        self.assertEqual(str(ar.exception),
                         f"Given position is out of range: (0,{cri_len})")
        self.assertEqual(cri_names, self.impact_matrix.get_criterions_names())
        self.assertTrue(cri_name not in cri_names)

    def test_add_criterion_fail_wrong_values(self):
        cri_values = [160., 150., 140., 130.]
        cri_name = "cri3"
        cri_pos = 1
        alt_len = len(self.impact_matrix.get_alternatives_names())

        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.add_criterion(cri_values, cri_name, "", cri_pos)
        self.assertEqual(str(ar.exception),
                         f"Length of given array should be {alt_len}, rather than {len(cri_values)}.")

    def test_add_criterion_fail_wrong_name(self):
        cri_values = [160., 150., 140.]
        cri_name = "cri1"
        cri_pos = 1

        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.add_criterion(cri_values, cri_name, "", cri_pos)

        self.assertEqual(str(ar.exception),
                         f"There is already criterion named {cri_name}. Choose other name.")

    def test_change_criterion_name_pass(self):
        cri_name_old = "cri1"
        cri_name_new = "cri1_change"
        self.impact_matrix.change_criterion_name(cri_name_old, cri_name_new)
        cri_names = self.impact_matrix.get_criterions_names()
        self.assertEqual(["cri1_change", "cri2"], cri_names)

    def test_change_criterion_name_fail_wrong_old_name(self):
        cri_name_old = "cri_wrong"
        cri_name_new = "cri1_change"
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.change_criterion_name(cri_name_old, cri_name_new)
        self.assertEqual(str(ar.exception),
                         f"There is no criterion named {cri_name_old}")

    def test_change_criterion_name_fail_wrong_new_name(self):
        cri_name_old = "cri1"
        cri_name_new = "cri2"
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.change_criterion_name(cri_name_old, cri_name_new)
        self.assertEqual(str(ar.exception),
                         f"There is criterion named {cri_name_new}. Choose other name.")

    def test_delete_criterion_pass(self):
        cri_name = "cri1"
        cri_names = self.impact_matrix.get_criterions_names()
        impact_matrix_values = np.array([[15.0], [16.0], [14.0]], dtype=float)

        self.impact_matrix.delete_criterion(cri_name)

        new_cri_names = self.impact_matrix.get_criterions_names()
        new_impact_matrix_values = self.impact_matrix.impact_matrix

        self.assertNotEqual(cri_names, new_cri_names)
        self.assertEqual(cri_names[1:], new_cri_names)
        self.assertTrue((impact_matrix_values == new_impact_matrix_values).all())

    def test_delete_criterion_fail_wrong_name(self):
        cri_name = "cri_wrong"
        with self.assertRaises(ValueError) as ar:
            self.impact_matrix.delete_criterion(cri_name)
        self.assertEqual(str(ar.exception),
                         f"There is no criterion named {cri_name}")


if __name__ == '__main__':
    unittest.main()
