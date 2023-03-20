import subprocess
import os 
import yaml

# param="file di configurazione iuri"
# sytem=" striga oscura di iurii"
# icfile="file condizioni iniziali oscure di iurri"
# outputfolder="abbasta chiaro"
# n_event=100

params_dict = {
"outputDir"     :   "none",
"eosType"       :   "0",           
"etaS"          :   "0.12",            #  eta/s value
"zetaS"         :   "0.0",             #  zeta/s, bulk viscosity
"e_crit"        :   "0.515",           #  criterion for surface finding
"zetaSparam"    :   "3",               #  0 basic param (is zetaS 0 no bulk), 1,2,3
"nx"            :   "101",             # number of cells in X direction
"ny"            :   "101",             # number of cells in Y direction
"nz"            :   "51",              # number of cells in eta direction
"xmin"          :   "-20.0",           # coordinate of the first cell
"xmax"          :   "20.0",            # coordinate of the last cell
"ymin"          :   "-20.0",
"ymax"          :   "20.0",
"etamin"        :   "-10.0",
"etamax"        :   "10.0",
"icModel"       :   "8",
"glauberVar"    :   "1",       	      #not used
"icInputFile"   :   "ic/glissando/sources.RHIC.20-50.dat",
"s0ScaleFactor" :   "53.55",	      #not used in glissando (glauber + rapidity)
"epsilon0"      :   "30.0",	      #not used in glissando (glauber)
"impactPar"     :   "7.0",	      #not used in glissando (glauber)
"alpha"         :   "0.0",             #NEVER used
"tau0"          :   "0.6",  	      # starting proper time
"tauMax"        :   "15.0",  	      # proper time to stop hydro
"dtau"          :   "0.1"   	      # timestep
}


glissando_dict = {
	"sNN"      : "5020",
	"eta0"     : "3.7", #/2.3 // midrapidity plateau
  	"sigEta"   : "1.4", # diffuseness of rapidity profile
  	"etaM"     : "4.5",
  	"ybeam"    : "8.585", # beam rapidity
  	"alphaMix" : "0.15", # WN/binary mixing
  	"Rg"	   : "0.4", # Gaussian smearing in transverse dir
  	"A" 	   : "0.0",  # 5e-4; // initial shear flow
  	"neta0"	   : "0.0" 
}

supermc_dict = {
	"sNN"      : "5020",
	"eta0"     : "3.5", # midrapidity plateau
  	"sigmaeta" : "1.4", # diffuseness of rapidity profile
  	"w"	   : "0.4",
  	"eff"	   : "0.15" 
}

input_dict = {
        "param" : "vhlle param file (-param)",
        "system" : "vhlle collision system (-system)",
        "icinput" : "initial condition file in vhlle (-ISinput)",
        "outputfolder" : "master output folder, base of the path three",
        "Nevents" : 100
}

sampler_config = {
        "surface"          : "/path/to/freezeout/surface",
        "spectra_dir"      : " /path/to/output",
        "number_of_events" : 100,
        "weakContribution" : 0,
        "shear"            : 1,
        "ecrit"            : 0.5
}

smash_yaml_config={
        'Version': 1.8,
        'Logging': {'default': 'INFO'},
        'General': {'Modus': 'List',
        'Time_Step_Mode': 'None',
        'Delta_Time': 0.1,
        'End_Time': 100.0,
        'Randomseed': -1,
        'Nevents': 100},
        'Output': {'Particles': {'Format': ['Binary', 'Oscar2013']}},
        'Modi': {'List': {'File_Directory': '../build/',
        'File_Prefix': 'sampling',
        'Shift_Id': 0}}
}

def params_modify(**kwargs):
	dict2 = params_dict.copy()
	for v, k in kwargs.items():
		dict2[v] = k
	return dict2

def glissando_modify(**kwargs):
        dict2 = glissando_dict.copy()
        for v, k in kwargs.items():
                dict2[v] = k
        return dict2

def supermc_modify(**kwargs):
        dict2 = supermc_dict.copy()
        for v, k in kwargs.items():
                dict2[v] = k
        return dict2

def get_input(input_file):
        d = {}
        with open(input_file) as f:
                lines = (line.rstrip() for line in f) # All lines including the blank ones
                lines = (line for line in lines if line) # Non-blank lines
                for line in lines:
                        if line:
                                key = line.split()[0]
                                val =  line.split()[1]
                                d[key] = val
        return d

def init(output_main):
        path_tree_dict={}
        hydropath = "./"+output_main + "/Hydro"
        samplerpath = "./"+output_main + "/Sampler"
        afterpath = "./"+output_main + "/Afterburner"
        plotspath = "./"+output_main + "/Plots"
        polpath = "./"+output_main + "/Polarization"
        keys = ["hydro","sampler","after","plots","pol"]
        values = [hydropath,samplerpath,afterpath,plotspath,polpath]
        try:
                os.mkdir(output_main)
                for i,j in zip(keys,values):
                        os.mkdir(j)
                        path_tree_dict[i]=j
                return path_tree_dict
        except:
                for i,j in zip(keys,values):
                        path_tree_dict[i]=j
                return path_tree_dict

def run_vhlle(param,system,icfile,path_tree):
        try:
                subprocess.run(["./hlle_visc", "-system", system, "-params",param,"-ISinput",icfile,"-outputDir",path_tree["hydro"]])
        except:
                print("ERROR: something went wrong running vHLLE.")


def print_dict_to_file(dict,output):
    with open(output, 'w') as f: 
        for key, value in dict.items(): 
            f.write('%s    %s\n' % (key, value))

def read_param(param_file):
        d = {}
        with open(param_file) as f:
                lines = (line.rstrip() for line in f) # All lines including the blank ones
                lines = (line for line in lines if line) # Non-blank lines
                for line in lines:
                        if line:
                                key = line.split()[0]
                                val =  line.split()[1]
                                d[key] = val
        return d

def write_sampler_config(param,path_tree,Nevent=sampler_config.copy()["number_of_events"],dict_sampler_config=sampler_config.copy()): 
        dict = read_param(param)
        dict_sampler_config["ecrit"] = dict["e_crit"]
        dict_sampler_config["surface"]=path_tree["hydro"]+"/freezeout.dat"
        dict_sampler_config["spectra_dir"]=path_tree["sampler"]
        dict_sampler_config["number_of_events"]=Nevent
        if float(dict["etaS"])==0.:
                dict_sampler_config["shear"] = 0
        else:
               dict_sampler_config["shear"] = 1
        
        print_dict_to_file(dict_sampler_config,dict_sampler_config["spectra_dir"]+"/sampler_config")
        return dict_sampler_config
         
def run_sampler(path_tree):
        try:
                samconfig = path_tree["sampler"]+"/sampler_config"
                subprocess.run(["./sampler", "events","1",samconfig])
        except:
                print("ERROR: no sampler_config found!")
        return 1

def write_afterburn_config(path_tree,Nevent=sampler_config.copy()["number_of_events"],dict_afterb_config=smash_yaml_config.copy()): 
        dict_afterb_config["Modi"]["List"]["File_Directory"]=path_tree["sampler"]
        dict_afterb_config["General"]["Nevents"]=Nevent      
        with open(path_tree["after"]+"/smash_afterburner.yaml","w") as file:
                yaml.dump(dict_afterb_config,file)
        #rename particle_lists.oscar, because!
        if os.path.exists(path_tree["sampler"]+"/particle_lists.oscar"):
                os.rename(path_tree["sampler"]+"/particle_lists.oscar",path_tree["sampler"]+"/sampling0")
        return dict_afterb_config

def run_smash(path_tree):
        try:
                yaml = path_tree["after"]+"/smash_afterburner.yaml"
                subprocess.run(["./smash", "-i",yaml,"-o",path_tree["after"]])
        except:
                print("ERROR: no smash_afterburner.yaml found!")
        return 1

def run_pol(path_tree):
        try: 
                beta = path_tree["hydro"]+"/beta.dat" 
                subprocess.Popen(["./calc",beta, path_tree["pol"]+"/primary"])
                subprocess.Popen(["./calc",beta, path_tree["pol"]+"/lambda_from_sigma0","3212","22"])
                subprocess.Popen(["./calc",beta, path_tree["pol"]+"/lambda_from_sigmastar","3224","211"])
        except:
                print("ERROR: no beta.dat found!")
        return 1

def run_hybrid(param, system, icfile ,outputfolder,Nevent=sampler_config.copy()["number_of_events"]):
        path_tree=init(outputfolder)
        try:
                run_vhlle(param,system,icfile,path_tree)
                write_sampler_config(param,path_tree,Nevent)
                #run_pol(path_tree)
                run_sampler(path_tree)
                write_afterburn_config(path_tree,Nevent)
                run_smash(path_tree)
        except:
                print("ERROR: something bad happened :(")

def analysis_and_plots(path_tree,Nevents):
        #try:
                particle_file = path_tree["after"]+"/particles_binary.bin"
                subprocess.run(["python3","mult_and_spectra.py",
                "--output_files_extended",path_tree["plots"],
                #path_tree["plots"]+"/yspectra.txt", path_tree["plots"]+"/mtspectra.txt", path_tree["plots"]+"/ptspectra.txt",
                #path_tree["plots"]+"/v2spectra.txt", path_tree["plots"]+"/meanmt0_midrapidity.txt", 
                #path_tree["plots"]+"/meanpt_midrapidity.txt", path_tree["plots"]+"/midrapidity_yield.txt", path_tree["plots"]+"/total_multiplicity.txt",
                "--input_files",particle_file])
                print("Analysis done...")
                subprocess.run(["python3", "plot_spectra.py", 
                "--input_files", 
                path_tree["plots"]+"/yspectra.txt", path_tree["plots"]+"/mtspectra.txt", path_tree["plots"]+"/ptspectra.txt",
                path_tree["plots"]+"/v2spectra.txt", path_tree["plots"]+"/meanmt0_midrapidity.txt",
                path_tree["plots"]+"/meanpt_midrapidity.txt", path_tree["plots"]+"/midrapidity_yield.txt", path_tree["plots"]+"/total_multiplicity.txt",
                "--Nevents", Nevents ])
        #except:
               # print("ERROR: there's no file to analyse and plot!")

def name_path_tree(dict_par,dict_glis,cent):
        # function to name the path tree
        path_name = "system"+ dict_glis["sNN"]+"centrality"+cent + "etaS" + dict_par["etaS"] + "ecrit" +dict_par["e_crit"] + "eta0" + dict_glis["eta0"] + "sigEta" + dict_glis["sigEta"]
        return path_name

def custom_call(icfile,centrality,Nevents = 1000,**kwargs):
	copy_params = params_modify()
	copy_gliss_setup = glissando_modify()
	for k,v in kwargs.items():
		if k in copy_params:
			print(k,v)
			copy_params[k] = v
		elif k in copy_gliss_setup:
                	copy_gliss_setup[k] = v
                	print(k,v)
		else:
			print("Invalid key!")
			return 0 
	name_maindir = name_path_tree(copy_params,copy_gliss_setup,centrality)

	path_tree = init(name_maindir)
                                
	path_params_file = path_tree["hydro"] + "/params"
	path_glissando_file = path_tree["hydro"] + "/gliss"
	print_dict_to_file(copy_params,path_params_file)
	print_dict_to_file(copy_gliss_setup,path_glissando_file)
	run_hybrid(path_params_file,path_glissando_file,icfile,name_maindir)
	analysis_and_plots(path_tree,str(Nevents))                  
	subprocess.run(["rm","-r",path_tree["hydro"],path_tree["sampler"],path_tree["after"],path_tree["pol"]])
	












