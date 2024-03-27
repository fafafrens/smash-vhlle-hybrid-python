import subprocess
import sys

### Use this script to move all the useful files from this repo 
### and the executable from smash, vhlle, smash-hadron-sampler to your desired 
### location, which we'll refer as ''target directory'' (i.e. where you want to
### have the hybrid model working) 

# Directory where you want the hybrid to work
target_directory = ""

#The directory containing the folders: smash, smash-hadron-smapler, vhlle, and this repo.
work_directory = '/home/'

print("Copying...")
try:
    subprocess.run(["cp",f"{work_directory}/smash/build/smash",target_directory])
    subprocess.run(["cp",f"{work_directory}/super-vhlle/hlle_visc",target_directory])
    subprocess.run(["cp",f"{work_directory}/smash-hadron-sampler/build/sampler",target_directory])
    subprocess.run(["cp","./hybrid_lib.py",target_directory])
    subprocess.run(["cp","../Snakefile",target_directory])
    subprocess.run(["cp","../Snakefile_centrality",target_directory])
    subprocess.run(["cp","./plot_lib.py",target_directory])
    print("Done!")
    print("Friendly reminder: have you compiled the correct branches? If so, good for you :D")

except:
    print("An error occurred! Check the paths in 'move_to_hyb_folder.py'.")