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

def pseudorapidity_distribution(px,py,pz,nevents,eta_min=-4,eta_max=4, number_of_bins=50):
    '''
    Returns a tuple with (bin_centers,<dN/deta>)
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

def pseudorapidity_distribution_simple(particle_list_file, selection_criterion,**kwargs):
    '''
    Overload of the previous function with simpler arguments
    '''
    number_events = number_of_events(particle_list_file)
    E,px,py,pz = momentum_in_particle_selection(particle_list_file, selection_criterion)
    return pseudorapidity_distribution(px,py,pz,number_events, **kwargs)


def pt_distribution(px,py,pz,nevents,pt_max=3, pt_min=0, number_of_bins=50):
    '''
    Returns a tuple with (bin_centers,<1/(2\pi p_T) dN/dpt>) 
    The output of this function can be easily plotted unpacking with *:
        plt.plot(*pt_distribution, ... )
    '''
    pt = np.sqrt(px**2+py**2)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    pt_bins = np.linspace(pt_min,pt_max,number_of_bins)
    #selecting particles at midrapidity
    pt = pt[(np.fabs(eta)<0.5)]
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

def complex_flow_pt(px,py,pz,n_order=2,pt_min = 0,pt_max=3,number_of_bins=10):
    '''
    Return pt-bins and complex flow information for the n_order flow harmonics.
    '''
    pt_bins = np.linspace(pt_min,pt_max,number_of_bins)
    pt = np.sqrt(px*px+py*py)
    phi = np.arctan2(py,px)
    eta = 0.5*np.log((np.sqrt(px*px+py*py+pz*pz)+pz)/(np.sqrt(px*px+py*py+pz*pz)-pz))
    #selecting particles at midrapidity
    pt = pt[(np.fabs(eta)<0.5)]
    phi = phi[(np.fabs(eta)<0.5)]
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
 
def nth_flow_pt(px,py,pz,n_order=2,pt_min = 0,pt_max=3,number_of_bins=10):
    '''
    Return pt-bins and v_n flow of order n=n_order. Reaction plane angle is assumed to be zero (you can check this with complex_flow_pt).
    '''
    bin_centers, nth_flow, dummy_sin = complex_flow_pt(px,py,pz,n_order,pt_min=pt_min,pt_max = pt_max,number_of_bins=number_of_bins)
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

def Pz_polarization(polarization_file,vorticity=False, spin_to_polarization=2):
    '''
    Computes the z component of polarization as a function of phi from the particlizationCalc output.
    If vorticity = True plots only the contribution of the vorticity
    spin_to_polarization converts the mean spin formula to polarization. Particles are assumet to be S=1/2 by default.
    '''
    filename =  np.loadtxt(polarization_file, unpack=True)
    pT = filename[0]
    phi = filename[1]
    dndp = filename[2]
    dimP=np.size(np.unique(pT))
    dimPhi=np.size(np.unique(phi))
    if(vorticity):
        Pizu = filename[6]
    else:
        Pizu = filename[6] + filename[10]  

    Pz = Pizu.reshape((dimP,dimPhi))
    dNdP = dndp.reshape((dimP,dimPhi))
    Pt = pT.reshape((dimP,dimPhi))
    mean_spin = np.trapz(Pz*Pt,x=np.unique(pT),axis=0)
    spectra = np.trapz(dNdP*Pt,x=np.unique(pT),axis=0)

    pol = spin_to_polarization*mean_spin/spectra

    return np.unique(phi), pol

def Pj_polarization(polarization_file,vorticity=False, mass=1.115683 ,spin_to_polarization=2):
    '''
    Computes the component of polarization along J as a function of phi from the particlizationCalc output.
    If vorticity = True plots only the contribution of the vorticity
    spin_to_polarization converts the mean spin formula to polarization. 
    The particle at hand is assumed to be a Lambda by default.
    '''
    filename =  np.loadtxt(polarization_file, unpack=True)
    pT = filename[0]
    phi = filename[1]
    dndp = filename[2]
    px = pT * np.cos(phi)
    py = pT * np.sin(phi)
    dimP=np.size(np.unique(pT))
    dimPhi=np.size(np.unique(phi))
    if(vorticity):
        Pixu = filename[4]
        Piyu = filename[5]
    else:
        Pixu = filename[4] + filename[8]
        Piyu = filename[5] + filename[9]  

    #boost to the Particle rest frame
    Pix_rf = np.zeros(len(Piyu))
    Piy_rf = np.zeros(len(Piyu))
    for i in range(len(Piyu)):
        e = np.sqrt(mass*mass + pT[i]*pT[i])
        Pix_rf[i] = Pixu[i] - (Pixu[i]*px[i] + Piyu[i]*py[i])/(e*(e+mass))*px[i]  
        Piy_rf[i] = Piyu[i] - (Pixu[i]*px[i] + Piyu[i]*py[i])/(e*(e+mass))*py[i]
        
    Py = Piy_rf.reshape((dimP,dimPhi))
    dNdP = dndp.reshape((dimP,dimPhi))
    Pt = pT.reshape((dimP,dimPhi))
    mean_spin = np.trapz(Py*Pt,x=np.unique(pT),axis=0)
    spectra = np.trapz(dNdP*Pt,x=np.unique(pT),axis=0)

    pol = spin_to_polarization*mean_spin/spectra

    return np.unique(phi), -pol #The experimental y axis is opposite to the angular momentum