import hybrid_lib as hl

# define a list of values for etaS and eta0
etaS_values = ["0.12"]
eta0_values = ["5"]
ecrit_values = ["0.15","0.12"]
sigEta_values = ["1.4"]

rule all:
    input:
        [f"etaS_{etaS}_eta0_{eta0}_ecrit_{ecrit}_sigEta_{sigEta}.txt" for etaS in etaS_values for eta0 in eta0_values for ecrit in ecrit_values for sigEta in sigEta_values],
        [f"done_hyb_{etaS}_{eta0}_{ecrit}_{sigEta}.txt" for etaS in etaS_values for eta0 in eta0_values for ecrit in ecrit_values for sigEta in sigEta_values]
    output:
        "chain_done.txt"
    shell:
        "rm {input} && echo done > {output}"

# generate output files with a single value for etaS and eta0
rule gen_input:
    input:
    output:
        "etaS_{etaS}_eta0_{eta0}_ecrit_{ecrit}_sigEta_{sigEta}.txt"
    shell:
        "echo ammamo > {output}" 

# run the hybrid model for each combination of etaS and eta0
rule run_hybrid:
    input:
        "etaS_{etaS}_eta0_{eta0}_ecrit_{ecrit}_sigEta_{sigEta}.txt"
    output:
        file_name = "done_hyb_{etaS}_{eta0}_{ecrit}_{sigEta}.txt"
    run:
        Nevents = "100"
        centrality = "20-30"
        icfile = "/home/palermo/superMC/wouded_lhc5020_20-30%.data"
        etaS_value = wildcards.etaS
        eta0_value = wildcards.eta0
        ecrit_value = wildcards.ecrit
        sigEta_value = wildcards.sigEta
        print(etaS_value)

        # modify the parameter values and create the output directory
        copy_params = hl.params_modify(etaS=etaS_value, e_crit=ecrit_value)
        copy_superMC_setup = hl.supermc_modify(eta0=eta0_value, sigmaeta=sigEta_value)
        name_maindir = hl.name_path_tree(copy_params, copy_superMC_setup, centrality)
        path_tree = hl.init(name_maindir)
        
        # write the modified parameter values to files
        path_params_file = path_tree["hydro"] + "/params"
        path_supermc_file = path_tree["hydro"] + "/init"
        hl.print_dict_to_file(copy_params, path_params_file)
        hl.print_dict_to_file(copy_superMC_setup, path_supermc_file)

        # run the hybrid model and perform analysis
        hl.run_hybrid_plots(path_tree, Nevents)
        with open(output.file_name,"w") as f:
            f.write("gnegne")



