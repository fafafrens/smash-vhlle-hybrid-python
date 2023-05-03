import subprocess
import sys

#syntax to move the files from terminal $: python3 move_to_hyb_folder.py <path_to_hybrid_folder>
target_directory = sys.argv[1]

#The directory containing smash, smash-hadron-smapler, vhlle, smash-vhlle-hybrid-python.
work_directory = '~'

print("Friendly reminder: have you compiled the correct branches? If so, good for you :D")

subprocess.run(["cp",f"{work_directory}/smash/build/smash",target_directory])
subprocess.run(["cp",f"{work_directory}/super-vhlle/hlle_visc",target_directory])
subprocess.run(["cp",f"{work_directory}/smash-hadron-sampler/build/sampler",target_directory])
subprocess.run(["cp","./hybrid_lib.py",target_directory])
subprocess.run(["cp","./Snakefile",target_directory])
subprocess.run(["cp","./Snakefile_polarization",target_directory])
subprocess.run(["cp","./plot_lib.py",target_directory])