import hybrid_lib as hl

input_dict = hl.get_input("input.txt")
outputfolder = input_dict["outputfolder"]
system = input_dict["system"]
param = input_dict["param"]
icfile = input_dict["icinput"]
Nevents = input_dict["Nevents"]

path_tree = hl.init(outputfolder)

hl.write_sampler_config(param,path_tree,Nevents)
hl.run_sampler(path_tree)
hl.write_afterburn_config(path_tree,Nevents)
hl.run_smash(path_tree)

