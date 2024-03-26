import hybrid_lib as hl 

input_dict = hl.get_input("input.txt")
outputfolder = input_dict["outputfolder"]
system = input_dict["system"]
param = input_dict["param"]
icfile = input_dict["icinput"]
Nevents = input_dict["Nevents"]

path_tree = hl.init(outputfolder)

hl.run_hybrid(param, system, icfile ,outputfolder,Nevents)
hl.analysis_and_plots(path_tree,Nevents)
