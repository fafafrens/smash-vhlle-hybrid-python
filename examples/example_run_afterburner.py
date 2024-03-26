import hybrid_lib as hl

input_dict = hl.get_input("input_example.txt")
outputfolder = input_dict["outputfolder"]
system = input_dict["system"]
param = input_dict["param"]
icfile = input_dict["icinput"]
Nevents = input_dict["Nevents"]

path_tree = hl.init(outputfolder)

hl.write_sampler_config(param,path_tree,Nevents)
hl.run_afterburner(path_tree) ##runs only the sampler and afterburning stage. 
                                #the hydro stage is assumed to be over and to be
                                # in the same path tree as you want to write the
                                # sampling and afterburning
