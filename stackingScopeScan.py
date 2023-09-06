import h5py
import numpy as np
import re

from numpy import array as npa
from numpy import asarray as npaa



    # Get key for data array
def get_key_data(keys,data_label):
    # Extract key data and associated index 
    key_data, key_data_index = zip(
        *[(key, int(re.search('(\d+)$', key)[0])) for key in keys if data_label in key])
    # List is not sorted so we sort it using the index
    ordering_index = np.argsort(key_data_index)
    # Return sorted key_data array
    return npa(key_data)[ordering_index]

# Get key for position array
def get_key_position(keys):
    return npa([key for key in keys if "StagePosition" in key])

# Get key for parameters
def get_key_parameters(keys):
    return npa([key for key in keys if "Scan_parameters" in key])


def get_dataset_keys(f):
    keys = []        
    f.visit(lambda key: keys.append(key) if isinstance(f[key], h5py.Dataset) else None)
    return keys
def convertInput(inputs):
    return [input.decode('ISO-8859-1)') if input[0] == 80 else input for input in inputs]

def get_values(f, keys):
    # return [npa(np.squeeze(f[key])) if len(f[key].shape) > 1 else npa(f[key]) for key in keys]        
    return npaa([np.squeeze(npa(f[key])) for key in keys])



def readh5(filename):
    with h5py.File(filename, 'r') as file:
        keys = get_dataset_keys(file)
        keys = convertInput(keys)
        position = np.round(get_values(file, get_key_position(keys))[0],1)
        parameters = get_values(file, get_key_parameters(keys))
        data_transient = get_values(file, get_key_data(keys,"Data/Y_axis/Averaged_data")).T            
        try:
            data_statOn = get_values(file,get_key_data(keys,"Static spectra/Averaged_on")).T
            data_statOff = get_values(file,get_key_data(keys,"Static spectra/Averaged_off")).T
        except:
            data_statOn = np.zeros_like(data_transient)
            data_statOff = np.zeros_like(data_transient)

    max_entry = np.min([data_transient.shape[1],data_statOn.shape[1],data_statOff.shape[1]])
    data_transient=data_transient[:,:max_entry]
    data_statOn=data_statOn[:,:max_entry]
    data_statOff=data_statOff[:,:max_entry]
    position= position[:max_entry]     
    data = np.asarray([data_transient,data_statOn,data_statOff])    
    # delay = 2 * position / ( 0.299792458)
    t_vol = parameters[-2] * 1e9 * np.arange(data[0].shape[0])
    # indexing = np.argsort(delay)
    # position = position[indexing]
    # delay = delay[indexing]
    # data_statOn = data_statOn[:,indexing]
    # data_statOff = data_statOff[:,indexing]
    # data_transient = data_transient[:,indexing]   
    delay = position * 0.633 / ( 2 * np.pi * 0.299792458)

    signal_params = {'signal':{
                'signal_transient':data_transient ,'signal_statOn': data_statOn,'signal_statOff': data_statOff,
                },
                't_vol':t_vol,
                'delay':np.flip(position)
                }     
    return signal_params


def stackScan(filenames,):            
    for i,filename in enumerate(filenames):
        f = folder_init+filename+'.h5'
        signal_temp = readh5(f)
        if i == 0:
            signal_params = signal_temp
        else:
            for key in signal_params.keys():
                if type(signal_params[key]) is dict:
                    for key2 in signal_params[key].keys():
                        signal_params[key][key2] = np.append(signal_params[key][key2],signal_temp[key][key2],axis=1)
                else:
                    if key != 't_vol':
                        signal_params[key] = np.append(signal_params[key],signal_temp[key])
    return signal_params
    

def storeDic(filename,data):
    hf = h5py.File(filename, "w")
    for grp_name in data:
        grp = hf.create_group(grp_name)
        for dset_name in data[grp_name]:
            dset = grp.create_dataset(dset_name, data = data[grp_name][dset_name])
            print(grp_name, dset_name, data[grp_name][dset_name])
    hf.close() 
    
def orderSignals(signal_param,doOrder=False):    
    if doOrder:
        ordering = np.argsort(signal_params['delay'])
        signal_params['delay'] = signal_params['delay'][ordering]
        signal_params['signal']['signal_transient'] = signal_params['signal']['signal_transient'][:,ordering].T
        signal_params['signal']['signal_statOn'] = signal_params['signal']['signal_statOn'][:,ordering].T
        signal_params['signal']['signal_statOff'] = signal_params['signal']['signal_statOff'][:,ordering].T
    else:    
        signal_params['signal']['signal_transient'] = signal_params['signal']['signal_transient'].T
        signal_params['signal']['signal_statOn'] = signal_params['signal']['signal_statOn'].T
        signal_params['signal']['signal_statOff'] = signal_params['signal']['signal_statOff'].T
    return signal_params

def stackSamePos(signal_param_init,doStackSamePos=False):    
    signal_params = signal_param_init
    if doStackSamePos:    
        S = signal_param_init['signal']['signal_transient'].shape[1]
        upos = np.unique(signal_param_init['delay'],return_index=False)
        signal_params = {'signal':{
            'signal_transient':np.zeros((len(upos),S)) ,'signal_statOn': np.zeros((len(upos),S)),'signal_statOff': np.zeros((len(upos),S)),
            },
            't_vol':signal_param_init['t_vol'],
            'delay':upos
            }     
        for i,pos in enumerate(upos):
            mask = (pos == signal_param_init['delay'])
            signal_params['signal']['signal_transient'][i] = np.mean(signal_param_init['signal']['signal_transient'][mask],axis=0)
            signal_params['signal']['signal_statOn'][i] = np.mean(signal_param_init['signal']['signal_statOn'][mask],axis=0)
            signal_params['signal']['signal_statOff'][i] = np.mean(signal_param_init['signal']['signal_statOff'][mask],axis=0)    
    else:
        signal_params = signal_param_init
    return signal_params








folder_init = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SEI_2023/20230802/'
filenames = ['Ne - Ne_3','Ne - Ne_4','Ne - Ne_5']
filename_out = folder_init+'Ne_Ne_DECAP_20230802.h5'

# folder_init = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SEI_2023/20230810/'
# filenames = ['Ne_Ne_1','Ne_Ne_0']
# filename_out = folder_init+'Ne_Ne_DECAP_20230810.h5'


# folder_init = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SEI_2023/20230810/'
# filenames = ['Ne_Ar_2','Ne_Ar_1','Ne_Ar_0']
# filename_out = folder_init+'Ne_Ar_DECAP_20230810.h5'


# doStackSamePos = True
# doOrder = True
signal_params = stackScan(filenames,)
signal_params = orderSignals(signal_params,doOrder=True)
signal_params = stackSamePos(signal_params,doStackSamePos=True)
    

data = dict()
data['Parameters'] = dict(bin_axis=signal_params['t_vol'],position=signal_params['delay'])

H = [signal_params['signal']['signal_transient'],signal_params['signal']['signal_statOff'],signal_params['signal']['signal_statOn']]
data['Data'] = dict(data=H)


# storeDic('test',data)
storeDic(filename_out,data)


a = 0
    
    
    
    

