import hybrid_lib as hl 
import sys 


if len(sys.argv)==0:
        input_dict = hl.get_input()
else:
        input_dict = hl.get_input(sys.argv[1])
outputfolder = input_dict["outputfolder"]
system = input_dict["system"]
param = input_dict["param"]
icfile = input_dict["icfile"]
Nevents = input_dict["Nevents"]

hl.run_hybrid(param, system, icfile ,outputfolder,Nevents)