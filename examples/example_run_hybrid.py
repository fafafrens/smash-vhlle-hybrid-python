import hybrid_lib as hl

input_dict = hl.get_input("input_example.txt")
outputfolder = input_dict["outputfolder"]
system = input_dict["system"]
param = input_dict["param"]
icfile = input_dict["icinput"]
Nevents = input_dict["Nevents"]

path_tree = hl.init(outputfolder)

##runs the full hybrid chain                                                       
hl.run_hybrid(param, system, icfile,path_tree,Nevents)  
##to turn on polarization calculations, uncomment the appropriate line
##in the function run_hybrid of hybrid_lib