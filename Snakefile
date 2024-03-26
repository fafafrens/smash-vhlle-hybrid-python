import hybrid_lib as hl
import os

#we create a directory to store the temporary snakemake files
snakemake_folder = "tmp_snakemake"  
if not os.path.exists(snakemake_folder):
    os.makedirs(snakemake_folder)
snakemake_folder = snakemake_folder +"/"

# define a list of values to loop over if you want to test different setups
loopable_dict = { 
    #WARNING: USE THE SAME ENTRIES AS DEFINED IN THE DEFAULT DICTIONARIES!!!!
    #WARNING 2: THE CHARACTER '?' IS USED BY CONVENTION IN THE TEMPORARY SNAKEMAKE FILES: DO NOT USE IT IN THE DICTIONARIES!!!
    'etaS' : ["0.08"],
    'e_crit' : ["0.5"],
    'w' : ["0.4","0.8","1.2"],  
    "eta0"	   : ["2.5","3.0","2.0","3.5"],
    "sigmaeta" : ["0.5","0.8","1.2","1.4"],
    'zetaSparam' : ["0","3"]
}
#static values for superMC dctionary
supermc_dict_value = {
	"sNN"      : "5020",
	"eff"	   : "0.15",
	"etaB"     : "3.5",
	"sigmaIN"  : "2.0",
	"sigmaOUT" : "0.1"
}

#Number of events sampled from the particlization hypersup
Nevents = "200"

input_format = hl.input_format(loopable_dict)
format_string = snakemake_folder + input_format
done_hydro_format = snakemake_folder + "done?hydro?"+input_format
done_hyb_format = snakemake_folder + "done?hyb?"+input_format

list_names = hl.snake_rule_files(loopable_dict)

input_list_rule_all = [snakemake_folder + name for name in list_names]
done_hydro_list = [snakemake_folder + f"done?hydro?" + name for name in list_names]
done_hyb_list = [snakemake_folder + f"done?hyb?" + name for name in list_names]

rule all:
    input:
        input_list_rule_all,
        done_hydro_list,
        done_hyb_list
    output:
        "chain_done.txt"
    shell:
        "rm {input} && echo done > {output}"

# generate output files with a single value for etaS and eta0
rule gen_input:
    input:
    output:
        fileout = format_string
    run:
        input_parameter_string = output.fileout.replace(snakemake_folder,'')
        dictionary = hl.unpack_string_to_dictionary(input_parameter_string)
        hl.print_dict_to_file(dictionary,output.fileout) 

rule run_afterburn:
        input:
            file_input = format_string,
            file_hydro = done_hydro_format
        output:
            file_hybrid = done_hyb_format
        run:
            with open(input.file_hydro,"r") as f:
                name_maindir = f.read()
            path_tree = hl.init(name_maindir)
            
            hl.run_sampler(path_tree)
            hl.write_afterburn_config(path_tree,Nevents)
            hl.run_smash(path_tree)


            #subprocess.run(["rm","-r ",path_tree["hydro"],path_tree["sampler"]])       ##UNCOMMENT IF YOU WANT TO DELATE THESE FOLDERS     
            with open(output.file_hybrid,"w") as f:
                f.write("ammammao")
        
# run the hybrid model for each combination of etaS and eta0
rule run_vhlle:
    input:
        file_input = format_string
    output:
        file_hydro = done_hydro_format
    run:
        centrality = "30-50"
        icfile = "/home/palermo/superMC/lhc_30-50_5kevents.data"
        input_dictionary = hl.read_dictionary(input.file_input)

        # modify the parameter values and create the output directory
        copy_params = hl.modify_dictionary("params_dict",**input_dictionary)
        copy_superMC_setup = hl.modify_dictionary("supermc_dict",**input_dictionary, **supermc_dict_value)
        

        name_maindir = hl.name_folder(param=copy_params,smc=copy_superMC_setup,prefix="Plo_run_cent"+centrality)
        path_tree = hl.init(name_maindir)
        
        # write the modified parameter values to files
        path_params_file = path_tree["hydro"] + "/params"
        path_supermc_file = path_tree["hydro"] + "/supermc_file"
        hl.print_dict_to_file(copy_params, path_params_file)
        hl.print_dict_to_file(copy_superMC_setup, path_supermc_file)

        # run the hybrid model and perform analysis    
        hl.run_vhlle(path_params_file,path_supermc_file,icfile,path_tree)
        hl.write_sampler_config(path_params_file,path_tree,Nevents)
	
        with open(output.file_hydro,"w") as f:
            f.write(name_maindir)




