import hybrid_lib as hl
import subprocess

def name_path_tree(dict_par,dict,cent):
	'''function to name the path tree'''
	path_name = "system"+ dict["sNN"]+"centrality"+cent + "eta0" + dict["eta0"] + "ecrit" +dict_par["e_crit"] + "sigeta" + dict["sigmaeta"] + "w" + dict["w"] + "f" + dict["eff"]
	return path_name

##You want to run simulations with different values of some parameters for the superMC and params dictionaries
## Here you put the values you want to test. It can be a long list...

##params_dict
values_etaS = ["0.12"] 
values_ecrit = ["0.5"]

##superMC_dict
values_eta0 = ["4","4.5"]
values_sigEta = ["1","1.4"]

##Here go other info, as the Number of events to sample from the particlization hypersup
##the location of the initial condition file and additional strings to name the path of the output
Nevents = 200 ##Number of events
icfile  = "/home/palermo/superMC/wouded_lhc5020_20-30%.data" ##Path to initial state data

centrality="20-30" ##miscellania

for EtaS in values_etaS:
	for Ecrit in values_ecrit:
		for Eta0 in values_eta0:
			for SEta in values_sigEta:
				copy_params = hl.params_modify(etaS=EtaS, e_crit=Ecrit) ##return a copy of the params dictionary with modified entries according to the list.
				copy_superMC_setup = hl.supermc_modify(eta0=Eta0,sigmaeta=SEta)  ##return a copy of the superMC dictionary with modified entries according to the list.
				name_maindir = name_path_tree(copy_params,copy_superMC_setup,centrality)

				path_tree = hl.init(name_maindir) ##creates a path tree with the various directories for hydro, particlization, Afterburning, ecc
				
				path_params_file = path_tree["hydro"] + "/params"
				path_supermc_file = path_tree["hydro"] + "/supermc"
				hl.print_dict_to_file(copy_params,path_params_file) ##save new params dict to file for vhlle to read
				hl.print_dict_to_file(copy_superMC_setup,path_supermc_file) ##save new supermc dict to file for vhlle to read

				hl.run_hybrid(path_params_file,path_supermc_file,icfile,name_maindir) ##runs the hbryd model in the path tree
				
				# subprocess.run(["rm -r ",path_tree["hydro"],path_tree["sampler"],path_tree["after"]]) ##UNCOMMENT if you want to remove these folders
