import numpy as np
import matplotlib.pyplot as plt
from abel.tools import polar
from scipy.special import eval_legendre, hyp2f1, factorial
from scipy.interpolate import interp1d
import os.path
import time
class Abel_object():
    def __init__(self, data, center_y, center_x, d_alpha_deg, dr, N, Rmax, parent=None):
        """
            Creates an object that can Abel invert an image using the DAVIS
            (Direct Algorithm for Velocity-map Imaging) technique described in
            https://doi.org/10.1063/1.5025057

            Parameters
            ----------
            data : 2D np.array
                The data to invert
            center_y : int
                y coordinate of the center of the image, corresponds to vertical axis / rows
            center_x : int
                x coordinate of the center of the image, corresponds to horizontal axis / cols            
            d_alpha_deg : float
                Angular coordinate spacing (in degrees)
            dr : int
                Radial coordinate spacing for the inverted array
            N : int
                number of photons. Determines the number of legendre polynomials
                to use (which is equal to 2N+1)
                ex: if N=1 then P0, P1 and P2 are used, if N=2 then P0 to P4 are used.
            Rmax : int
                maximum radius up to which the image is inverted
        """

        self.parent = parent

        self.center_x = center_x
        self.center_y = center_y
        self.d_alpha_deg = d_alpha_deg
        self.d_alpha = d_alpha_deg * np.pi / 180  # deg to rad conversion
        self.dr = dr
        self.N = N
        self.Rmax = Rmax

        self.Ny, self.Nx = data.shape

        self.N_alpha = int(2 * np.pi / self.d_alpha)
        self.N_R = int(Rmax/dr)
        self.R_vector = np.linspace(dr, Rmax, self.N_R)
        self.data_polar, r_grid, theta_grid = polar.reproject_image_into_polar(
            data, origin=(center_y, center_x), dr=dr, dt=self.d_alpha, Jacobian=True)
        self.alpha_vector = theta_grid[0,:]

        self.M_inv = {}
        self.Mnk = {}
        self.F = {}

    def set_data(self, data):
        if data.shape != (self.Ny, self.Nx):
            print('Incorrect data shape')
            raise ValueError
        self.data_polar, r_grid, theta_grid = polar.reproject_image_into_polar(
            data, origin=(self.center_y, self.center_x), dr=self.dr, dt=self.d_alpha, Jacobian=True)

    def show(self, data):
        plt.figure()
        # g = plt.pcolormesh(data.T)
        g = plt.imshow(data, cmap='jet', origin='lower')
        plt.colorbar(g)
        plt.show()

    def falling_factorial(self, x, m):
        prod = 1
        for i in range(int(m)):
            prod *= (x-i)
        return prod

    def summand_cnkl(self, n,k,l,p):
        ''' this function is used by the c function'''
        return self.falling_factorial(2*(n-2*k+l-p),2*(l-p))/\
                    self.falling_factorial(2*(l-p),2*(l-p))*self.c(n,k-l+p,p)
    def C(self,n,k,l):
        ''' This function is defined in eqn. 6 and used in the Gamma function
                to calculate the transformation matrices Mn,n-2k'''
        C = (-1)**(k-l)*2**(2*l+1)/factorial(k-l)*self.c(n,k,l)
        return C        
    def c(self, n,k,l):
        ''' This function is defined in eqn. 7 and used in the Gamma function
         to calculate the transformation matrices Mn,n-2k'''
        c = self.falling_factorial(n-k+l-1/2,k-l)*self.falling_factorial(n-k,l)*\
            self.falling_factorial(n-2*k+2*l-1/2,2*l)/(self.falling_factorial(2*l,2*l)*\
                                                       self.falling_factorial(n-k+l-1/2,l))
        if l>0:
            c = c - 1/(2**(k+l))*np.array([self.summand_cnkl(n,k,l,p) for p in range(0,l)]).sum()
        return c

    def Gammma(self,n,k,l,i,ip):
        ''' This function is defined in eqn. 11 and used to calculate the transformation matrices Mn,n-2k '''
        step = dr / 2
        R_minus = self.R_vector[i] - step
        R_plus = self.R_vector[i] + step
        if ip==i:
            R_plus -= step # this is a trick of mine, otherwise R_plus/R_vector[ip] > 1
            # and the hypergeometric function in eqn. 11 is not defined
        try:
            Gamma = 1/(2+2*l-2*k+n)*\
                  (((R_plus)/self.R_vector[ip])**(2+2*l-2*k+n)*\
                   hyp2f1(1/2+l-k,1+l-k+n/2,2+l-k+n/2,(R_plus/self.R_vector[ip])**2)\
                - ((R_minus)/self.R_vector[ip])**(2+2*l-2*k+n)*\
                   hyp2f1(1/2+l-k,1+l-k+n/2,2+l-k+n/2,(R_minus/self.R_vector[ip])**2))
            return Gamma
                # I replaced R_vector[i]+dr/2 by R_vector[i]
        except ZeroDivisionError:
            print('ZeroDivisionError in Gamma function')

    def M_eq13(self,N_R, n, k): # from equation 13
        ''' This function calculates the upper triangular transformation matrices Mn,n-2k using the formula of eqn. 13
        It uses the functions Gamma and c. It is not currently used but I thought it could be useful for n>4'''
        sM = np.zeros((N_R,N_R))
        for i in range (0, N_R):
            for ip in range(i, N_R):
                sM[i,ip] = np.array([self.C(n,k,l)*self.dr*self.d_alpha* \
                                            self.Gammma(n,k,l,i,ip) for l in range(0,max(k-1,0)+1)]).sum()
        return sM

    def M(self,N_R,n,k):
            ''' This function calculates the upper triangular transformation matrices Mn,n-2k using the analytical formulas
            from Table I. I checked that it's equal to M_eqn13(N_R,n,k). However it's faster than M_eq13 so this is the function
            actually used '''
            d_alpha = self.d_alpha
            dr = self.dr
            M = np.zeros((N_R,N_R))
            coeff = dr*d_alpha
            for i in range (0, N_R):
                for ip in range(i, N_R):
                    if ip == i:
                        R_plus = self.R_vector[i]
                    else:
                        R_plus = self.R_vector[i] + dr/2 # Ri ^ = Ri + DeltaR/2
                    R_minus = self.R_vector[i] - dr/2 # Ri v = Ri - DeltaR/2
                    R_ip = self.R_vector[ip] # ri'
                    R_plus_frac = R_plus/R_ip  # Ri ^ / Ri
                    R_minus_frac = R_minus/R_ip # Ri v  / Ri 
                    sqrtR_plus = np.sqrt(1-(R_plus_frac)**2) # (1 - (Ri ^  / Ri)^2)^1/2
                    sqrtR_minus = np.sqrt(1-(R_minus_frac)**2) # (1 - (Ri v  / Ri)^2)^1/2
                    asin_Rdiff =  np.arcsin(R_plus_frac) - np.arcsin(R_minus_frac) # asin(Ri ^ / Ri) - asin(Ri v / Ri)
                    if(n==0 and k==0): # M00
                        M[i,ip] = 2*coeff*(sqrtR_minus-sqrtR_plus)
                    elif(n==1 and k==0): # M11                 
                        M[i,ip] = coeff*\
                                (R_minus_frac*sqrtR_minus-R_plus_frac*sqrtR_plus+asin_Rdiff)
                    elif(n==2 and k==0): # M22
                        M[i,ip] = 2*coeff/3*\
                                (sqrtR_minus*(2+R_minus_frac**2)-sqrtR_plus*(2+R_plus_frac**2))
                    elif(n==2 and k==1): # M20
                        M[i,ip] = coeff/3*(sqrtR_plus**3-sqrtR_minus**3)
                    elif(n==3 and k==0): # M33
                        M[i,ip] = coeff/4*\
                                (R_minus_frac*sqrtR_minus*(3+2*R_minus_frac**2)
                                 -R_plus_frac*sqrtR_plus*(3+2*R_plus_frac**2)\
                                 +3*asin_Rdiff)
                    elif(n==3 and k==1): # M31
                        M[i,ip] = 3*coeff/8*\
                                (R_minus_frac*sqrtR_minus*(-1+2*R_minus_frac**2)\
                                 -R_plus_frac*sqrtR_plus*(-1+2*R_plus_frac**2)\
                                 -asin_Rdiff)                        
                    elif(n==4 and k==0): # M44
                        M[i,ip] = 2*coeff/15*\
                                (sqrtR_minus*(8+4*R_minus_frac**2+3*R_minus_frac**4)\
                                 -sqrtR_plus*(8+4*R_plus_frac**2+3*R_plus_frac**4))
                    elif(n==4 and k==1): # M42
                        M[i,ip] = coeff/3*\
                                (sqrtR_plus**3*(2+3*R_plus_frac**2)\
                                 -sqrtR_minus**3*(2+3*R_minus_frac**2))
                    elif(n==4 and k==2): # M40 (error in the article)
                        M[i,ip] = coeff/(60)*\
                                (sqrtR_plus**3*(19+51*R_plus_frac**2)\
                                 -sqrtR_minus**3*(19+51*R_minus_frac**2))
                    elif(n==5 and k==0): # M55
                        M[i,ip] = coeff/24*\
                               (sqrtR_minus*R_minus_frac*(15+10*R_minus_frac**2+8*R_minus_frac**4)\
                                 -sqrtR_plus*R_plus_frac*(15+10*R_plus_frac**2+8*R_plus_frac**4)\
                                 +15*asin_Rdiff)                                         
                    elif(n==5 and k==1): # M53
                        M[i,ip] = 7*coeff/48*\
                                (sqrtR_minus*R_minus_frac*(-3-2*R_minus_frac**2+8*R_minus_frac**4)\
                                 -sqrtR_plus*R_plus_frac*(-3-2*R_plus_frac**2+8*R_plus_frac**4)\
                                 -3*asin_Rdiff)        
                    elif(n==5 and k==2): # M51
                        M[i,ip] = coeff/64*\
                                (sqrtR_minus*R_minus_frac*(-81-134*R_minus_frac**2+296*R_minus_frac**4)\
                                 -sqrtR_plus*R_plus_frac*(-81-134*R_plus_frac**2+296*R_plus_frac**4)\
                                 -81*asin_Rdiff)     
                    elif(n==6 and k==0): # M66 (not in the article)
                        M[i,ip] = 2*coeff/35*\
                                (sqrtR_minus*(16+8*R_minus_frac**2+6*R_minus_frac**4+5*R_minus_frac**6)\
                                 -sqrtR_plus*(16+8*R_plus_frac**2+6*R_plus_frac**4+5*R_plus_frac**6))                                     
                    elif(n==6 and k==1): # M64 (not in the article)
                        M[i,ip] = coeff/35*\
                                (sqrtR_plus**3*(24+36*R_plus_frac**2+45*R_plus_frac**4)\
                                 -sqrtR_minus**3*(24+36*R_minus_frac**2+45*R_minus_frac**4))
                    elif(n==6 and k==2): # M62 (not in the article)
                        M[i,ip] = coeff/84*\
                                  (sqrtR_plus**3*(422 + 633*R_plus_frac**2 + 975*R_plus_frac**4)\
                                   -sqrtR_minus**3*(422 + 633*R_minus_frac**2 + 975*R_minus_frac**4))
                    elif(n==6 and k==3): # M60 (not in the article)                     
                        M[i,ip] = coeff/1680*\
                                (sqrtR_plus**3*(-536 - 1329*R_plus_frac**2 + 2670*R_plus_frac**4)
                                -sqrtR_minus**3*(-536 - 1329*R_minus_frac**2 + 2670*R_minus_frac**4))
                    else: #Take the numerical solution otherwise
                        M[i,ip] = np.array([self.C(n,k,l)*self.dr*self.d_alpha* \
                                            self.Gammma(n,k,l,i,ip) for l in range(0,max(k-1,0)+1)]).sum()                                
            return M        

    def precalculate(self):
        N = self.N
        filename = 'dr_' + (str(self.dr) + '_da_' + '{:.2f}'.format(self.d_alpha_deg) + '_N_' + \
                            str(self.N) + '_center_x_' + \
                            str(self.center_x) + '_y_' + str(self.center_y) + \
                            '_Rmax_' + str(self.Rmax)).replace('.','p') + '.npy'
        print(filename)
        if os.path.isfile('M_inv_'+filename):
            print('matrices already precalculated, loading them...')
            self.M_inv = np.load('M_inv_'+filename, allow_pickle='TRUE').item()
            self.Mnk = np.load('Mnk_'+filename, allow_pickle='TRUE').item()
        else:
            print('precalculating matrices...')
            for k in range(0, 2 * N + 1):
                self.M_inv[k] = np.linalg.inv(self.M(self.N_R, k, 0))  # inverse of M_kk
                try:
                    self.parent.progress_precalc.setValue(int((k + 1) / (2 * N + 1) * 50))
                    self.parent.progress_precalc.repaint()
                except AttributeError:
                    print(int((k + 1) / (2 * N + 1) * 50), " %")

            for k in range(2 * N, -1, -1):  # reversed loop from 2N to 0 included
                if k % 2 == 0:  # even k
                    if k == 2 * N:  # no sum over i
                        pass
                    elif k == 2 * N - 2:  # only one term in the sum
                        i = 1
                        self.Mnk[(k + 2 * i, i)] = self.M(self.N_R, k + 2 * i, i)
                    else:
                        for i in range(1, N - k // 2 + 1):
                            self.Mnk[(k + 2 * i, i)] = self.M(self.N_R, k + 2 * i, i)
                elif k % 2 == 1:  # odd k
                    for i in range(1, N - (int(k / 2) + 1) + 1):
                        self.Mnk[(k + 2 * i, i)] = self.M(self.N_R, k + 2 * i, i)
                try:
                    self.parent.progress_precalc.setValue(int((2 * N + 1 - k) / (2 * N + 1) * 50 + 50))
                    self.parent.progress_precalc.repaint()
                except AttributeError:
                    print(int((2 * N + 1 - k) / (2 * N + 1) * 50 + 50), " %")
            print('precalculation done, saving matrices as ', filename)
            np.save('M_inv_' + filename, self.M_inv)
            np.save('Mnk_' + filename, self.Mnk)

    def invert(self):
        N = self.N
        delta = np.zeros([2 * N + 1, self.N_R])
        for k in range(0, 2 * N + 1):
            for Ri in range(0, self.N_R):
                delta[k, Ri] = (2 * k + 1) / 2 * \
                        np.trapz(np.abs(np.sin(self.alpha_vector))*\
                        eval_legendre(k, np.cos(self.alpha_vector))*\
                        self.data_polar[Ri, :],dx=self.d_alpha) * 0.5
                        # I added the 0.5 because we integrate between 0 and 2pi
                        # instead of between 0 and pi

        # Application of eqn. 19
        for k in range(2 * N, -1, -1):  # reversed loop from 2N to 0 included
            if k % 2 == 0:  # even k
                if k == 2 * N:  # no sum over i
                    m2 = delta[k]
                elif k == 2 * N - 2:  # only one term in the sum
                    i = 1
                    m2 = delta[k] - np.dot(self.Mnk[(k + 2 * i, i)], self.F[k + 2 * i])
                else:
                    m2 = delta[k] - np.array(
                        [np.dot(self.Mnk[(k + 2 * i, i)], self.F[k + 2 * i]) \
                         for i in range(1, N - k // 2 + 1)]).sum(axis=0)
                self.F[k] = np.dot(self.M_inv[k], m2)
            elif k % 2 == 1:  # odd k
                m2 = delta[k] - np.array(
                    [np.dot(self.Mnk[(k + 2 * i, i)], self.F[k + 2 * i]) \
                     for i in range(1, N - (int(k / 2) + 1) + 1)]).sum(axis=0)
                self.F[k] = np.dot(self.M_inv[k], m2)        
   
    def reconstruct(self,sel=None):
            # Reconstruction of the Abel-inverted image
            Nr = int(self.Rmax/self.dr)
            Rvect = np.linspace(self.dr, self.Rmax, Nr)
            Sinv = np.zeros([2048, 2048])
            X_vect = np.arange(2048)-self.center_x
            Y_vect = np.arange(2048)-self.center_y
            
            nx = len(X_vect)
            S = np.zeros([nx**2])
            R = np.sqrt(X_vect**2+Y_vect[:,np.newaxis]**2).flatten()
            cosTh = np.cos(np.arctan2(X_vect,Y_vect[:,np.newaxis])).flatten()
            mask = np.logical_and(R>0, R<self.Rmax)
            cosTh = cosTh[mask]
            R = R[mask]            
            if sel is None:
                L = np.arange(2*self.N+1)
            elif sel is str:
                if sel == 'even':
                    L = L[0::2]
                elif sel == 'odd':
                    L = L[1::2]
            elif sel is list:
                L = sel[sel<=self.N]
            for l in L:
                S[mask] += interp1d(Rvect, self.F[l])(R)*eval_legendre(l, cosTh) 
            S[mask] = S[mask]/R
            Sinv = S.reshape([nx,nx])

            plt.figure()
            plt.imshow(Sinv, origin='lower', cmap='jet')
            plt.show()

if __name__ == '__main__':
    from file_manager import FileManager as FM
    from usefulclass import Filter
    path = 'Q:\LIDyL\Atto\ATTOLAB\SE1\Data_Experiments\SE1_2021\\2021-02-15\\'
    # path = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SE1_2021/2021-02-15/'
    path = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SE1_2022/2022-09-26/'
    filename = 'Slow rabbit With BlueShift at 500kV_1.h5'
    # filename='Ar-He_PE_Vrep1p0_Vext_0p794_MCP700+300_PMCP2p6em5_7p1em6_avg100_WITHfilter_WITHdrilled_WITHSB_2p3W_better.npy'
    # data = np.load(path+filename)
    fileManager = FM(filename=path+filename, format='VMI')
    data = np.squeeze(fileManager.readVMIData_h5(500))
    ############# INPUT PARAMETERS ##########################################
    transpose = False
    remove_bkg = False
    # center_x = 992  # vertical axis if the data is transposed
    # center_y = 1018  # vertical axis if the data is transposed
    center_x = 1026  # vertical axis if the data is transposed
    center_y = 1027  # vertical axis if the data is transposed
    d_alpha_deg = 0.1  # increment in angle alpha (in degrees)
    dr = 1  # increment in radius r
    N = 2  # number of photons. Determines the number of legendre polynomials to use (which is equal to 2N+1)
    # ex: if N=1 then P0, P1 and P2 are used. If N=2 then P0 to P4 are used.
    Rmax = 500  # maximum radius up to which the image is inverted
    #########################################################################
    Vmax = 5000
    if transpose:
        data = np.transpose(data)
    if remove_bkg:
        data = data - data[0:200,0:200].mean()
    # center_y = 2048 - center_y  # because of the top/bottom coordinate convention
    data *= Filter.PolarFilter(data.shape,(center_y,center_x),radial_edges=(0,1000),)

    plt.figure('Raw image')
    plt.imshow(data,origin ='lower',cmap='jet')
    abel_obj = Abel_object(data, center_y, center_x, d_alpha_deg, dr, N, Rmax)    
    abel_obj.show(data)
    abel_obj.precalculate()
    t = 0
    L = 10
    for i in range(L):
        t_init = time.time()
        abel_obj.invert()
        t += time.time()-t_init        
    print(t/L)
    # abel_obj.invert()

    fig = plt.figure(num=None, figsize=(9, 4.5), dpi=100, tight_layout=True)
    ax = plt.subplot(1,1,1)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    ax.set_xlabel("Radius (pixels)", fontsize=14)
    ax.set_ylabel("Intensity (arb. u.)", fontsize=14)
    for i in range(len(abel_obj.F)):
        ax.plot(abel_obj.F[i], label=f'P{i}')
    plt.legend()    
    plt.show()
    abel_obj.reconstruct()
    reconstr = False
    if reconstr:
        abel_obj.reconstruct()
        # Reconstruction of the Abel-inverted image
        Nr = int(Rmax/dr)
        Rvect = np.linspace(dr, Rmax, Nr)
        Sinv = np.zeros([2048, 2048])
        X_vect = np.arange(2048)-center_x
        Y_vect = np.arange(2048)-center_y
        
        h0 = interp1d(Rvect, abel_obj.F[0])
        h2 = interp1d(Rvect, abel_obj.F[2])
        h4 = interp1d(Rvect, abel_obj.F[4])

        L = len(X_vect)
        S = np.zeros([L**2])
        R = np.sqrt(X_vect**2+Y_vect[:,np.newaxis]**2).flatten()
        cosTh = np.cos(np.arctan2(X_vect,Y_vect[:,np.newaxis])).flatten()
        mask = np.logical_and(R>0, R<Rmax)
        cosTh = cosTh[mask]
        R = R[mask]
        S[mask] = 1/R*(h0(R) 
                        + h2(R)*eval_legendre(2, cosTh) 
                        + h4(R)*eval_legendre(4, cosTh) 
                            ) 
        Sinv = S.reshape([L,L])

        plt.figure()
        plt.imshow(Sinv, origin='lower', cmap='jet')
        plt.show()
