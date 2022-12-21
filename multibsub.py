import hybrid_lib as hl
import os
import numpy as np

input_folder = "./list_runs"
input_run_names = os.listdir(input_folder)

input_run_path = input_folder +"/"+ np.array(input_run_names)

len(input_run_path)