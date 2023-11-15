from typing import OrderedDict
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QTabWidget,
    QWidget,QFileDialog)

from pyqtgraph.parametertree import Parameter
import pathlib
import h5py
from numpy import array as npa
from numpy import asarray as npaa

import sys, traceback
import numpy as np
import os
import re
import time

class FileManager:
    def __init__(self, filename = None,format = None):
        self.filename = filename
        self.format = format
        self.dataset_list= []
        # if not self.format:
        #     filename,self.format = os.path.splitext(self.filename)
        # try:
        #     self.makeKeyList()
        # except:
        #     return
            
    # def makeKeyList(self):
    #     with h5py.File(self.filename, 'r') as file:
    #         # keys = self.get_dataset_keys(file)
    #         # keys = self.convertInput(keys)
    #         # self.parameter_key = get_key_parameters(keys)
    #         self.position_key = ['StagePosition/Position_um']
    #         self.data_key = [f"Data/Y_axis/Averaged_data_{index}" for index in np.arange(len(self.get_values(file,self.position_key)[0]))]
    def readFile(self,units='rad'):
        if self.format == 'MBES':
            return self.Read_h5(units=units)
        elif self.format == 'TDC':
            return self.Read_TDC_h5(units=units)        
        elif self.format == 'VMI':
            return self.ReadCamera_h5()

    def makeParameter(self):
        folder,filename_withext = os.path.split(self.filename)
        filename,ext = os.path.splitext(filename_withext)
        size = os.path.getsize(self.filename )
        file_params =  {
                'fullpath':{
                    'title': 'filename',
                    'type': 'str',
                    'value': self.filename,
                    'editable':False,
                    'readonly':True,
                    },               
                'dir': {
                    'title': 'folder',                                        
                    'type': 'str',
                    'value': folder,
                    'editable':False,
                    'readonly':True,                    
                    },   
                'ext': {
                    'title':'ext',                                        
                    'type': 'str',
                    'value': ext,
                    'editable':False,
                    'readonly':True,                                        
                    },    
                'size': {
                    'title':'size',                                        
                    'type': 'int',
                    'value': size,
                    'editable':False,
                    'readonly':True,                                        
                    },      
        }
        return Parameter.create(name=filename_withext, type='group',expanded = False,children = file_params,removable = True,renamable=False)

               

    def get_keys(self,f):
        return [key for key in f.keys()]

    def list_keys(self,group):
        return group.keys()
# Create a list containing all the keys

    def get_dataset_keys(self,f):
        keys = []        
        f.visit(lambda key: keys.append(key) if isinstance(f[key], h5py.Dataset) else None)
        return keys
    def get_values_TDC(self, f, keys):
        L = len(keys)
        for i,key in enumerate(keys):
            _data = npa(f[key])
            if len(_data.shape)>1: 
                _data = _data[-1]
            if i == 0:
                data = np.zeros((L,len(_data)))
            data[i]=_data
        return data
 
    def get_values(self, f, keys):
        # return [npa(np.squeeze(f[key])) if len(f[key].shape) > 1 else npa(f[key]) for key in keys]        
        return npaa([np.squeeze(npa(f[key])) for key in keys])

    def get_type(self, value):
        return value.dtype

    def get_shape(self, value):
            return value.shape

    def extractValues(self,filename,keys):
        with h5py.File(filename, 'r') as file:
            return [self.get_values(file,key) for key in keys]  
        
    def extractType(self,filename,keys):
        with h5py.File(filename, 'r') as file:
            return [self.get_type(self.get_values(file,key)) for key in keys]    

    def extractShape(self,filename,keys):
        with h5py.File(filename, 'r') as file:
            return [self.get_shape(self.get_values(file,key)) for key in keys]    

    def extractKeys(self,filename):
        with h5py.File(filename, 'r') as file:
            return self.get_dataset_keys(file)

    def extractAll(self):
        with h5py.File(self.filename, 'r') as file:
            keys = self.extractKeys(file)
            values = self.get_values(self, file, keys)
            shape = values.shape
            dtype = values.dtype
        return keys,values,shape,dtype       

    def convertInput(self,inputs):
        return [input.decode('ISO-8859-1)') if input[0] == 80 else input for input in inputs]


    def ReadCamera_h5(self):
        with h5py.File(self.filename, 'r') as file:
            keys = self.get_dataset_keys(file)
            keys = self.convertInput(keys)
            parameters = self.get_values(file, get_key_parameters(keys))
            position = self.get_values(file, get_key_position(keys))[0]
            data = npa(self.get_values(file, get_key_data(keys,"Data/Y_axis/Averaged_data"))).T        
    def ExtractMetaData_h5(self):
        with h5py.File(self.filename, 'r') as file:
            keys = self.get_dataset_keys(file)
            keys = self.convertInput(keys)
            # dataFrame = len(get_key_data(keys,"Data/Y_axis/Averaged_data"))
            # parameters = self.get_values(file, get_key_parameters(keys))
            position = self.get_values(file, get_key_position(keys))[0]    
        return position
    def readVMIData_h5(self,index):
        with h5py.File(self.filename, 'r') as file:
            data = self.get_values(file,[self.data_key[index]])            
        return data.T
    
    # def loadFileHist_h5(filename,):
    #     with h5py.File(filename, 'r') as file:
    #         stage_position = np.array(file[stage_pattern]) # Loqd stage position
    #         bin,size = (np.array(file[p]) for p in parameters_pattern) # Loqd bin+hist size
    #         data_hist = np.zeros((len(stage_position),size)) 
    #         # Extract keys from coinc
    #         keys = get_dataset_keys(file)
    #         keys = np.array(convertInput(keys))
    #         # Loop through positions
    #         for i,pos in enumerate(stage_position):
    #             data_hist[i] = np.array(file[f'{data_pattern}{int(pos)}']) # Load mean hist
    #     return data_hist    
    
    def convertParameterAxis(self,parameterAxis,units='rad'):
        if units == 'rad':
            return parameterAxis * 0.6328 / ( 2 * np.pi * 0.299792458)
        elif units == 'fs':
            return parameterAxis
        elif units == 'micrometer':
            return parameterAxis * 2 / ( 0.299792458)
        else:
            return parameterAxis
    def Read_TDC_h5(self,units='rad'):        
        with h5py.File(self.filename, 'r') as file:
            data_hist = np.array(file['Data']['data'])
            stage_position = np.array(file['Parameters']['position'])
            t_vol = np.array(file['Parameters']['bin_axis'])*1e9
            if data_hist.shape[0] != 3:
                data_transient = data_hist.T
                data_statOff = data_transient
                data_statOn = data_transient
            else:
                data_transient = data_hist[0].T
                data_statOn = data_hist[1].T
                data_statOff = data_hist[-1].T
        delay = self.convertParameterAxis(stage_position,units)
        # delay = stage_position * 0.6328 / ( 2 * np.pi * 0.299792458)
        # delay = delay[:len(data_hist)]
        # delay,indexing = np.unique(delay,return_index=True)
        # data_statOn = data_statOn[:,indexing]
        # data_statOff = data_statOff[:,indexing]
        # data_hist = data_hist[:,indexing]   
        signal_params = {'signal':{
                    'signal_transient':data_transient ,'signal_statOn': data_statOn,'signal_statOff': data_statOff,
                    },
                    't_vol':t_vol,
                    'delay':delay
                    }                                        
        return signal_params
    
    def storeDic(self,filename,data):
        with h5py.File(filename, "w") as hf:
            for grp_name in data:
                grp = hf.create_group(grp_name)
                for dset_name in data[grp_name]:
                    dset = grp.create_dataset(dset_name, data = data[grp_name][dset_name])
                    print(grp_name, dset_name, data[grp_name][dset_name])
        

    def Read_TDC_h5_old(self):
        parameters_pattern = [f"Scan_parameters/bin",f"Scan_parameters/size",f"Scan_parameters/numberOfMeasurements",f"Scan_parameters/exposureTime"]
        stage_pattern = f"StagePosition/Scan"
        data_pattern = f"Data/On/Scan"
        index = 0
        with h5py.File(self.filename, 'r') as file:
            keys = self.get_dataset_keys(file)
            key_pos = f'{stage_pattern}{index}phase'
            bin,N_bins,N_measurements,exp_time = (np.array(file[p]) for p in parameters_pattern)
            stage_position = np.array(file[key_pos]) # Load stage position
            data_hist = np.zeros((len(stage_position),N_bins)) 

            for i,pos in enumerate(stage_position):
                key_data = f'{data_pattern}{index}Averaged_on{i}'
                data_hist[i] = np.array(file[key_data]) # Load mean hist
            data_hist = data_hist.T
            data_statOn = np.zeros_like(data_hist)
            data_statOff = np.zeros_like(data_hist)

        t_vol = bin*27.4*1e-3*np.arange(N_bins)
        delay = stage_position * 0.6328 / ( 2 * np.pi * 0.299792458)
        delay = delay[:len(data_hist)]
        delay,indexing = np.unique(delay,return_index=True)
        # delay = 2 * position / ( 0.299792458)
        # indexing = np.argsort(delay)
        # delay = delay[indexing]
        data_statOn = data_statOn[:,indexing]
        data_statOff = data_statOff[:,indexing]
        data_hist = data_hist[:,indexing]   
        signal_params = {'signal':{
                    'signal_transient':data_hist ,'signal_statOn': data_statOn,'signal_statOff': data_statOff,
                    },
                    't_vol':t_vol,
                    'delay':delay
                    }                                        
        return signal_params
    
    def Read_h5(self,units='rad'):
        with h5py.File(self.filename, 'r') as file:
            keys = self.get_dataset_keys(file)
            keys = self.convertInput(keys)
            position = self.get_values(file, get_key_position(keys))[0]
            parameters = self.get_values(file, get_key_parameters(keys))
            data_transient = self.get_values(file, get_key_data(keys,"Data/Y_axis/Averaged_data")).T            
            try:
                data_statOn = self.get_values(file,get_key_data(keys,"Static spectra/Averaged_on")).T
                data_statOff = self.get_values(file,get_key_data(keys,"Static spectra/Averaged_off")).T
            except:
                data_statOn = np.zeros_like(data_transient)
                data_statOff = np.zeros_like(data_transient)        
        # Kill extra entries when programs crashes
        L_min = np.min([position.shape[0],data_statOn.shape[1],data_statOff.shape[1],data_transient.shape[1]])  
        position=position[:L_min]
        data_statOn=data_statOn[:,:L_min]
        data_statOff=data_statOff[:,:L_min]
        data_transient=data_transient[:,:L_min]

        delay = self.convertParameterAxis(position,units)
        t_vol = parameters[-2] * 1e9 * np.arange(data_transient.shape[0])
        indexing = np.argsort(delay)
        delay = delay[indexing]
        data_statOn = data_statOn[:,indexing]
        data_statOff = data_statOff[:,indexing]
        data_transient = data_transient[:,indexing]   

        signal_params = {'signal':{
                    'signal_transient':data_transient ,'signal_statOn': data_statOn,'signal_statOff': data_statOff,
                    },
                    't_vol':t_vol,
                    'delay':delay
                    }                                        
        return signal_params
    
    
    def Read_h5(self,units='rad'):
        with h5py.File(self.filename, 'r') as file:
            keys = self.get_dataset_keys(file)
            keys = self.convertInput(keys)
            position = self.get_values(file, get_key_position(keys))[0]
            parameters = self.get_values(file, get_key_parameters(keys))
            data_transient = self.get_values(file, get_key_data(keys,"Data/Y_axis/Averaged_data")).T            
            try:
                data_statOn = self.get_values(file,get_key_data(keys,"Static spectra/Averaged_on")).T
                data_statOff = self.get_values(file,get_key_data(keys,"Static spectra/Averaged_off")).T
            except:
                data_statOn = np.zeros_like(data_transient)
                data_statOff = np.zeros_like(data_transient)        
        # Kill extra entries when programs crashes
        L_min = np.min([position.shape[0],data_statOn.shape[1],data_statOff.shape[1],data_transient.shape[1]])  
        position=position[:L_min]
        data_statOn=data_statOn[:,:L_min]
        data_statOff=data_statOff[:,:L_min]
        data_transient=data_transient[:,:L_min]

        delay = self.convertParameterAxis(position,units)
        t_vol = parameters[-2] * 1e9 * np.arange(data_transient.shape[0])
        indexing = np.argsort(delay)
        delay = delay[indexing]
        data_statOn = data_statOn[:,indexing]
        data_statOff = data_statOff[:,indexing]
        data_transient = data_transient[:,indexing]   

        signal_params = {'signal':{
                    'signal_transient':data_transient ,'signal_statOn': data_statOn,'signal_statOff': data_statOff,
                    },
                    't_vol':t_vol,
                    'delay':delay
                    }                                        
        return signal_params
    

    def convert_h5(self,data,position,parameters):
        delay = position * 0.633 / ( 2 * np.pi * 0.299792458)        
        t_vol = parameters[-2] * 1e9 * np.arange(data[0].shape[0])
        indexing = np.argsort(delay)
        delay = delay[indexing]
        data = data[:,:,indexing]


        return data,delay,t_vol

    def readCalibration(self):
        with open(self.filename, "r") as f:  
            file_content = f.read().split()
            if len(file_content) != 8:
                print('File non valid')
                return None
            else:
                headers = file_content[0:4]
                coeffs = file_content[4:8]
                [print(f'{headers[i]}: {coeffs[i]}') for i in range(3)]
                return [float(coeff) for coeff in coeffs]

    def writeCalibration(self,calibration_inputs):
        if self.filename == '':
            print('Filename is empty')
            return
        else:         
            with open(self.filename, "w") as f:       
                [f.write(letter+'\t') for letter in ['A','B','t0','R2']]
                f.write('\n') 
                [f.write(item.text()+'\t') for item in calibration_inputs]
            print(f'Calibration saved as {self.filename}')


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

   

# class FileReadMBES():
#     def __init__(self, filename = None):
#         self.filename = filename
#         self.parameter = Parameter()
#         self.makeParameter()
    
#     def makeParameter(self):
#         Parameter.create(name='signal',title='Signal',type='group',children = [])
#         Parameter.create(name='signal',title='Signal',type='group')

#         Parameter.create(name='signal',title='Signal',type='group')




















def main():
    from file_manager import FileManager as F
    import matplotlib.pyplot as plt

    ############################# TEST #######################

    # MBES
    folder = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SE1_2022/2022-09-08/'
    filename = 'Ne-Xe_1.h5'
    file_format = 'MBES'

    # VMI
    # folder = '/home/cs268225/Atto/ATTOLAB/SE1/Data_Experiments/SE1_2022/2022-09-21/'
    # filename = 'Slow rabbit test _good.h5'
    # file_format = 'VMI'



    a = F(folder+filename,file_format).readFile()    

    a = 1

if __name__ == "__main__":
    main()