# smash-vhlle-hybrid-python
This repository contains the scripts to run the chain of hydrodynamic and afterburning through the codes vHLLE, smash-hadron.sampler and SMASH. It is based on Python. To use it you need to have installed the following programs:
* [vHLLE](https://github.com/yukarpenko/vhlle)
* [vHLLE-parameters](https://github.com/yukarpenko/vhlle_params)
* [SMASH](https://github.com/smash-transport/smash)
* [hadron sampler](https://github.com/smash-transport/smash-hadron-sampler)

 If you want to run parallelly multiple simulations, you will also need:
 * [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html)
   
We recommend the use of a [miniconda environment](https://docs.anaconda.com/free/miniconda/index.html) to install Snakemake. If you use this repo, please cite xxxx.xxxxx.

## Disclaimer
This hybrid model should work for any initial conditions but it has been extensively used with the [superMC](https://github.com/chunshen1987/superMC) initial condition. Adding other initial conditions requires some modifications to the hybrid_lib and, possibly, to vHLLE. We have run with an average initial state, but event-by-event simulations are also possible with no modifications to the hybrid_lib.

# Installing 

After cloning the repository you simply need to move the Python and Snakemake files contained in this repo to the location where you want the hybrid to work. The hybrid directory should also contain the executables of vHLLE, SMASH and the hadron sampler, so make sure you have compiled them. You can move everything manually or use the **move_to_hybrid_folder.py** script. If you choose the latter, make sure to modify the target directory and the path to the other programs:
```
# Directory where you want the hybrid to work
target_directory = "./"

#The directory containing the folders: smash, smash-hadron-smapler, vhlle, and this repo.
work_directory = '/home/'
```
Notice that the default location for the hybrid is assumed to be the current directory and that the default location of all the other programs is `home`. After that, simply run 
```python move_to_hybrid_folder.py```.

# Running the hybrid

This code works based on dictionaries in Python and on the library **hybrid_lib.py**. This library contains dictionaries associated with the configuration files of each of the other programs. The advantage is that parameters can be modified online by acting on the dictionaries instead of the files themselves. A description of each function is present in the library itself.

Some example files are provided in the `examples` folder. An example script to run the full hybrid or part of it, based on some preexisting parameter file is available at **examples/example_run_hybrid.py**. This uses an input file, `input_example.txt` (provided) where you would need to add the information relevant to the hybrid. 

If you want to run the hybrid by modifying some parameters and/or run multiple times each time with a different set of parameters (looping on the parameter space you want to explore) you can modify the parameters online in a Python script, acting on the built-in copies of the configuration dictionaries. An example script is available at **examples/example_multirun.py**.


# Snakemake
For tuning the initial state parameters, or for event-by-event simulations, it is convenient to run several simulations at the same time. To take track of the dependencies of each chain we advocate the use of **Snakemake**. Snakemake is similar to make and cmake, but much easier to read, and it is based on the Python language. For a detailed explanation of how it works, please refer to the [documentation](https://snakemake.readthedocs.io/en/stable/index.html). The Snakemake files provided here are commented to be understandable. To run the instructions written in a file called "Snakefile" run:
```
snakemake --cores n
```
where n is the number of cores you want to use. Each of the cores will handle a snakemake instruction, in our case a hybrid run. To run a file with a custom name, run:
```
snakemake -s custom_name --cores n
```

## Example
An example of a Snakefile is provided in the example folder. Here, we comment on its functioning.

Snakemake is based on **rules**. Each rule, to be executed, waits until the files in the **input** section are present, and its execution can produce output files in the **output** section. Additional sections that we use are **run**, which works as a Python script, and **shell**, which executes bash commands (Notice that one cannot use both run and shell in the same rule). Furthermore, substrings in the name of the input files can be used as **wildcards**, and accessed in the run section. In the example, we have a rule:
```
rule example:
    input:
        "input_{wild}.txt"
    output:
        "snakemake_{wild}.txt"
    run:
        wildcard = wildcards.wild
        print(f"\n the wildcard is the string: {wildcard}\n")
        
        with open(output[0],"w") as f:
            f.write("done!")
```
This rule will run if there is a file called `input_x.txt` in the folder, where "x" can be any string. `{wild}` will match the string "x" to the wildcard `wild`. We can access it in the run section through `wildcards.wild`. However, the wildcard wild is not defined yet. We need to tell the rule example what to expect by adding a rule *before* example. For instance:
```
rule all:
    input:
        "snakemake_example.txt"
```
This rule will work only if snakemake_example.txt is in the folder (and the rule will do nothing). But since example_snakemake is not there yet, this rule will invoke the example rule, which generates precisely the expected format. Now snakemake defines the wildcard wild="example". If the file input_example.txt is in the folder, the chain of rules will be executed. Notice that, if the dependencies of the rule all are already satisfied and snakemake_example.txt exists in the folder already, nothing will happen.
If you have successfully installed snakemake, executing `snakemake --cores 1` in the examples folder will run the example script Snakefile and produce the snakemake_example.txt file.

This mechanism can be used to run parallelly n different chains (--cores n) based on different filenames. For example, if we label 100 runs of the initial state as 1.txt, 2.txt ... the number can be accessed as a wildcard and each file can be used for a separate, parallel run. 
