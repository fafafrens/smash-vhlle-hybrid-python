import hybrid_lib as hl

def name_path_tree(dict_par,dict_glis,cent):
	# function to name the path tree
	path_name = "system"+ dict_glis["sNN"]+"centrality"+cent + "etaS" + dict_par["etaS"] + "ecrit" +dict_par["e_crit"] + "eta0" + dict_glis["eta0"] + "sigEta" + dict_glis["sigEta"]
	return path_name


test_values_etaS = ["0.08","0.12","0.16"]
test_values_ecrit = ["0.5"]
test_values_eta0 = ["3.7"]
test_values_sigEta = ["1.4"]

Nevents = 1000
centrality="20-50"
icfile  = "/home/palermo/vhlle/ic/glissando/sources.LHC."+centrality+".dat"

for EtaS in test_values_etaS:
	for Ecrit in test_values_ecrit:
		for Eta0 in test_values_eta0:
			for SEta in test_values_sigEta:
				copy_params = hl.params_modify(etaS=EtaS, e_crit=Ecrit)
				copy_gliss_setup = hl.glissando_modify(eta0=Eta0,sigEta=SEta)
				name_maindir = name_path_tree(copy_params,copy_gliss_setup,centrality)

				path_tree = hl.init(name_maindir)
				
				path_params_file = path_tree["hydro"] + "/params"
				path_glissando_file = path_tree["hydro"] + "/gliss"
				hl.print_dict_to_file(copy_params,path_params_file)
				hl.print_dict_to_file(copy_gliss_setup,path_glissando_file)

				hl.run_hybrid(path_params_file,path_glissando_file,icfile,name_maindir)
				hl.analysis_and_plots(name_maindir,Nevents)                  
				subprocess.run(["rm -r ",path_tree["hydro"],path_tree["sampler"],path_tree["after"]])
