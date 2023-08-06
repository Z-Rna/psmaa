if __name__ == '__main__':
    from smaa import create_tri_data, SMAATri, no_preference

    data_matrix, b = create_tri_data("data_electre/matrix.csv",
                                     "data_electre/cri_info.csv",
                                     "data_electre/b_values.csv",
                                     "data_electre/q_values.csv",
                                     "data_electre/p_values.csv",
                                     "data_electre/v_values.csv")

    model = SMAATri(data_matrix, b, 0.65)

    h = model.compute_category_acceptability_indices(no_preference)
    print(h)

