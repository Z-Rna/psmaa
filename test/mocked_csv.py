from io import StringIO

mock_csv_data = StringIO(
    "A,C1,C2\n"
    "A1,100.0,9.0\n"
    "A2,120.0,7.0\n"
    "A3,150.0,2.0\n"
    "A4,110.0,5.0\n"
)

mock_csv_cri_info = StringIO(
    "I,C1,C2\n"
    "ascending,True,True\n"
    "criterion_type,cardinal\n"
)

mock_csv_data_2 = StringIO(
    "A,C1,C2\n"
    "A1,100.0,9.0\n"
    "A2,120.0,7.0\n"
    "A3,150.0,2.0\n"
    "A4,110.0,5.0\n"
)

mock_csv_cri_info_2 = StringIO(
    "I,C1,C2\n"
    "ascending,True,True\n"
    "criterion_type,cardinal\n"
)

mock_b_values = StringIO(
    "C,Cat1-Cat2,Cat2-Cat3\n"
    "C1,120.0,140.0\n"
    "C2,0.0,0.0\n"
)

mock_q_values = StringIO(
    "C1,C2\n"
    "10.0,1.0\n"
)

mock_p_values = StringIO(
    "C1,C2\n"
    "30.0,5.0\n"
)

mock_v_values = StringIO(
    "C1,C2\n"
    "40.0,6.0\n"
)