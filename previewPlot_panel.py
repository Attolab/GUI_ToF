from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,Signal,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QTransform,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QCloseEvent)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QPushButton,
    QSizePolicy, QWidget, QFileDialog)
from previewPlot_panel_ui import Ui_previewPlot_Panel
from signal_processing_toolbox import SignalProcessingToolbox
import pyqtgraph as pg
from usefulclass import FourierTransform
from usefulclass import Filter
import pyqtgraph.graphicsItems.NonUniformImage as NonUniformImage
from viewer2D_widget import Viewer2DWidget
from scipy.interpolate import interp1d
import numpy as np
from file_manager import FileManager as FM7
import csv

class PreviewPlot_Panel(Ui_previewPlot_Panel,QWidget):
    signal_updatePlot = Signal(object,object,object) # [2D, x ,y ]
    signal_sendData = Signal(object)
    signal_sendParameterAxis = Signal(object)
    def __init__(self,parent=None, axis_0 = [], axis_1 = [], signal = np.zeros((3,3))):
        super(PreviewPlot_Panel, self).__init__(parent)        
        # Set up the user interface from Designer.
        self.setupUi(self)
        # Initialize connections
        self.connectSignal()
        # Set up the plotwidgets
        self.setupPlotWidget()
        self.isNotProcessing = True
        self.setData(signal,axis_0,axis_1)
        # Show plot
        self.displayPlotWidget()     
        self.path_folder = ""   

    def setData(self,data,axis_0,axis_1):
        self.signal_input = np.array(data)
        # Store input        
        if len(axis_0)!=0:
            self.axis0_input = np.array(axis_0)
        else:
            self.axis0_input = np.arange(np.shape(self.signal_input)[1],dtype=float)
        if len(axis_1)!=0:
            self.axis1_input = np.array(axis_1)
        else:
            self.axis1_input = np.arange(np.shape(self.signal_input)[0],dtype=float)               
        self.n_sample = self.signal_input.shape[0]         
        # Update the settings and the parameters on the GUI according to input
        self.isCalibrated = False
        self.updateSettings()

    def getRawData(self):
        return [self.axis0_input,self.axis1_input,self.signal_input]   

    def getData(self,output_choice):
        if output_choice == 'Signal':
            output = [self.axis1_inputPlot,np.sum(self.signal_inputPlot,axis=1)]
        elif output_choice == 'FT':
            output = [self.axis1_inputPlot,np.abs(np.sum(self.signal_outputPlot,axis=1))] 

        self.signal_sendData.emit(output)
        
    def setupPlotWidget(self):        
        self.inputViewerWidget = Viewer2DWidget(name = 'Signal')
        self.signalInput_groupBox.layout().addWidget(self.inputViewerWidget)
        self.outputMagnViewerWidget = Viewer2DWidget(name = 'FT magnitude')
        self.outputPhaseViewerWidget = Viewer2DWidget(name = 'FT phase')
        self.signalOutput_groupBox.layout().addWidget(self.outputMagnViewerWidget)
        self.signalOutput_groupBox.layout().addWidget(self.outputPhaseViewerWidget)
        self.outputMagnViewerWidget.view_2D.setYLink(self.outputPhaseViewerWidget.view_2D)
        self.outputMagnViewerWidget.view_2D.setXLink(self.outputPhaseViewerWidget.view_2D)

    def _updatePlotWidget(self,):      
        self.checkVisibleWidget()
        self.displayPlotWidget()

    def showHideWidget(self,items,show_bool = True):
        if show_bool:        
            [item.show() for item in items]
        else:
            [item.hide() for item in items]

    def checkVisibleWidget(self):
        self.showHideWidget([self.signalInput_groupBox],self.signal_checkBox.isChecked())
        self.showHideWidget([self.outputPhaseViewerWidget],self.FT_phase_checkBox.isChecked())
        self.showHideWidget([self.outputMagnViewerWidget],self.FT_magn_checkBox.isChecked())
        if (self.FT_magn_checkBox.isChecked()) or (self.FT_phase_checkBox.isChecked()):
            self.signalOutput_groupBox.show()
        else:
            self.signalOutput_groupBox.hide()

    def displayPlotWidget(self):
        self.inputViewerWidget.updateViewerWidget(self.signal_inputPlot,self.axis0_inputPlot,self.axis1_inputPlot)
        self.outputMagnViewerWidget.updateViewerWidget(np.abs(self.signal_outputPlot),self.axis0_outputPlot,self.axis1_inputPlot)
        angle = np.angle(self.signal_outputPlot)
        # angle = np.unwrap(np.angle(self.signal_outputPlot),axis = 0)
        # angle -= np.min(angle,axis =1)
        # self.outputPhaseViewerWidget.updateViewerWidget(angle-angle[0][:,np.newaxis].T,self.axis0_outputPlot,self.axis1_inputPlot) 
        self.outputPhaseViewerWidget.updateViewerWidget(angle,self.axis0_outputPlot,self.axis1_inputPlot)        
        # self.outputPhaseViewerWidget.updateViewerWidget(np.unwrap(np.angle(self.signal_outputPlot),axis = 0),self.axis0_outputPlot,self.axis1_inputPlot)        

    def connectSignal(self):    
        self.configuration_button.clicked.connect(self.openConfig)  
        self.signal_checkBox.stateChanged.connect(self.checkVisibleWidget)
        self.FT_phase_checkBox.stateChanged.connect(self.checkVisibleWidget)
        self.FT_magn_checkBox.stateChanged.connect(self.checkVisibleWidget)        

    def _update_signal_toolboxParameters(self):
        if (hasattr(self,'_signal_processing_toolbox')) & (self.isCalibrated):
            self.parameter_list_signal_toolbox = dict(self._signal_processing_toolbox.widget_extraction.extractValues())            
        else:
            try:
                self.parameter_list_signal_toolbox = [('inputAxis0Start_doubleSpinBox', np.min(self.axis0_input)),
                            ('inputAxis0End_doubleSpinBox', np.max(self.axis0_input)),
                            ('inputAxis1Start_doubleSpinBox', np.min(self.axis1_input)),
                            ('inputAxis1End_doubleSpinBox', np.max(self.axis1_input)),                        
                            ('interpolation_comboBox', 0),
                            ('interpolation_spinBox', int(self.n_sample)),
                            ('removeBackground_comboBox', 0),
                            ('removeBackground_doubleSpinBox', np.mean(self.signal_input)),
                            ('FT_window_comboBox', 2),
                            ('FT_zeropadding_comboBox', 1),
                            ('FT_zeropaddingpower2_spinBox',11),
                            ('FT_zeropadding_spinBox', FourierTransform.next_power_of_2(self.n_sample)),
                            ('outputAxisStart_doubleSpinBox', 0),
                            ('outputAxisEnd_doubleSpinBox', np.pi/(self.axis0_input[1]-self.axis0_input[0])),
                            ('inputAxis0Mult_lineEdit',1.0),
                            ('inputAxis1Mult_lineEdit',1.0),
                            ('inputAxis0Add_doubleSpinBox',0.0),
                            ('inputAxis1Add_doubleSpinBox',0.0),
                            ('outputAxisMult_lineEdit',1.0),                                                                          
                            ]  
            except:
                print('Problem inititializing data, check input')
                return
            self.isCalibrated = True
            self.parameter_list_signal_toolbox = dict(self.parameter_list_signal_toolbox)       
            self._signal_processing_toolbox = SignalProcessingToolbox(item_list = self.parameter_list_signal_toolbox)                        
            self.connectSignalToolbox()            
            self.signal_sendParameterAxis.emit(['inputAxis0Start_doubleSpinBox','inputAxis0End_doubleSpinBox',self.axis0_input])
            self.signal_sendParameterAxis.emit(['inputAxis1Start_doubleSpinBox','inputAxis1End_doubleSpinBox',self.axis1_input])
                
    def openConfig(self):          
        self._update_signal_toolboxParameters()
        self._signal_processing_toolbox.show()
        # self._signal_processing_toolbox.raise_()

    def connectSignalToolbox(self):
        self._signal_processing_toolbox.emitSettings.connect(self.updateSettings)
        self._signal_processing_toolbox.signal_comboBox.connect(self.updateParameters)
        self.signal_sendParameterAxis.connect(self._signal_processing_toolbox.updateAxisSettings)

    def updateParameters(self,widget_name,value):
        getattr(self._signal_processing_toolbox,str)
        # self.parameter_list_signal_toolbox[widget_name = value]

    def updateSettings(self):
        import time
        if self.isNotProcessing:
            print("Update Settings")
            self._update_signal_toolboxParameters()
            start = time.time()            
            self.isNotProcessing = False
            self._processParameters()
            self._signal_processing_toolbox.widget_extraction.initializeValues(self.parameter_list_signal_toolbox)    

            if self.check_plotInput():
                self._updatePlotWidget()
            self.isNotProcessing = True
            print(time.time()-start)

    def check_axis(self,axes):
        return all([len(axis) != 0 for axis in axes])
    def check_plotInput(self):
        return self.check_axis([self.axis0_outputPlot,self.axis0_inputPlot,self.axis1_inputPlot])
         
    def updateZeroPadding(self):
        if self.parameter_list_signal_toolbox['FT_zeropadding_comboBox'] == 0:
            n_fourier = FourierTransform.next_power_of_2(self.parameter_list_signal_toolbox['interpolation_spinBox'])
        elif self.parameter_list_signal_toolbox['FT_zeropadding_comboBox'] == 1:       
            n_fourier = 2**self.parameter_list_signal_toolbox['FT_zeropaddingpower2_spinBox']
        elif self.parameter_list_signal_toolbox['FT_zeropadding_comboBox'] == 2:            
            n_fourier = self.n_sample
        elif self.parameter_list_signal_toolbox['FT_zeropadding_comboBox'] == 3:            
            n_fourier = self.parameter_list_signal_toolbox['FT_zeropadding_spinBox']    
        return n_fourier

    def updateInterpolation(self):
        if self.parameter_list_signal_toolbox['interpolation_comboBox']:
            n_sampling = self.parameter_list_signal_toolbox['interpolation_spinBox']
            if self.parameter_list_signal_toolbox['interpolation_comboBox'] == 1:
                fit = interp1d(self.axis0_inputPlot, self.signal_inputPlot, kind='linear')
            elif self.parameter_list_signal_toolbox['interpolation_comboBox'] == 2:                        
                fit = interp1d(self.axis0_inputPlot, self.signal_inputPlot, kind='cubic')
            self.axis0_inputPlot = np.linspace(self.axis0_inputPlot[0], self.axis0_inputPlot[-1], num=n_sampling, endpoint=True)                            
            self.signal_inputPlot = fit(self.axis0_inputPlot)  
        else:
            self.parameter_list_signal_toolbox['interpolation_spinBox'] = self.n_sample 

    def removeBackground(self):
        if self.parameter_list_signal_toolbox['removeBackground_comboBox'] == 0:            
            self.parameter_list_signal_toolbox['removeBackground_doubleSpinBox'] = np.mean(self.signal_inputPlot)                   
        elif self.parameter_list_signal_toolbox['removeBackground_comboBox'] == 1:
            self.parameter_list_signal_toolbox['removeBackground_doubleSpinBox'] = np.mean(self.signal_inputPlot[0])
        elif self.parameter_list_signal_toolbox['removeBackground_comboBox'] == 2:            
            self.parameter_list_signal_toolbox['removeBackground_doubleSpinBox'] = np.mean(self.signal_inputPlot[-1])
        elif self.parameter_list_signal_toolbox['removeBackground_comboBox'] == 3:            
            self.parameter_list_signal_toolbox['removeBackground_doubleSpinBox'] = np.min(self.signal_inputPlot)
        return self.parameter_list_signal_toolbox['removeBackground_doubleSpinBox']
                                   

    def updateInputAxis0(self):
        [self.axis0_inputPlot,self.signal_inputPlot] = Filter.ApplyFilter(self.axis0_input,self.signal_input,
                                                            start=self.parameter_list_signal_toolbox['inputAxis0Start_doubleSpinBox'],
                                                            end=self.parameter_list_signal_toolbox['inputAxis0End_doubleSpinBox'],axis = 1)  
        if self.parameter_list_signal_toolbox['inputAxis0Add_doubleSpinBox'] != 0.:            
            self.axis0_inputPlot += self.parameter_list_signal_toolbox['inputAxis0Add_doubleSpinBox']   
        if self.parameter_list_signal_toolbox['inputAxis0Mult_lineEdit']  is not float:
            self.parameter_list_signal_toolbox['inputAxis0Mult_lineEdit'] = float(self.parameter_list_signal_toolbox['inputAxis0Mult_lineEdit'])
        if self.parameter_list_signal_toolbox['inputAxis0Mult_lineEdit'] != 1.:
            self.axis0_inputPlot *= self.parameter_list_signal_toolbox['inputAxis0Mult_lineEdit']        


    def updateInputAxis1(self):
        [self.axis1_inputPlot,self.signal_inputPlot] = Filter.ApplyFilter(self.axis1_input,self.signal_inputPlot,
                                                            start=self.parameter_list_signal_toolbox['inputAxis1Start_doubleSpinBox'],
                                                            end=self.parameter_list_signal_toolbox['inputAxis1End_doubleSpinBox'],axis = 0) 
        if self.parameter_list_signal_toolbox['inputAxis1Add_doubleSpinBox'] != 0.:
            self.axis1_inputPlot += self.parameter_list_signal_toolbox['inputAxis1Add_doubleSpinBox']   
        if self.parameter_list_signal_toolbox['inputAxis1Mult_lineEdit']  is not float:
            self.parameter_list_signal_toolbox['inputAxis1Mult_lineEdit'] = float(self.parameter_list_signal_toolbox['inputAxis1Mult_lineEdit'])            
        if self.parameter_list_signal_toolbox['inputAxis1Mult_lineEdit'] != 1.:
            self.axis1_inputPlot *= self.parameter_list_signal_toolbox['inputAxis1Mult_lineEdit']  

    def updateOutputAxis0(self):
        self.signal_sendParameterAxis.emit(['outputAxisStart_doubleSpinBox','outputAxisEnd_doubleSpinBox',self.axis0_outputPlot])
        [self.axis0_outputPlot,self.signal_outputPlot] = Filter.ApplyFilter(self.axis0_outputPlot,self.signal_outputPlot,
                                                            start=self.parameter_list_signal_toolbox['outputAxisStart_doubleSpinBox'],
                                                            end=self.parameter_list_signal_toolbox['outputAxisEnd_doubleSpinBox'],axis = 1)                                                                 
        if self.parameter_list_signal_toolbox['outputAxisMult_lineEdit']  is not float:
            self.parameter_list_signal_toolbox['outputAxisMult_lineEdit'] = float(self.parameter_list_signal_toolbox['outputAxisMult_lineEdit'])                                                             
        if self.parameter_list_signal_toolbox['outputAxisMult_lineEdit'] != 1.:                                                            
            self.axis0_outputPlot *= self.parameter_list_signal_toolbox['outputAxisMult_lineEdit']    

    def _processParameters(self):
        self.updateInputAxis0()
        self.updateInputAxis1()                                                                 
        self.n_sample = self.axis0_inputPlot.shape[0]
        self.signal_inputPlot -= self.removeBackground()
        self.updateInterpolation()
        self.parameter_list_signal_toolbox['FT_zeropadding_spinBox'] = self.updateZeroPadding()
        [self.axis0_outputPlot,self.signal_outputPlot] = self.doFourierTransform(self.axis0_inputPlot,self.signal_inputPlot,
                                                            N = int(self.parameter_list_signal_toolbox['FT_zeropadding_spinBox']),
                                                            windowchoice=self.parameter_list_signal_toolbox['FT_window_comboBox'])                                                          
        self.updateOutputAxis0()                                                                 

    def doFourierTransform(self,x,y,N=None,windowchoice = 0) -> np.array:    
        return FourierTransform.do_Fourier(x,y*FourierTransform.do_Window(len(x),windowchoice),N) #Windowed Signal,N = npad) #Fourier transform of Signal  


    def closeEvent(self, event: QCloseEvent) -> None:
        if hasattr(self,'_signal_processing_toolbox'):
            self._signal_processing_toolbox.close()
        return super().closeEvent(event)



def main():
    import h5py
    import file_manager
    import sys
    import numpy as np
    def gaussianPulse(t,amplitude,t0,FWHM):
        sigma = FWHM/(2*np.sqrt(2*np.log(2)))
        P = amplitude*np.exp(-(t-t0)**2/(2*sigma**2))
        return P

    def oscillation(t,omega,t0):
        S = np.cos(omega*(t-t0))       
        return S
    def laserPulse(t,amplitude,t0,FWHM,omega):
        if np.size(t0)>1:
            t0 = t0[:,np.newaxis]
        P = gaussianPulse(t,amplitude,t0,FWHM)*oscillation(t,omega,t0)
        return P      
    

    
    app = QApplication([])

    from file_manager import FileManager as F
    folder ='/home/cs268225/Documents/Python/GUI/FourierGUI/TestData/Dataset_20220415_002/'
    filename = 'Dataset_20220415_002.h5'
    fileread = F(folder + filename)

    t = np.linspace(-150,1000,10000) #Time axis
    amplitude = 1
    FWHM = 5
    t0 = 0
    omega = 2*np.pi*374.74057*1e-3 #Frequency
    delta_T = np.linspace(380,420,41)
    S = laserPulse(t,amplitude,t0,FWHM,omega) + laserPulse(t,amplitude,t0+delta_T,FWHM,omega) #Total Signal
    signal_panel = PreviewPlot_Panel(axis_0 = t,signal = S)
    signal_panel.show()
    app.exec()

    
if __name__=="__main__":
    main()

