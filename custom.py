import hybrid_lib as hl

def name_path_tree(dict_par,dict_glis):
	# function to name the path tree
	path_name = "system"+ dict_glis["sNN"] + "etaS" + dict_par["etaS"] + "ecrit" +dict_par["e_crit"] + "eta0" + dict_glis["eta0"] + "sigEta" + dict_glis["sigEta"]
	return path_name


test_values_etaS = ["0.08","0.12","0.16"]
test_values_ecrit = ["0.3","0.45","0.5","0.6"]
test_values_eta0 = ["3","3.7","4","4.5"]
test_values_sigEta = ["1","1.4","2","2.5"]

Nevents = 1000
icfile  = "~/vhlle/ic/glissando/sources.LHC.20-50.dat"

for EtaS in test_values_etaS:
	for Ecrit in test_values_ecrit:
		for Eta0 in test_values_eta0:
			for SEta in test_values_sigEta:
				copy_params = hl.params_modify(etaS=EtaS, e_crit=Ecrit)
				copy_gliss_setup = hl.glissando_modify(eta0=Eta0,sigEta=SEta)
				name_maindir = name_path_tree(copy_params,copy_gliss_setup)

				path_tree = hl.init(name_maindir)
				
				path_params_file = path_tree["hydro"] + "/params"
				path_glissando_file = path_tree["hydro"] + "/gliss"
				hl.print_dict_to_file(copy_params,path_params_file)
				hl.print_dict_to_file(copy_gliss_setup,path_glissando_file)

				print("hl.run_hybrid("+path_params_file+","+path_glissando_file+","+icfile+","+"name_maindir"+")")
				print("hl.analysis_and_plots("+name_maindir+","+"Nevents"+")")                  
