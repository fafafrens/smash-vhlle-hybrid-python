import subprocess
import os 
import yaml

### Dictionary for the param file used by vhlle
params_dict = {
        "outputDir"     :   "none",
        "eosType"       :   "0",           
        "etaS"          :   "0.12",            #  eta/s value
        "zetaS"         :   "0.0",             #  zeta/s, bulk viscosity
        "e_crit"        :   "0.515",           #  criterion for surface finding
        "zetaSparam"    :   "0",               #  0 basic param (is zetaS 0 no bulk), 1,2,3
        "nx"            :   "201",             # number of cells in X direction
        "ny"            :   "201",             # number of cells in Y direction
        "nz"            :   "101",              # number of cells in eta direction
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
        "tau0"          :   "1.0",  	      # starting proper time
        "tauMax"        :   "15.0",  	      # proper time to stop hydro
        "dtau"          :   "0.1"   	      # timestep
}

### Dictionary for the glissando values used by vhlle
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

### Dictionary for the superMC file used by vhlle
supermc_dict = {
	"sNN"      : "5020",
	"eta0"     : "3.5", # midrapidity plateau
  	"sigmaeta" : "1.4", # diffuseness of rapidity profile
  	"w"	   : "0.4",
  	"eff"	   : "0.15",
        "etaB"     : "3.5",
        "sigmaIN"  : "2.0",
        "sigmaOUT" : "0.1"
}

### Dictionary for the of hybrid model: see examples/
input_dict = {
        "param" : "vhlle param file (-param)",
        "system" : "vhlle collision system (-system)",
        "icinput" : "initial condition file in vhlle (-ISinput)",
        "outputfolder" : "master output folder, base of the path three",
        "Nevents" : "1000"
}

### Dictionary for the sampler config file
sampler_config = {
        "surface"          : "/path/to/freezeout/surface",
        "spectra_dir"      : " /path/to/output",
        "number_of_events" : "1000",
        "weakContribution" : "0",
        "shear"            : "1",
        "ecrit"            : "0.5"
}

### Dictionary for SMASH config file
smash_yaml_config={
        'Version': "1.8",
        'Logging': {'default': 'INFO'},
        'General': {'Modus': 'List',
        'Time_Step_Mode': 'None',
        'Delta_Time': "0.1",
        'End_Time': "30000.0",
        'Randomseed': "-1",
        'Nevents': "1000"},
        'Output': {'Particles': {'Format': ['Binary', 'Oscar2013']}},
        'Modi': {'List': {'File_Directory': '../build/',
        'File_Prefix': 'sampling',
        'Shift_Id': "0"}}
}

def modify_dictionary(dict_name,**kwargs):
        """
        Function used to change the entries of the dictionary called "dict_name". kwargs are of the form "key=value".
        If the key is not in the dictionary nothing happens
        """
        if dict_name == "params_dict":
                dict_copy = params_dict.copy()
        if dict_name == "glissando_dict":
                dict_copy = glissando_dict.copy()
        if dict_name == "supermc_dict":
                dict_copy = supermc_dict.copy()
        if dict_name == "input_dict":
                dict_copy = input_dict.copy()
        if dict_name == "sampler_config":
                dict_copy = sampler_config.copy()
        if dict_name == "smash_yaml_config":
                dict_copy = smash_yaml_config.copy()

        for key, value in kwargs.items():
                if key in dict_copy.keys():
                        dict_copy[key] = value
                        
        return dict_copy


def modify_dictionary_logger(dict_name,**kwargs):
        """
        Function used to change the entries of the dictionary called "dict_name". kwargs are of the form "key=value".
        Error message if key is not in the dictionary
        """
        
        dict_copy = modify_dictionary(dict_name, **kwargs)

        for key, value in kwargs.items():
                if key not in dict_copy.keys():
                        print("ERROR: the key you want to modify is not in this dictionary!")
                        return
                        
        return dict_copy


def read_dictionary(input_file):
        '''
        Returns a dictionary, reading it from the file input_file
        '''
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
        '''
        Used to create the path tree of a single hybrid run. 
        Creates the folder ./output_main as well as the subfolders 'Hydro', 'Sampler', 'Afterburner',
        'Plots' and 'Polarization'. The last two folders will be empty at the end of the hybrid run but they are useful
        to keep track of the analysis.
        Returns a dictionary containing the information about the path tree structure, which can be used to redirect the input and output
        e.g. :
                path_tree = init("example") ##creates a directory called 'example' and all the subdir. path_tree is a dictionary.
                path_tree["hydro"] ##path to the Hydro folder, i.e. "example/Hydro"
        
        If the folders already exist they are not modified, and the function returns the dictionary of the path tree

        The dictionary will look like:
        path_tree["hydro"] = 'path_to_hydroFolder"
        path_tree["sampler"] =  'path_to_samplerFolder"
        path_tree["after"] = 'path_to_afterburnerFolder"
        path_tree["plots"] = 'path_to_plotsFolder"
        path_tree["pol"] = 'path_to_polarizationFolder"
        '''
        path_tree_dict={}
        hydropath = f"./{output_main}/Hydro"
        samplerpath = f"./{output_main}/Sampler"
        afterpath = f"./{output_main}/Afterburner"
        plotspath = f"./{output_main}/Plots"
        polpath = f"./{output_main}/Polarization"

        keys = ["hydro","sampler","after","plots","pol"] #These are the keys of the path_tree dictionary
        values = [hydropath,samplerpath,afterpath,plotspath,polpath] #These are the paths associated to each key
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
        '''
        Function used to run vhlle.
        param, system, icfile are part of the input expected by vhlle. path_tree is used to
        write the output files at path_tree/Hydro
        '''
        try:
                subprocess.run(["./hlle_visc","-system",system,"-params",param,"-ISinput",icfile,"-outputDir",path_tree["hydro"]])
        except:
                print("ERROR: something went wrong running vHLLE.")


def print_dict_to_file(dict,output):
    '''
    Prints the dictionary "dict" to the file "output"
    '''
    with open(output, 'w') as f: 
        for key, value in dict.items(): 
            f.write('%s    %s\n' % (key, value))


def write_sampler_config(param,path_tree,Nevent): 
        '''
        Given the "param" file used by vhlle writes the corresponding sampler file for Nevent
        events in the folder path_tree["sampler"] (see the function init()).
        Returns the sampler's dictionary associated to the config file that has been just written.
        '''
        dict_param = read_dictionary(param)
        dict_sampler_config = sampler_config.copy()
        
        dict_sampler_config["ecrit"] = dict_param["e_crit"]
        dict_sampler_config["surface"] = path_tree["hydro"]+"/freezeout.dat"
        dict_sampler_config["spectra_dir"] = path_tree["sampler"]
        dict_sampler_config["number_of_events"] = Nevent
        
        if float(dict_param["etaS"])==0.:
                dict_sampler_config["shear"] = 0
        else:
               dict_sampler_config["shear"] = 1
        
        print_dict_to_file(dict_sampler_config,dict_sampler_config["spectra_dir"]+"/sampler_config")
        
        return dict_sampler_config
         
def run_sampler(path_tree):
        '''
        Runs the sampler and renames the output as expected from smash
        '''
        try:
                samconfig = path_tree["sampler"]+"/sampler_config"
                subprocess.run(["./sampler", "events","1",samconfig])
                #rename particle_lists.oscar
                if os.path.exists(path_tree["sampler"]+"/particle_lists.oscar"):
                        os.rename(path_tree["sampler"]+"/particle_lists.oscar",path_tree["sampler"]+"/sampling0")
        except:
                print("ERROR with the run_sampler function of the hybrid!")
        return 1

def write_afterburn_config(path_tree,Nevent):
        '''
        Writes the afterburner configuration file for Nevents and with the correct paths.
        Returns the dictionary associated to the file created.
        '''
        dict_afterb_config = smash_yaml_config.copy() 
        dict_afterb_config["Modi"]["List"]["File_Directory"] = path_tree["sampler"]
        dict_afterb_config["General"]["Nevents"] = Nevent      
        with open(path_tree["after"]+"/smash_afterburner.yaml","w") as file:
                yaml.dump(dict_afterb_config,file)
        return dict_afterb_config

def run_smash(path_tree):
        '''
        Runs smash taking the input from the path_tree["sampler"] folder and saving the output in path_tree["after"]
        NB: the file smash_afterburner.yaml is assumed to exist.
        '''
        try:
                yaml = path_tree["after"]+"/smash_afterburner.yaml"
                subprocess.run(["./smash", "-i",yaml,"-o",path_tree["after"]])
        except:
                print("ERROR with the function run_smash of the hybrid!")
        return 1

def run_afterburner(path_tree):
        '''
        Runs the sampler and the afterburner. 
        NB: the sampler_config file is assumed to exist.
        '''
        try:
                path_sampler_config = path_tree["sampler"]+"/sampler_config"
                sampler_config_dict = read_dictionary(path_sampler_config)
                Nevent = sampler_config_dict["number_of_events"]
                
                run_sampler(path_tree)
                write_afterburn_config(path_tree,Nevent)
                run_smash(path_tree)
                
        except:
                print("ERROR with the function run_afterburner of the hybrid!")
        return 1

def run_polarization(path_tree):
        '''
        Runs the polarization calculations.
        NB: NOT TESTED
        '''
        try: 
                beta = path_tree["hydro"]+"/beta.dat" 
                subprocess.run(["./foil",beta, path_tree["pol"]])
        except:
                print("ERROR when running the polarization calculations!")
        return 1

def run_hybrid(param, system, icfile,pathtree,Nevent):
        '''
        Given the param file, the initial condition file and the
        system of vhlle, runs the full hybrid chain saving the outputs
        in the path tree pathtree. Nevent events are sampled by samsh at freeze-out
        '''
        path_tree = init(pathtree)
        try:
                run_vhlle(param,system,icfile,path_tree)
                write_sampler_config(param,path_tree,Nevent)
                #run_pol(path_tree) ##uncomment if you want the polarization calculations
                run_sampler(path_tree)
                write_afterburn_config(path_tree,Nevent)
                run_smash(path_tree)
        except:
                print("ERROR: something bad happened :(")

##################################################################################
#### THE FOLLOWING FUNCTIONS ARE USEFUL FOR SCHEDULING MULTIPLE SIMULTANEOUS RUNS
#### WITH SNAKEMAKE
##################################################################################

def get_different_key_value(dictionary1,dictionary2):
    """
    Compares dictionary1 and dictionary2 and outputs a string of the key and value of dictionary1 that are different from
    the those in dictionary2. The comparison happens between common keys.
    """
    name = "" 
    for key, value in dictionary1.items():
        if key in dictionary2 and value != dictionary2[key]:
            name += key + "_" + str(value) + "_" 
    return name

def name_folder(prefix="", param=params_dict, gliss=glissando_dict, 
                    smc=supermc_dict, sampl=sampler_config, smash=smash_yaml_config):
    '''
    Name a folder according to the unique parameters that are different
    from the default dictionaries. "prefix" is an optional prefix
    that can be used to specify additional info e.g. the centrality, 
    number of averaged events for the IC, the date...

    This function is useful if you want to run many events with different values of
    some dictionary parameter. E.g. if you want to run with different etaS than
    the default, say etaS=0.11, and a prefix "testingEtaS"
    you will get strings like "testingEtaS_params:etaS_0.11"
    '''
    name = ""
    if(prefix != ""):
        name += prefix + "_"

    if param != params_dict:
        name += "params:"
        name += get_different_key_value(param,params_dict)  

    if gliss != glissando_dict:
        name += "gliss:" 
        name += get_different_key_value(gliss,glissando_dict)
        
    if smc != supermc_dict:
        name += "superMC:"
        name += get_different_key_value(smc,supermc_dict)

    if sampl != sampler_config:
        name += "sampler:"
        name += get_different_key_value(sampl, sampler_config)
    
    if smash != smash_yaml_config:
        name += "smash:"
        name += get_different_key_value(smash, smash_yaml_config)
    
    name = name[:-1] #remove the last "_"
    
    return name

def add_string_lists(str_list1, str_list2):
    ''' 
    Combines the two lists of strings in every possible way: ["a","b"]+["c","d"]=["ac","ad","bc","bd"]
    if one of the lists is empty returns the non empty one.
    Useful if you want to run combinations of multiple parameters, e.g. etaS and ecrit
    '''
    sum = []
    if(str_list1 == []):
        return str_list2
    if (str_list2 == []):
        return str_list1

    for s1 in str_list1:
        for s2 in str_list2:
            sum.append(s1+s2)
    
    return sum

def snake_rule_files(dict):
    '''
    From a dictionary {key:[values]} where key and values are strings
    returns a list of strings with the expected format for Snakemake.
    Here the expected format used is "key1?value1?key2?value2?.txt"
    ''' 
    output = []
    keys = dict.keys()
    for key in keys:
        temp_list = []
        for value in dict[key]:
            temp_list.append(key+"?"+value+"?")
        output = add_string_lists(output,temp_list)
    ###output is now a list of all the possible combintation of parameters and keys in dict
    
    for i in range(len(output)):
        filename = output[i] 
        output[i] = filename[:-1]+".txt"

    return output
       
def input_format(dict):
    '''
    Return the expected format for output files as expected in Snakemake.
    The {} are used for wildcards in Snakemake.
    '''
    string = ""
    for k in dict.keys():
        string += k+"?{"+k+"}?"
    string = string[:-1] +".txt"
    return string

def unpack_string_to_dictionary(string):
    '''
    Gets a dictionary from a string in order to print it to the snakemake file
    '''
    string = string[:-4] #remove the .txt from the string
    dummy = string.replace("{","")
    dummy = dummy.replace("}","")
    unpacked = dummy.split("?")
    
    keys = unpacked[::2]
    values = unpacked[1::2]
    dictionary = {}
    for k,v in zip(keys,values):
            dictionary[k]=v
    return dictionary