import hybrid_lib as hl

# define a list of values for etaS and eta0
etaS_values = ["0.08","0.12"]
eta0_values = ["5.0"]
ecrit_values = ["0.5","0.4"]
sigEta_values = ["0.6","0.8"]
eff_values = ["1.0","0.5"]

rule all:
    input:
        [f"etaS_{etaS}_eta0_{eta0}_ecrit_{ecrit}_sigEta_{sigEta}_eff_{eff}.txt" for eff in eff_values for etaS in etaS_values for eta0 in eta0_values for ecrit in ecrit_values for sigEta in sigEta_values],
        [f"done_hyb_{etaS}_{eta0}_{ecrit}_{sigEta}_{eff}.txt" for eff in eff_values for etaS in etaS_values for eta0 in eta0_values for ecrit in ecrit_values for sigEta in sigEta_values]
    output:
        "chain_done.txt"
    shell:
        "rm {input} && echo done > {output}"

# generate output files with a single value for etaS and eta0
rule gen_input:
    input:
    output:
        "etaS_{etaS}_eta0_{eta0}_ecrit_{ecrit}_sigEta_{sigEta}_eff_{eff}.txt"
    shell:
        "echo ammammao > {output}" 

# run the hybrid model for each combination of etaS and eta0
rule run_hybrid:
    input:
        "etaS_{etaS}_eta0_{eta0}_ecrit_{ecrit}_sigEta_{sigEta}_eff_{eff}.txt"
    output:
        file_name = "done_hyb_{etaS}_{eta0}_{ecrit}_{sigEta}_{eff}.txt"
    run:
        Nevents = "100"
        centrality = "20-30"
        icfile = "/home/palermo/superMC/rhic200_20-30%_10kevents.data"
        etaS_value = wildcards.etaS
        eta0_value = wildcards.eta0
        ecrit_value = wildcards.ecrit
        sigEta_value = wildcards.sigEta
        eff_value = wildcards.eff

        # modify the parameter values and create the output directory
        copy_params = hl.params_modify(etaS=etaS_value, e_crit=ecrit_value)
        copy_superMC_setup = hl.supermc_modify(eta0=eta0_value, sigmaeta=sigEta_value, eff=eff_value )
        name_maindir = hl.name_folder(param=copy_params,smc=copy_superMC_setup,prefix="cent"+centrality)
        path_tree = hl.init(name_maindir)
        
        # write the modified parameter values to files
        path_params_file = path_tree["hydro"] + "/params"
        path_supermc_file = path_tree["hydro"] + "/init"
        hl.print_dict_to_file(copy_params, path_params_file)
        hl.print_dict_to_file(copy_superMC_setup, path_supermc_file)

        # run the hybrid model and perform analysis
        hl.run_hybrid(path_params_file,"RHIC200",icfile,name_maindir,int(Nevents))
        hl.analysis_and_plots(path_tree, Nevents)
        #subprocess.run(["rm -r ",path_tree["hydro"],path_tree["sampler"],path_tree["after"]])      
        #with open(output.file_name,"w") as f:
            #f.write("gnegne")



