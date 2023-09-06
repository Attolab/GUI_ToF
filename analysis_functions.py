import numpy as np
import scipy.interpolate as interpolate
class AnalysisFunctions():
    
    def get_SpeedOfLight(units_choice):
        if units_choice == 'nm/fs':
            coeff = 1
        else:
            coeff = 1
        return 0.299792458 * coeff

    def get_h(units_choice):
        if units_choice == 'nm/fs':
            coeff = 1
        else:
            coeff = 1
        return 0.658211957  #in ev.fs   

    def get_hBar():
        return 4.1356677 #in ev.fs


    def nm2eV(wavelength):
        # Convert photon wavelength in eV
        h = 4.1356677 # Planck's constant in eV.fs
        c = 299.792458 #Speed of light in nanometer/fs
        return h*c/wavelength

    def eV2ToF(E,alpha,beta,t0):
        return t0 + np.sqrt(alpha/(E-beta))
    def eV2ToF_potential(E,alpha,beta,t0,V,l):
        L = np.sqrt(2*alpha/9.1e-31)
        return t0 + np.sqrt(9.1e-31/2)*(l/np.sqrt(E-beta) + (L-l)/np.sqrt(E-beta+V))
    def eV2ToF_Jac(E,alpha,beta):
        return np.sqrt(alpha/(E-beta)**3)
    def eV2ToF_Jac_potential(E,alpha,beta,V,l):
        L = np.sqrt(2*alpha/9.1e-31)
        print("done")
        return np.sqrt(9.1e-31/2)*(l/np.sqrt((E-beta)**2) + (L-l)/np.sqrt((E-beta+V)**2))

    def ToF2eV(t,alpha,beta,t0):
        return alpha/(t-t0)**2 + beta
    def ToF2eV_Jac(t,alpha,t0):
        return 2*alpha/(t-t0)**3


    def goFromTimeToEnergy(axisTime, signalTime, alpha, beta, t0, doFlip=True):
        axisEnergy = AnalysisFunctions.ToF2eV(axisTime,alpha,beta,t0)
        signalEnergy = signalTime/AnalysisFunctions.ToF2eV_Jac(axisTime,alpha,t0)[:,np.newaxis]
        signalEnergy = signalTime
        if doFlip:            
            axisEnergy = np.flip(axisEnergy)
            signalEnergy = np.flip(signalEnergy,axis=0) 
        return axisEnergy,signalEnergy  


    def goFromEnergyToTime(axisEnergy, signalEnergy, alpha, beta, t0, doFlip=True):
        axisTime = AnalysisFunctions.eV2ToF(axisEnergy,alpha,beta,t0)
        signalTime = signalEnergy*AnalysisFunctions.eV2ToF_Jac(axisEnergy,alpha,beta)[:,np.newaxis]
        if doFlip:
            axisTime = np.flip(axisTime)
            signalTime = np.flip(signalTime,axis=0)
        return axisTime,signalTime  



    def linearizeData(xp_axis,datap,starting_x,ending_x,spacing_x,axis = 0):
        steps = int(np.round((ending_x - starting_x)/spacing_x))
        fit_interpolate = interpolate.interp1d(xp_axis,datap,axis = axis)
        if ending_x > xp_axis[-1]:
            ending_x = xp_axis[-1]
        if starting_x < xp_axis[0]:
            starting_x = xp_axis[0]            
        x_axis = np.linspace(starting_x,ending_x,steps)            
        return x_axis, fit_interpolate(x_axis)


    def getNumberOfSteps(starting_x,ending_x,spacing_x):
        return np.round((ending_x - starting_x)/spacing_x)        