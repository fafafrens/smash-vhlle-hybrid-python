import hybrid_lib as hl

# define a list of values for etaS and eta0
loopable_dict = { 
    #WARNING: USE THE SAME ENTRIES AS DEFINED IN THE DEFAULT DICTIONARIES!!!!
    #WARNING 2: THE CHARACTER '?' IS USED BY CONVENTION IN THE TEMPORARY SNAKEMAKE FILES: DO NOT USE IT IN THE DICTIONARIES!!!
    'etaS' : ["0.001","0.08","0.16"],
    'e_crit' : ["0.25"],#["0.25","0.5"],
    'w' : ["0.4"]#["0.4","0.8","1.2"]
}
#static values for superMC dctionary
supermc_dict_value = {
	"sNN"      : "200",
	"eta0"	   : "2.5",
	"sigmaeta" : "0.5",
    "eff"	   : "0.15",
	"etaB"     : "3.5",
    "sigmaIN"  : "2.0",
    "sigmaOUT" : "0.1"
}

format_string = hl.input_format(loopable_dict)
input_list_rule_all = hl.snake_rule_files(loopable_dict)

rule all:
    input:
        input_list_rule_all,
        [f"done?hyb?" + name for name in input_list_rule_all]
    output:
        "chain_done.txt"
    shell:
        #"rm {input} && echo done > {output}"
        "echo done > {output}"

# generate output files with a single value for etaS and eta0
rule gen_input:
    input:
    output:
        fileout = format_string
    run:
        dictionary = hl.unpack_string_to_dictionary(output.fileout)
        hl.print_dict_to_file(dictionary,output.fileout) 

# run the hybrid model for each combination of etaS and eta0
rule run_hybrid:
    input:
        file_input = format_string
    output:
        file_name = "done?hyb?"+format_string
    run:
        Nevents = "200"
        centrality = "20-30"
        icfile = "/home/palermo/superMC/rhic200-20-30%_10kevents.data"
        input_dictionary = hl.get_input(input.file_input)

        # modify the parameter values and create the output directory
        copy_params = hl.modify_dictionary("params_dict",**input_dictionary)
        copy_superMC_setup = hl.modify_dictionary("supermc_dict",**input_dictionary, **supermc_dict_value)
        name_maindir = hl.name_folder(param=copy_params,smc=copy_superMC_setup,prefix="baryon"+"cent"+centrality)
        path_tree = hl.init(name_maindir)
        
        # write the modified parameter values to files
        path_params_file = path_tree["hydro"] + "/params"
        path_supermc_file = path_tree["hydro"] + "/supermc_file"
        hl.print_dict_to_file(copy_params, path_params_file)
        hl.print_dict_to_file(copy_superMC_setup, path_supermc_file)

        # run the hybrid model and perform analysis
        #hl.run_hybrid(path_params_file,path_supermc_file,icfile,name_maindir,int(Nevents))
        #hl.analysis_and_plots(path_tree, Nevents)
        #subprocess.run(["rm -r ",path_tree["hydro"],path_tree["sampler"],path_tree["after"]])      
        with open(output.file_name,"w") as f:
            f.write("ammammao")



