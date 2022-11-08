# Online Python compiler (interpreter) to run Python online.

# Write Python 3 code in this online editor and run it.
import numpy as np
import scipy.fft as fft
import scipy.signal.windows as windows
import scipy.signal as sc_sig
from scipy.optimize import least_squares, curve_fit
import matplotlib.pyplot as plt
import re
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
        
    def makeFilter(x,edges,edges_in=(True,True)):
        if edges_in[0]:
            mask = x >= edges[0]**2
        else:
            mask = x > edges[0]**2
        if edges_in[1]:
            mask *= x <= edges[1]**2
        else:
            mask *=x < edges[1]**2          
        return mask
    def PolarFilter(shape,center=None,radial_edges=None,radial_edges_in=(True,True),angular_edges=None,angular_edges_in=(True,True), belongTo=True):
        if center is None:
            c_x = shape/2
            c_y = c_x
        else: #Row/Col formalism
            c_x = center[1]
            c_y = center[0]
        x,y = np.ogrid[:shape[0],:shape[1]]
        mask = np.ones((shape),dtype=bool)
        if radial_edges is not None:
            r2 = (x-c_x)*(x-c_x) + (y-c_y)*(y-c_y)   
            mask *= Filter.makeFilter(r2,radial_edges,radial_edges_in)        
        if angular_edges is not None:
            theta = np.arctan2(x-c_x,y-c_y) 
            theta %= (2*np.pi)
            mask *= Filter.makeFilter(theta,np.deg2rad(angular_edges),angular_edges_in)                    
        if belongTo == 'out':
            mask = ~mask
        return mask


class FunctionDictionnary():

    class Gauss():
        # Gaussian function
        def getOutput(self, x, coefficients):
            a, x0, sigma = coefficients
            return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
        def getNumberOfParameters(self):
            return 3
        def getStandardInput(self):
            return np.array([1,0,1])
    class Polynomial():
        # Polynomial function
        def __init__(self,order = 0) -> None:
            self.order = order
        def getOutput(self,x,coefficients):            
            return np.polyval(coefficients,x)
        def getNumberOfParameters(self):
            return self.order 
        def getStandardInput(self):
            return np.ones((self.order))

    class Exponential():
        # Exponential function
        def getOutput(self,x,coefficients):   
            a,x0,b = coefficients 
            return a*np.exp(-b*(x-x0))
        def getNumberOfParameters(self):
            return 3 
        def getStandardInput(self):
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
        self.funcDic = FunctionDictionnary() #Class containing other function classes
        self.function_list = [self.extractMethodFromFunction(f) for f in function_list] #Array containing function class which has associated methods

        self.p = self.buildParameters()
        if initial_input.size != np.sum(self.p):
            self.p0 = self.buildInitialInput()
        else:
            self.p0 = initial_input
        # self.parameters_lsq = least_squares(self.getResidual, self.p0, args=(), **kwargs)
        parameters_lsq, pcov, infodict,mesg,ier = curve_fit(self.sumFunction, self.x, self.y,self.p0, **kwargs,full_output=True )

        if showOutput:
            import matplotlib.pyplot as plt
            # print(f'Cost: {self.parameters_lsq.cost};')
            # print(f'Termination condition: {self.parameters_lsq.status}')
            # print(f'Number of evaluations: {self.parameters_lsq.nfev}')
            plt.figure()
            # plt.plot(self.x,self.sumFunction(self.x,self.parameters_lsq))
            plt.plot(self.x,self.y,linestyle = '--',linewidth=2)
            # plt.plot(self.x,self.sumFunction(self.x,parameters_lsq),linestyle = '--',linewidth=2)
            self.plotFunction(parameters_lsq)
        print(f'Output:{parameters_lsq}')
        print(mesg)
        print(f'Success: {ier > 0}?')



        return self.makeOutput(function_list,parameters_lsq)

    def makeOutput(self,function_list,parameters,):
        output = []
        last_index=0
        for i,f in enumerate(function_list):
            current_index = last_index
            last_index = current_index + self.p[i]            
            output.append((f,parameters[current_index:last_index]))
        return output

    def extractFunctionfromMethod(self,m):
        if m == self.funcDic.Gauss():
            return 'gaussian'
    def extractMethodFromFunction(self,f):
        if 'gaussian' in f:
            return self.funcDic.Gauss()
        elif 'poly' in f:
            m = re.search(r"(\d+)", f)
            return self.funcDic.Polynomial(order=1+int(m.group(0)))

    def sumFunction(self,x,*input):        
        output = np.zeros_like(self.y)
        last_index=0
        for i,f in enumerate(self.function_list):
            current_index = last_index
            last_index = current_index + self.p[i]
            output += self.getOutput(f,input[current_index:last_index])
        return output
    # Plot all functions listed in function_list according to input
    def plotFunction(self,input,showSum=True):
        if showSum:
            output = np.zeros_like(self.y)
        last_index=0
        for i,f in enumerate(self.function_list):
            current_index = last_index
            last_index = current_index + self.p[i]
            if showSum:
                output = output + self.getOutput(f,input[current_index:last_index])
            plt.plot(self.x,self.getOutput(f,input[current_index:last_index]))        
        if showSum:
            plt.plot(self.x,output)        
        plt.show()
    # Calculate residual between expectations and fit
    def getResidual(self,p):     
        err = self.y - self.sumFunction(p)
        return err        
    # Get expected number of parameters to fit
    def buildParameters(self,):
        return [self.getNumberOfParameters(function) for function in self.function_list]
        
    # Make a standard input
    def buildInitialInput(self,):
        input = np.zeros(np.sum(self.p))
        last_index = 0
        for i,f in enumerate(self.function_list):
            current_index = last_index
            last_index = current_index + self.p[i]
            input[current_index:last_index] = self.getStandardInput(f)
        return input

    def getOutput(self,f,input):
        return f.getOutput(self.x,input)
    def getStandardInput(self,f):
        return f.getStandardInput()    
    def getNumberOfParameters(self,f):
        return f.getNumberOfParameters()    


class PeakFinder():

    def __init__(self,x=None,y=None) -> None:
        self.x = np.array(x)
        self.y = np.array(y)
    # Basic peak finder
    def findPeaksScipy(self,prominence=None, distance=None, rel_height=None):
        peak_indices,_ = sc_sig.find_peaks(self.y, prominence=prominence, distance = distance)
        results_half = sc_sig.peak_widths(self.y, peak_indices, rel_height=rel_height) # widths, width_heights, left intersection point, right intersection point        
        return peak_indices, results_half
        
    def makeInitialGuess(self,prominence=None, distance=None, rel_height=None,function_type ='gaussian',showOutput = False):
        peak_indices, results_half = self.findPeaksScipy(prominence,distance,rel_height)
        amplitude = self.y[peak_indices]
        mean = self.x[peak_indices]
        sigma = np.abs((self.x[np.round(results_half[0]).astype(int)]-self.x[0]) / (2 * np.sqrt(2 * np.log(2)))) # Go from FWHM to STD
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
                upperBounds[current_index:last_index] = [+np.inf, m + s, 1.2*a]
        if showOutput:
            plt.plot(self.x,self.y)
            plt.plot(mean,amplitude,'x')
            plt.show()
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
    A = PeakFitter(x=t,y=signal).fit(['gaussian','gaussian'],
                                    initial_input=initialGuess,bounds = tuple([lowerBounds, upperBounds]) ,showOutput = True)

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
