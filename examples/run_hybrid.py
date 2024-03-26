import hybrid_lib as hl 

input_dict = hl.get_input("input_example.txt") ##text file containing the information to run the full hybrid
outputfolder = input_dict["outputfolder"]
system = input_dict["system"]
param = input_dict["param"]
icfile = input_dict["icinput"]
Nevents = input_dict["Nevents"]

path_tree = hl.init(outputfolder)

hl.run_hybrid(param, system, icfile ,outputfolder,Nevents) ##runs a single hybrid based on the info in the input file

