import numpy as np
import matplotlib.pyplot as plt

##############################################################################
### USE TO ANALYSE SMASH OUTPUT
### THE OUTPUT OF MOST ANALYSIS FUNCTIONS ARE TUPLE, AND CAN BE PLOTTED
### EASILY BY UNPACKING WITH "*". 
### FOR EXAMPLE: plt.plot(*pseudorapidity_distribution, ... )
##############################################################################

def number_of_events(particle_list_file):
    '''
    This function checks the output of smash and returns the number of events sampled. 
    particle_list_file is the path to particle_list.oscar
    '''
    nevents = 0
    all_lines = open(particle_list_file, 'r')
    for line in all_lines:
        if 'impact' in line:
            nevents = nevents + 1
    return nevents

def momentum_in_particle_selection(particle_list_file, criterion_string, midrapidity=0):
    '''
    Returns a tuple corresponding to (E,px,py,pz) given a particle_list file and a selection criterion.
    Contravariant indices are implied. E,px,py,pz are lists.
    To sample in |\eta|<value use midrapidity=value in the argument.
    the selection criterion is assigner by criterion_string=criterion.
    Implemented criteria are: all, charged, pdg_id
    '''
    data = np.loadtxt(particle_list_file, unpack=True)
    E = data[5]
    px = data[6]
    py = data[7]
    pz = data[8]
    charge = data[11]
    pdg_id = data[9]

    if(midrapidity):
        print("Filtering particles in the pseudorapidity region |eta| < ", midrapidity)
        eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
        E = E[abs(eta)<midrapidity]
        px = px[abs(eta)<midrapidity]
        py = py[abs(eta)<midrapidity]
        pz = pz[abs(eta)<midrapidity]
        charge = charge[abs(eta)<midrapidity]
        pdg_id = pdg_id[abs(eta)<midrapidity]
    else:
        print("No rapidity cut selected...")
        
        
    if(criterion_string == "charged"):
        print("Filtering charged particles...")
        return E[(charge!=0)], px[(charge!=0)], py[(charge!=0)] , pz[(charge!=0)]
    
    elif(criterion_string == "all"):
        print("Momenta of all particles...")
        return E, px, py , pz

    elif(str(criterion_string).lstrip("-").isdigit()):
        print("Checking pdg_id...")
        pdg_particle = int(criterion_string)
        if pdg_particle in pdg_id:
           print("Filtering pdg_id = ",pdg_particle)
           return E[(pdg_id==pdg_particle)], px[(pdg_id==pdg_particle)], py[(pdg_id==pdg_particle)] , pz[(pdg_id==pdg_particle)]
        else:
            print("Alas, the pdg_id ", pdg_particle, " doesn't correspond to any particle produced!")
            print("Error!")
            exit(1)
    else:
        print("Unkonwn selection criterion!")
        print("Error!")
        exit(1)


### FUNCTIONS FOR PSEUDORAPIDITY DISTRIBUTION
def pseudorapidity_distribution(px,py,pz,nevents,eta_min=-4,eta_max=4, number_of_bins=50):
    '''
    Given the list of momenta px,py,pz and the number of SMASH events,
    returns a tuple with (bin_centers,<dN/deta>).
    Rapidity cuts and number of bins can be adjusted in the input.
    '''
    eta_bins = np.linspace(eta_min, eta_max, number_of_bins)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    N_in_bin, bin_edges = np.histogram(eta, bins=eta_bins)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_width = bin_centers[1] - bin_centers[0]
    dN_deta = N_in_bin/(bin_width*nevents)

    return bin_centers,dN_deta

def pseudorapidity_distribution_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments.
    '''
    number_events = number_of_events(particle_list_file)
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return pseudorapidity_distribution(px,py,pz,number_events, **kwargs)

### FUNCTIONS FOR PT DISTRIBUTION
def pt_distribution(px,py,pz,nevents,pt_max=3, pt_min=0, number_of_bins=50, etacut=0.5):
    '''
    Given the list of momenta px,py,pz and the number of SMASH events,
    returns a tuple with (bin_centers,<1/(2\pi p_T) dN/dpt>) 
    pt cuts and number of bins can be adjusted in the input
    '''
    pt = np.sqrt(px**2+py**2)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    pt_bins = np.linspace(pt_min,pt_max,number_of_bins)
    #selecting particles at midrapidity
    pt = pt[(np.fabs(eta)<etacut)]
    N_in_bin, bin_edges = np.histogram(pt, bins=pt_bins)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_width = bin_centers[1] - bin_centers[0]
    dN_dpt = N_in_bin/(bin_width*nevents*bin_centers*(2*np.pi))

    return bin_centers,dN_dpt

def pt_distribution_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    number_events = number_of_events(particle_list_file)
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return pt_distribution(px,py,pz,number_events,**kwargs)

### FUNCTIONS FOR FLOWS
def complex_flow_pt(px,py,pz,n_order=2,pt_min = 0,pt_max=3,number_of_bins=10,etacut=0.5):
    '''
    Return pt-bins and cos and sin information for the n_order flow harmonics.
    cuts and number of bins can be adjusted
    '''
    pt_bins = np.linspace(pt_min,pt_max,number_of_bins)
    pt = np.sqrt(px*px+py*py)
    phi = np.arctan2(py,px)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    #selecting particles at midrapidity
    pt = pt[(np.fabs(eta)<etacut)]
    phi = phi[(np.fabs(eta)<etacut)]
    cos, bin_edges = np.histogram(pt,bins=pt_bins,weights=np.cos(n_order*phi))
    sin, bin_edges = np.histogram(pt,bins=pt_bins,weights=np.sin(n_order*phi))

    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    nth_cos = cos/(np.histogram(pt,bins=pt_bins)[0])
    nth_sin = sin/(np.histogram(pt,bins=pt_bins)[0])

    return bin_centers, nth_cos, nth_sin

def complex_flow_pt_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return complex_flow_pt(px,py,pz,**kwargs)
 
def nth_flow_pt(px,py,pz,n_order=2,pt_min = 0,pt_max=3,number_of_bins=10,etacut=0.5):
    '''
    Return pt-bins and v_n flow of order n=n_order. Reaction plane angle is assumed to be zero (you can check this with complex_flow_pt).
    '''
    bin_centers, nth_flow, dummy_sin = complex_flow_pt(px,py,pz,n_order,pt_min=pt_min,pt_max = pt_max,number_of_bins=number_of_bins,etacut=etacut)
    return bin_centers, nth_flow

def nth_flow_pt_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return nth_flow_pt(px,py,pz,**kwargs)

def complex_flow_eta(px,py,pz,n_order=2,eta_min=-1, eta_max=1,number_of_bins=20):
    '''
    Return eta-bins and complex flow information for the n_order flow harmonics.
    '''
    eta_bins = np.linspace(eta_min,eta_max,number_of_bins)
    phi = np.arctan2(py,px)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    cos, bin_edges = np.histogram(eta,bins=eta_bins,weights=np.cos(n_order*phi))
    sin, bin_edges = np.histogram(eta,bins=eta_bins,weights=np.sin(n_order*phi))

    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    nth_cos = cos/(np.histogram(eta,bins=eta_bins)[0])
    nth_sin = sin/(np.histogram(eta,bins=eta_bins)[0])

    return bin_centers, nth_cos, nth_sin

def complex_flow_eta_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return complex_flow_eta(px,py,pz,**kwargs)
 
def nth_flow_eta(px,py,pz,n_order=1,eta_min=-1, eta_max=1,number_of_bins=10):
    '''
    Return eta-bins and v_n flow of order n=n_order. Reaction plane angle is assumed to be zero (you can check this with complex_flow_eta).
    '''
    bin_centers, nth_flow, dummy_sin = complex_flow_eta(px,py,pz,n_order,eta_min=eta_min,eta_max=eta_max,number_of_bins=number_of_bins)
    return bin_centers, nth_flow

def nth_flow_eta_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return nth_flow_eta(px,py,pz,**kwargs)

def complex_flow_y(E,px,py,pz,n_order=2,y_min=-1, y_max=1,number_of_bins=20):
    '''
    Return y-bins and complex flow information for the n_order flow harmonics.
    '''
    y_bins = np.linspace(y_min,y_max,number_of_bins)
    phi = np.arctan2(py,px)
    y = 0.5*np.log((E+pz)/(E-pz))
    cos, bin_edges = np.histogram(y,bins=y_bins,weights=np.cos(n_order*phi))
    sin, bin_edges = np.histogram(y,bins=y_bins,weights=np.sin(n_order*phi))

    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    nth_cos = cos/(np.histogram(y,bins=y_bins)[0])
    nth_sin = sin/(np.histogram(y,bins=y_bins)[0])

    return bin_centers, nth_cos, nth_sin

def complex_flow_y_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return complex_flow_y(E,px,py,pz,**kwargs)
 
def nth_flow_y(E,px,py,pz,n_order=1,y_min=-1, y_max=1,number_of_bins=10):
    '''
    Return eta-bins and v_n flow of order n=n_order. Reaction plane angle is assumed to be zero (you can check this with complex_flow_eta).
    '''
    bin_centers, nth_flow, dummy_sin = complex_flow_y(E,px,py,pz,n_order,y_min=y_min,y_max=y_max,number_of_bins=number_of_bins)
    return bin_centers, nth_flow

def nth_flow_y_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return nth_flow_y(E,px,py,pz,**kwargs)