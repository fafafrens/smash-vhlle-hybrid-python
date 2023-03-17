import hybrid_lib as hl
import subprocess

def name_path_tree(dict_par,dict,cent):
	# function to name the path tree
	path_name = "system"+ dict["sNN"]+"centrality"+cent + "eta0" + dict["eta0"] + "ecrit" +dict_par["e_crit"] + "sigeta" + dict["sigmaeta"] + "w" + dict["w"] + "f" + dict["eff"]
	return path_name


test_values_etaS = ["0.12"]
test_values_ecrit = ["0.5"]
test_values_eta0 = ["4","4.5"]
test_values_sigEta = ["1","1.4"]

Nevents = 200
centrality="20-30"
icfile  = "/home/palermo/superMC/wouded_lhc5020_20-30%.data"

for EtaS in test_values_etaS:
	for Ecrit in test_values_ecrit:
		for Eta0 in test_values_eta0:
			for SEta in test_values_sigEta:
				copy_params = hl.params_modify(etaS=EtaS, e_crit=Ecrit)
				copy_superMC_setup = hl.supermc_modify(eta0=Eta0,sigmaeta=SEta)
				name_maindir = name_path_tree(copy_params,copy_superMC_setup,centrality)

				path_tree = hl.init(name_maindir)
				
				path_params_file = path_tree["hydro"] + "/params"
				path_glissando_file = path_tree["hydro"] + "/gliss"
				hl.print_dict_to_file(copy_params,path_params_file)
				hl.print_dict_to_file(copy_superMC_setup,path_glissando_file)

				hl.run_hybrid(path_params_file,path_glissando_file,icfile,name_maindir)
				hl.analysis_and_plots(name_maindir,Nevents)                  
				subprocess.run(["rm -r ",path_tree["hydro"],path_tree["sampler"],path_tree["after"]])
