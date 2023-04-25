import numpy as np
import matplotlib.pyplot as plt

def number_of_events(particle_list_file):
    '''
    This function checks the output of smash and returns the number of events sampled. 
    The path to particle_list.oscar is used as argument
    '''
    nevents = 0
    all_lines = open(particle_list_file, 'r')
    for line in all_lines:
        if 'impact' in line:
            nevents = nevents + 1
    return nevents

def momentum_in_particle_selection(particle_list_file, criterion_string):
    '''
    Returns a tuple corresponding to (E,px,py,pz) given a particle_list file and a selection criterion.
    Contravariant indices are implied.
    '''
    data = np.loadtxt(particle_list_file, unpack=True)
    E = data[5]
    px = data[6]
    py = data[7]
    pz = data[8]
    charge = data[11]
    pdg_id = data[9]
    if(criterion_string == "charged"):
        print("analysing charged particles")
        return E[(charge!=0)], px[(charge!=0)], py[(charge!=0)] , pz[(charge!=0)]
    else:
        pdg_particle = int(criterion_string)
        if pdg_particle in pdg_id:
           return E[(pdg_id==pdg_particle)], px[(pdg_id==pdg_particle)], py[(pdg_id==pdg_particle)] , pz[(pdg_id==pdg_particle)]
        else:
            print("The pdg_id ", pdg_particle, " doesn't correspond to any particle produced!")
            print("Error!")
            exit(1)

def pseudorapidity_distribution(px,py,pz,nevents,eta_min,eta_max, number_of_bins=50):
    '''
    Returns a tuple with (bin_centers,<dN_deta>)
    The output of this function can be easily plotted unpacking with *:
        plt.plot(*pseudorapidity_distribution, ... )
    '''
    eta_bins = np.linspace(eta_min, eta_max, number_of_bins)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    N_in_bin, bin_edges = np.histogram(eta, bins=eta_bins)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_width = bin_centers[1] - bin_centers[0]
    dN_deta = N_in_bin/(bin_width*nevents)

    return bin_centers,dN_deta

def pt_distribution(px,py,pz,nevents,pt_max, number_of_bins=50):
    #WARNING: NOT COMPLETELY SURE ABOUT THIS ONE
    '''
    Returns a tuple with (bin_centers,<pt>)
    The output of this function can be easily plotted unpacking with *:
        plt.plot(*pt_distribution, ... )
    '''
    pt = np.sqrt(px**2+py**2)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    pt_bins = np.linspace(0.2,pt_max,number_of_bins)
    #pt_bins = np.logspace(np.log(0.2), np.log(pt_max), num=number_of_bins, base=np.exp(1))
    #selecting particles at midrapidity
    pt = pt[(np.fabs(eta)<0.5)]
    N_in_bin, bin_edges = np.histogram(pt, bins=pt_bins)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_width = bin_centers[1] - bin_centers[0]
    dN_dpt = N_in_bin/(bin_width*nevents*bin_centers*(2*np.pi))

    return bin_centers,dN_dpt