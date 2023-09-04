import unittest
import src
import numpy as np
import mocked_csv

class TestDatautils(unittest.TestCase):

    def setUp(self):
        alt1 = src.Alternative("A1")
        alt2 = src.Alternative("A2")
        alt3 = src.Alternative("A3")
        alt4 = src.Alternative("A4")
        self.alternatives = np.array([alt1, alt2, alt3, alt4])
        self.data = np.array([[100.0, 9.0], [120.0, 7.0], [150.0, 2.0], [110.0, 5.0]], dtype=float)

    def test_create_impact_matrix_from_csv(self):
        cri1 = src.Criterion("C1")
        cri2 = src.Criterion("C2")
        criterions = np.array([cri1, cri2])
        impact_matrix = src.ImpactMatrix(self.alternatives, criterions, self.data)

        result = src.create_impact_matrix_from_csv(mocked_csv.mock_csv_data, mocked_csv.mock_csv_cri_info)

        alt_names = impact_matrix.get_alternatives_names()
        cri_names = impact_matrix.get_criterions_names()

        self.assertEqual(result.get_alternatives_names(), alt_names)
        self.assertEqual(result.get_criterions_names(), cri_names)
        np.testing.assert_allclose(result.impact_matrix, impact_matrix.impact_matrix)

    def test_create_tri_data(self):
        cri1 = src.CriterionTri("C1",10.,30.,40.)
        cri2 = src.CriterionTri("C2",1.,5., 60.)
        cat1 = src.Category("Cat1")
        cat2 = src.Category("Cat2")
        cat3 = src.Category("Cat3")
        pro1 = src.Profile("Cat1-Cat2")
        pro2 = src.Profile("Cat2-Cat3")
        criterions = np.array([cri1, cri2])
        catregories = np.array([cat1, cat2, cat3])
        profiles = np.array([pro1, pro2])
        profile_data = np.array([[120.0,140.0], [0.0,0.0]], dtype=float)
        impact_matrix = src.ImpactMatrixTri(self.alternatives, criterions, self.data)
        profile_matrix = src.ProfileMatrix(profiles,criterions,catregories,profile_data)

        result_im, result_pm = src.create_tri_data(mocked_csv.mock_csv_data_2, mocked_csv.mock_csv_cri_info_2,
                                     mocked_csv.mock_b_values, mocked_csv.mock_q_values, mocked_csv.mock_p_values,
                                     mocked_csv.mock_v_values)

        alt_names = result_im.get_alternatives_names()
        cri_names = result_im.get_criterions_names()
        pro_names = result_pm.get_profiles_name()
        cat_names = result_pm.get_categories_names()

        self.assertEqual(result_im.get_alternatives_names(), alt_names)
        self.assertEqual(result_im.get_criterions_names(), cri_names)
        self.assertEqual(result_pm.get_profiles_name(), pro_names)
        self.assertEqual(result_pm.get_categories_names(), cat_names)
        np.testing.assert_allclose(result_im.impact_matrix, impact_matrix.impact_matrix)
        np.testing.assert_allclose(result_pm.data, profile_matrix.data)


if __name__ == '__main__':
    unittest.main()
