from src import create_tri_data, SMAATri, no_preference
from time import time

im, pm = create_tri_data('data_electre/matrix.csv','data_electre/cri_info.csv', 'data_electre/b_values.csv',
                         'data_electre/q_values.csv', 'data_electre/p_values.csv', 'data_electre/v_values.csv')

model = SMAATri(im, pm, [0.5,1.0])

t = time()
model.compute_pi(no_preference)
print(f"time: {time()-t}\n {model.pi}")

model = SMAATri(im, pm, [0.5,1.0])

t = time()
model.compute_pi(no_preference)
print(f"time: {time()-t}\n {model.pi}")

