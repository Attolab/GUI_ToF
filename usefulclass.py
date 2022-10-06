# Online Python compiler (interpreter) to run Python online.

# Write Python 3 code in this online editor and run it.
import numpy as np
import scipy.fft as fft
import scipy.signal.windows as windows
import scipy.signal as sc_sig
from scipy.optimize import least_squares, curve_fit
import matplotlib.pyplot as plt

class FourierTransform:
    

    def zero_padd(x,deltaX): #Useful function to retrieve x after zero padding

        L = len(x)

        N = FourierTransform.next_power_of_2(L)

        x = np.linspace(x[0],x[-1] + deltaX*(N-L),N)

        return N,x



    def next_power_of_2(x):

        return 1 if x ==0 else 2**(x-1).bit_length() #Smart way to count power of 2 is to use bytes



    def do_Fourier(x,signal, N = 0, axis=1):

        if not(N):        #Check if input has been given, find the next power of 2 of its length otherwise

            N = FourierTransform.next_power_of_2(x.size)

        f = fft.fftfreq(N,x[1]-x[0]) * 2 * np.pi #frequency axis     
        F = fft.fftn(signal,s = N, axes = axis) #fourier transform
        f = np.roll(f,N//2)
        F = np.roll(F,N//2)
        return f,F

    def do_inverse_Fourier(f,F, N = 0,axis=1):

        if N == 0:        #Check if input has been given, find the next power of 2 of its length otherwise

            N = FourierTransform.next_power_of_2(x.size)
        x = fft.fftfreq(N,f[1]-f[0]) * 2 * np.pi #frequency axis     
        S = fft.ifftn(F,s = N,axes = axis) #fourier transform
        x = np.roll(x,N//2)
        S = np.roll(S,N//2)
        return x,S
    

    def do_Window(N,index,beta = 1): #Function to get windows according to index used

        if index == 0:

            W = np.ones(N)        

        elif index == 1:

            W = windows.hamming(N)

        elif index == 2:

            W = windows.hann(N)

        elif index == 3:

            W = windows.kaiser(N,beta)

        elif index == 4:

            W = windows.blackman(N)

        else:

            W = np.ones(N)

        return W     


class Filter:
    # Filter function for starting and ending function

    def ApplyFilter(x,y,start=False,end=False,axis = 0):    
        if not(isinstance(start, bool)):
                mask = x >= start
        else:
            mask = np.ones_like(x).astype(bool)
        if not(isinstance(end, bool)):        
            mask = np.logical_and(mask,x <= end)                            
        x = x[mask]
        if axis == 0:
            y = y[mask,:]
        elif axis == 1:
            y = y[:,mask]
        else:
             y = y[mask]             
        return x, y        



class FunctionDictionnary():

    class Gauss():
        # Gaussian function
        def gauss(self, x, a, x0, sigma):
            return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
        def getNumberOfParameters(self):
            return 3
        def getInitialInput(self):
            return np.array([1,0,1])

        # # Store parameters in parameter vector
        # def store_parameters(n_gaussian, amplitude, mean, sigma):
        #     p = np.zeros(shape=(3*n_gaussian,), dtype="float")
        #     p[0:3:n_gaussian] = amplitude
        #     p[1:3>n_gaussian:2 * n_gaussian] = mean
        #     p[2 * n_gaussian:3 * n_gaussian] = sigma
        #     return p
        # # Retrieve parameters from parameter vector
        # def extract_gaussian_parameters(p, n_gaussian):
        #     amplitude = p[0:n_gaussian]
        #     mean = p[n_gaussian:2 * n_gaussian]
        #     sigma = p[2 * n_gaussian:3 * n_gaussian]
        #     return amplitude, mean, sigma
class PeakFitter():

    def __init__(self,x=None,y=None) -> None:
        self.x = x
        self.y = y

    # Launch least_square command
    def fit(self,function_list=None,initial_input=None,showOutput = None, **kwargs):
        self.funcDic = FunctionDictionnary()
        self.function_list = function_list
        self.p = self.buildParameters()
        if not(initial_input.size):
            self.p0 = self.buildInitialInput()
        else:
            self.p0 = initial_input
        self.parameters_lsq = least_squares(self.getResidual, self.p0, args=(), **kwargs)
        print(f'Success: {self.parameters_lsq.success}?')
        if showOutput:
            import matplotlib.pyplot as plt
            print(f'Cost: {self.parameters_lsq.cost};')
            print(f'Termination condition: {self.parameters_lsq.status}')
            print(f'Number of evaluations: {self.parameters_lsq.nfev}')
            plt.figure()
            plt.plot(self.x,self.sumFunction(self.parameters_lsq.x))
            plt.plot(self.x,self.y,linestyle = '--')
            self.plotFunction(self.parameters_lsq)
            plt.show()
        print(f'Output:{self.parameters_lsq.x}')
        return self.parameters_lsq.x

    # Sum all functions listed in function_list according to input
    def sumFunction(self,input):
        output = np.zeros_like(self.y)
        last_index=0
        for i,f in enumerate(self.function_list):
            current_index = last_index
            last_index = current_index + self.p[i]
            output += self.getOutput(f,input[current_index:last_index])
        return output
    # Plot all functions listed in function_list according to input
    def plotFunction(self,input,):   
        last_index=0
        for i,f in enumerate(self.function_list):
            current_index = last_index
            last_index = current_index + self.p[i]
            plt.plot(self.x,self.getOutput(f,input[current_index:last_index]))        
        plt.show()
    # Calculate residual between expectations and fit
    def getResidual(self,p):     
        err = self.y - self.sumFunction(p)
        return err        

    def buildParameters(self,):
        return [self.getNumberOfParameters(function) for function in self.function_list]

    def buildInitialInput(self,):
        input = np.zeros(np.sum(self.p))
        last_index = 0
        for i,f in enumerate(self.function_list):
            current_index = last_index
            last_index = current_index + self.p[i]
            input[current_index:last_index] = self.getInitialInput(f)
        return input

    def getOutput(self,f,input):
        if f == 'gaussian':
            return self.funcDic.Gauss().gauss(self.x,*input)    
    def  getInitialInput(self,f):
        if f == 'gaussian':
            return self.funcDic.Gauss().getInitialInput()    
    def getNumberOfParameters(self,f):
        if f == 'gaussian':
            return self.funcDic.Gauss().getNumberOfParameters()
    # def n_gaussian_fit(prominence, distance, rel_height,n=None):
    #     if not(self.x.size):        
    #         x = np.arange(len(y))
    #     number_of_peaks, initial_guess, lb, ub = PeakFitter.make_initial_guess(x, y, prominence = prominence, distance = distance, rel_height=rel_height)
    #     parameters_lsq = least_squares(PeakFitter.res, initial_guess, args=(y, x, number_of_peaks), bounds=tuple([lb, ub]),max_nfev = 1e3)
    #     print(f'Success:{parameters_lsq.success}?')
    #     return parameters_lsq.x, number_of_peaks
    # Return initial guess from peak_finder
    # def make_initial_guess(self,prominence, distance, rel_height, peak_indices =None, results_half=None):
    #         peak_indices, results_half = PeakFinder.find_peaks_scipy(self.y, prominence=prominence, distance = distance, rel_height=rel_height)
    #         amplitude = self.y[peak_indices]
    #         mean = self.x[peak_indices]
    #         sigma = (self.x[np.round(results_half[0]).astype(int)]-self.x[0]) / (2 * np.sqrt(2 * np.log(2)))
    #         number_of_peaks = len(peak_indices)
    #         initial_guess = PeakFitter.store_gaussian_parameters(number_of_peaks, amplitude, mean, sigma)
    #         lb = np.concatenate((np.zeros(number_of_peaks), mean - sigma, np.zeros(number_of_peaks)))
    #         ub = np.concatenate((np.inf * np.ones_like(amplitude), mean + sigma, np.inf * np.ones_like(amplitude)))
    #         return number_of_peaks, initial_guess, lb, ub     


class PeakFinder():

    def __init__(self,x=None,y=None) -> None:
        self.x = x
        self.y = y
    # Basic peak finder
    def findPeaksScipy(self,prominence=None, distance=None, rel_height=None):
        peak_indices,_ = sc_sig.find_peaks(self.y, prominence=prominence, distance = distance)
        results_half = sc_sig.peak_widths(self.y, peak_indices, rel_height=rel_height) # widths, width_heights, left intersection point, right intersection point        
        return peak_indices, results_half
        
    def makeInitialGuess(self,prominence=None, distance=None, rel_height=None,function_type ='gaussian'):
        peak_indices, results_half = self.findPeaksScipy(prominence,distance,rel_height)
        amplitude = self.y[peak_indices]
        mean = self.x[peak_indices]
        sigma = (self.x[np.round(results_half[0]).astype(int)]-self.x[0]) / (2 * np.sqrt(2 * np.log(2))) # Go from FWHM to STD
        number_of_peaks = len(peak_indices)
        if function_type == 'gaussian':
            initial_guess = np.zeros(3*number_of_peaks)
            lowerBounds = np.zeros(3*number_of_peaks)
            upperBounds = np.zeros(3*number_of_peaks)
            last_index=0
            for (a, m, s) in zip(amplitude, mean, sigma):
                current_index = last_index
                last_index = current_index + 3
                initial_guess[current_index:last_index] = [a,m,s]
                lowerBounds[current_index:last_index] = [-np.inf, m - s, 1e-16]
                upperBounds[current_index:last_index] = [+np.inf, m + s, np.inf]

        return number_of_peaks, initial_guess, lowerBounds, upperBounds       


if __name__ == "__main__":    
    import matplotlib.pyplot as plt

    #Minimal example

    def gaussianPulse(t,amplitude,t0,FWHM):
        sigma = FWHM/(2*np.sqrt(2*np.log(2)))
        P = amplitude*np.exp(-(t-t0)**2/(2*sigma**2))
        return P
    def oscillation(t,omega,t0):
        S = np.cos(omega*(t-t0))       
        return S
    def laserPulse(t,amplitude,t0,FWHM,omega):
        P = gaussianPulse(t,amplitude,t0,FWHM)*oscillation(t,omega,t0)
        return P


    

    t = np.linspace(-100*np.pi,100*np.pi,10000) #Time axis
    amplitude = 1
    FWHM = 5
    phase = 0 #Phase
    t0 = 0
    omega = 1 #Frequency
    L = 1000
    delta_T = np.arange(-L/2,L/2)*2*np.pi/50




    signal = laserPulse(t,amplitude,t0,FWHM,omega) + laserPulse(t,amplitude,t0+delta_T[0],FWHM,omega)
    signal = gaussianPulse(t,amplitude,t0+delta_T[0],FWHM)+gaussianPulse(t,amplitude,t0+delta_T[-1],FWHM)
    a,b = PeakFinder(x=t,y=signal).findPeaksScipy(distance = 5, rel_height= 0.5, prominence= 0.5)
    numberOfPeaks,initialGuess, lowerBounds, upperBounds = PeakFinder(x=t,y=signal).makeInitialGuess(distance = 5, rel_height= 0.5, prominence= 0.5)
    A = PeakFitter(x=t,y=signal).fit(['gaussian','gaussian'],initial_input=initialGuess,ftol = None,bounds = tuple([lowerBounds, upperBounds]))

    # # delta_T = np.arange(L)*2*np.pi/10
    # S = np.zeros([delta_T.size,t.size])
    # F = np.zeros([delta_T.size,2**16])
    # # argF = np.zeros([delta_T.size,2**16])
    # fig, axs =  plt.subplots(1,2)
    # for i in range(L):
    #     signal = laserPulse(t,amplitude,t0,FWHM,omega) + laserPulse(t,amplitude,t0+delta_T[i],FWHM,omega)
    #     signal = signal*FourierTransform.do_Window(signal.size,0) #Windowed Signal
    #     f,F_temp = FourierTransform.do_Fourier(t,signal,N = 2**16) #Fourier transform of Signal        
    #     S[i] = signal
    #     F[i] = np.abs(F_temp)
    #     # argF[i] = np.unwrap(np.angle(F_temp))
    # pcm = axs[0].pcolormesh(t, delta_T, S, cmap='viridis', shading='nearest')
    # pcm = axs[1].pcolormesh(f, delta_T, F, cmap='viridis', shading='nearest') 
    # axs[1].set_xlim(0,8)
                  
    # # axs[0].contourf(t,delta_T,S,20,norm = norm)
    # # # axs[0].contour(X,Y,F)
    # # axs[1].contourf(f,delta_T,F,20,norm = norm)
    # # axs[1].imshow(F,aspect ='auto',extent=[np.min(f), np.max(f),np.min(delta_T), np.max(delta_T)])
    
    # # axs[2].contour(f,delta_T,argF,30)
    # # axs[2].set_xlim(0,8)
    # # signal = np.cos(omega*t) + np.cos(2*omega*t+phase) #Signal
    # # signal = np.cos(omega*t) + np.cos(omega*(t-np.pi/2)+phase) #Signal
    # # f,F = FourierTransform.do_Fourier(t,signal,N = 2**16) #Fourier transform of Signal        
    # # axs[1].plot(f,np.abs(F))
    # plt.show()
