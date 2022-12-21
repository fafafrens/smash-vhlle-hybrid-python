import hybrid_lib as hl
import sys

input_dict = hl.get_input("input.txt")
path_tree = hl.init(input_dict["outputfolder"])
Nevents =  input_dict["Nevents"]

hl.analysis_and_plots(path_tree,Nevents)