import h5py
import numpy as np
import re

from numpy import array as npa
from numpy import asarray as npaa




    

def storeDic(filename,data):
    hf = h5py.File(filename, "w")
    for grp_name in data:
        grp = hf.create_group(grp_name)
        for dset_name in data[grp_name]:
            dset = grp.create_dataset(dset_name, data = data[grp_name][dset_name])
            print(grp_name, dset_name, data[grp_name][dset_name])
    hf.close() 
    




import os

# folder_init='Q:\\LIDyL\\Atto\\ATTOLAB\\SE1\\Data_Experiments\\SEI_2023\\20231114\\'
folder_init = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SEI_2023/'

date = '20231115'
folder_init = f'/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SEI_2023/{date}/'
folder_init = f'C:\\Data\\2023\\{date}\\'
dataset = '002'
filename = f'Dataset_{date}_{dataset}.h5'
folder_out = folder_init+f'{date}_{dataset}/'
with h5py.File(folder_init+filename,'r') as f:
    if not os.path.isdir(folder_out):
        os.mkdir(folder_out)    
    for n in range(len(f['RawData'].keys())-1):    
        scan = f['RawData'][f'Scan{n:03}']
        
        signal = scan[f'Detector{0:03}']['Data1D'][f'CH{0:02}']
        # axis = f['RawData'][f'Scan{0:03}'][f'Actuator{0:03}']['Data1D'][f'CH{0:02}']

        parameters = scan['NavAxes']
        psize = []
        parameter_axis = []
        for key in parameters.keys():
            parameter_axis.append(np.array(parameters[key]))
            psize.append(len(parameters[key]))
            
        shutter = len(parameters.keys())>1
                
        signal_temp = []
        axis_temp = []
        key_list = signal.keys()
        for channel in key_list:            
            if 'Data' in channel:
                if shutter:
                    signal_temp.append(np.array(signal[channel]))
                else:
                    signal_temp.append(np.array(signal[channel]))
            elif 'Axis' in channel:
                axis_temp.append(np.array(signal[channel]))
        
        t_axis = axis_temp[0]*1e-3 #in ns                
        for i,sig in enumerate(signal_temp):
            data = dict()
            data['Parameters'] = dict(bin_axis=t_axis,position=parameter_axis[np.argmax(psize)])         
            data['Parameters'] = dict(bin_axis=t_axis,position=np.arange(0,55)*0.5)         
            # parameter_axis[np.argmin(psize)]%2
            if shutter:       
                sig_on = np.squeeze(sig[:,np.squeeze(np.where(parameter_axis[np.argmin(psize)]%2==1)),:])
                sig_off = np.squeeze(sig[:,np.squeeze(np.where(parameter_axis[np.argmin(psize)]%2==0)),:])
                sig_transient = np.squeeze(np.mean(sig_on - sig_off,axis=1))
                sig_on = np.squeeze(np.mean(sig_on,axis=1))
                sig_off = np.squeeze(np.mean(sig_off,axis=1))
                H = [sig_transient, sig_on , sig_off]
            else:
                H = np.squeeze(sig)
            data['Data'] = dict(data=H)


            filename_out = f'{dataset}_Scan{n:03}_Data{i:02}'
            storeDic(folder_out+filename_out,data)

    

    
    

