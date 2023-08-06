import pandas as pd
import numpy as np
from .Alternative import Alternative
from .Criterion import Criterion
from .CriterionTri import CriterionTri
from .ImpactMatrix import ImpactMatrix
from .ImpactMatrixTri import ImpactMatrixTri
from .ProfileMatrix import ProfileMatrix
from .Profile import Profile


def create_impact_matrix_from_csv(filename_matrix,
                                  filename_criterion_data,
                                  filename_matrix_index_col: str = 'A',
                                  filename_criterion_data_index_col: str = 'I'):
    matrix = pd.read_csv(filename_matrix, index_col=filename_matrix_index_col)
    cri_information = pd.read_csv(filename_criterion_data, index_col=filename_criterion_data_index_col)

    raw_data = matrix.to_numpy()

    alt_names = matrix.index.values
    alternatives = [Alternative(a) for a in alt_names]
    criterions = [create_criterion(col, cri_information[col]) for col in matrix.columns]

    impact_matrix = ImpactMatrix(np.array(alternatives),
                                 np.array(criterions),
                                 raw_data)
    return impact_matrix


def create_tri_data(filename_matrix,
                    filename_criterion_data,
                    filename_b_data,
                    filename_q_data,
                    filename_p_data,
                    filename_v_data,
                    filename_matrix_index_col: str = 'A',
                    filename_criterion_data_index_col: str = 'I',
                    filename_b_data_col: str = 'C'):
    p = pd.read_csv(filename_p_data)
    q = pd.read_csv(filename_q_data)
    v = pd.read_csv(filename_v_data)
    matrix = pd.read_csv(filename_matrix, index_col=filename_matrix_index_col)
    cri_information = pd.read_csv(filename_criterion_data, index_col=filename_criterion_data_index_col)
    b = pd.read_csv(filename_b_data, index_col=filename_b_data_col)

    raw_data = matrix.to_numpy()

    alt_names = matrix.index.values
    alternatives = [Alternative(a) for a in alt_names]
    criterions = [create_tri_criterion(col,
                                       cri_information[col],
                                       q[col].values[0],
                                       p[col].values[0],
                                       v[col].values[0]) for col in b.index.values]

    impact_matrix = ImpactMatrixTri(alternatives, criterions, raw_data)

    raw_data_b = b.to_numpy()

    pro_names = b.columns
    profiles = [Profile(p) for p in pro_names]

    criterions = [create_tri_criterion(col,
                                       cri_information[col],
                                       q[col].values[0],
                                       p[col].values[0],
                                       v[col].values[0]) for col in b.index.values]

    profile_matrix = ProfileMatrix(profiles, criterions, raw_data_b)

    return impact_matrix, profile_matrix


def create_tri_criterion(name, cri_info, q, p, v):
    ascending = eval(cri_info["ascending"])
    criterion_type = cri_info["criterion_type"]
    cri = CriterionTri(name, q, p, v, ascending, criterion_type)
    return cri


def create_criterion(name, cri_info):
    ascending = bool(cri_info["ascending"])
    criterion_type = cri_info["criterion_type"]
    cri = Criterion(name, ascending, criterion_type)
    return cri
