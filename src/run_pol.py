import hybrid_lib as hl
input_dict = hl.get_input("input.txt")
path_tree = hl.init(input_dict["outputfolder"])
print(path_tree)
hl.run_pol(path_tree)