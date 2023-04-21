import hybrid_lib as hl

# define a list of values for etaS and eta0
etaS_values = ["0.001","0.08","0.16"]
ecrit_values = ["0.25","0.5"]
w_values = ["0.4","0.8","1.2"]

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

rule all:
    input:
        [f"etaS_{etaS}_ecrit_{ecrit}_w_{w}.txt" for etaS in etaS_values for ecrit in ecrit_values for w in w_values],
        [f"done_hyb_etaS_{etaS}_ecrit_{ecrit}_w_{w}.txt" for etaS in etaS_values for ecrit in ecrit_values for w in w_values]
    output:
        "chain_done.txt"
    shell:
        "rm {input} && echo done > {output}"

# generate output files with a single value for etaS and eta0
rule gen_input:
    input:
    output:
        "etaS_{etaS}_ecrit_{ecrit}_w_{w}.txt"
    shell:
        "echo ammammao > {output}" 

# run the hybrid model for each combination of etaS and eta0
rule run_hybrid:
    input:
        "etaS_{etaS}_ecrit_{ecrit}_w_{w}.txt"
    output:
        file_name = "done_hyb_etaS_{etaS}_ecrit_{ecrit}_w_{w}.txt"
    run:
        Nevents = "200"
        centrality = "20-30"
        icfile = "/home/palermo/superMC/rhic200-20-30%_10kevents.data"
        etaS_value = wildcards.etaS
        ecrit_value = wildcards.ecrit
        w_value = wildcards.w

        # modify the parameter values and create the output directory
        copy_params = hl.modify_dictionary("params_dict",etaS=etaS_value, e_crit=ecrit_value)
        copy_superMC_setup = hl.modify_dictionary("supermc_dict",w=w_value, **supermc_dict_value)
        name_maindir = hl.name_folder(param=copy_params,smc=copy_superMC_setup,prefix="baryon"+"cent"+centrality)
        path_tree = hl.init(name_maindir)
        
        # write the modified parameter values to files
        path_params_file = path_tree["hydro"] + "/params"
        path_supermc_file = path_tree["hydro"] + "/supermc_file"
        hl.print_dict_to_file(copy_params, path_params_file)
        hl.print_dict_to_file(copy_superMC_setup, path_supermc_file)

        # run the hybrid model and perform analysis
        hl.run_hybrid(path_params_file,path_supermc_file,icfile,name_maindir,int(Nevents))
        hl.analysis_and_plots(path_tree, Nevents)
        #subprocess.run(["rm -r ",path_tree["hydro"],path_tree["sampler"],path_tree["after"]])      
        with open(output.file_name,"w") as f:
            f.write("gnegne")



