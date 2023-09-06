from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QTransform,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QCloseEvent)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QPushButton,QListWidgetItem,
    QSizePolicy, QWidget, QFileDialog,QMenu)
import os
from main_panel_ui import Ui_main_panel
from previewPlot_panel import PreviewPlot_Panel
from file_manager import FileManager as FM
from calibration_toolbox import CalibrationToolBox
from analysis_functions import AnalysisFunctions as af
import numpy as np
from usefulclass import Filter
from convertinator_class import Convertinator as C
from viewer1D_widget import Viewer1DWidget
import matplotlib.pyplot as plt
from variable_panel import VariablePanel

class MainPanel(Ui_main_panel,QWidget):
    def __init__(self,parent=None):
        super(MainPanel, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.hasCalibration = False
        self.isDataLoaded = False
        self.energyAxisDefined = False
        self.path_folder = ''
        self.path_calib = 'Calibration/'
        self.setupGUI()
        self.connectSignals()

    ################################################## Widget functions ##########################################    
    def closeEvent(self, event: QCloseEvent) -> None:
        if hasattr(self,'calibration_toolbox'):
            self.calibration_toolbox.close()
        if hasattr(self,'plotPreview_panel'):
            self.plotPreview_panel.close()            
        return super().closeEvent(event)

    def setupGUI(self):
        self.calibration_toolbox = CalibrationToolBox()
        self.plotPreview_panel = PreviewPlot_Panel()
        self.fileData_panel = VariablePanel()
        self.main_layout.insertWidget(1,self.plotPreview_panel)
        self.connectSignals_widgets()
        self.updateGUI()

    def connectSignals(self):
        self.fileSelection_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileSelection_listWidget.connect(self.fileSelection_listWidget,SIGNAL("customContextMenuRequested(QPoint)" ), self.listItemRightClicked)                
        self.loadSpectrum_pushButton.pressed.connect(self.press_loadButton_function)
        self.makeCalibration_pushButton.pressed.connect(self.press_makeCalibrationButton_function)
        self.loadCalibration_pushButton.pressed.connect(self.press_loadCalibrationButton_function)
        self.energy_radioButton.toggled.connect(self.loadCurrentItem)
        self.time_radioButton.toggled.connect(self.loadCurrentItem)
        self.transient_radioButton.toggled.connect(self.loadCurrentItem)
        self.dressingOn_radioButton.toggled.connect(self.loadCurrentItem)
        self.dressingOff_radioButton.toggled.connect(self.loadCurrentItem)
        self.folderBase_lineEdit.editingFinished.connect(self.updateBaseFolder)
        self.forderSelection_toolButton.pressed.connect(self.press_selectFolder_function)
        self.fileSelection_listWidget.itemDoubleClicked.connect(self.loadDatafromItem)
        self.normalizeSpectrum_checkbox.stateChanged.connect(self.loadCurrentItem)
        self.energyMax_lineEdit.editingFinished.connect(self.updateEnergyAxis)
        self.energyMin_lineEdit.editingFinished.connect(self.updateEnergyAxis)
        self.energySteps_lineEdit.editingFinished.connect(self.updateEnergyAxis)        
        self.showPhase_pushButton.pressed.connect(self.plotRabbitPhase)
        self.exportData_pushButton.pressed.connect(self.exportData)
    def connectSignals_widgets(self):
        self.calibration_toolbox.signal_requestInput.connect(self.plotPreview_panel.getData)
        self.calibration_toolbox.signal_applyCalibration.connect(self.updateCalibration)
        self.plotPreview_panel.signal_sendData.connect(self.calibration_toolbox.getData)        

    ################################################## Press button functions ##########################################    
    def press_selectFolder_function(self):       
        self.folderBase_lineEdit.setText(str(QFileDialog.getExistingDirectory(self, 'Choose directory')))

    def press_makeCalibrationButton_function(self):
        self.calibration_toolbox.show()

    def press_loadCalibrationButton_function(self):
        coeffs = FM(QFileDialog.getOpenFileName(self, 'Choose file',self.path_calib)[0]).readCalibration()
        if coeffs:
            self.updateCalibration(coeffs)

    ################################################## Update functions ##########################################    

    def updateCalibration(self,calibration):        
        print('Calibration has been updated')
        self.calibration = calibration
        self.alphaCalib_label.setText(f'{calibration[0]:.3e}')
        self.betaCalib_label.setText(f'{calibration[1]:.3e}')
        self.t0Calib_label.setText(f'{calibration[2]:.3e}')
        self.hasCalibration = True
        self.updateGUI()

    
    def updateBaseFolder(self):
        self.path_folder = self.folderBase_lineEdit.text()

    def updateGUI(self):
        if self.hasCalibration:
            self.energyMax_lineEdit.setEnabled(True)
            self.energyMin_lineEdit.setEnabled(True)
            self.energySteps_lineEdit.setEnabled(True)
        else:
            self.energyMax_lineEdit.setEnabled(False)
            self.energyMin_lineEdit.setEnabled(False)
            self.energySteps_lineEdit.setEnabled(False)
            self.time_radioButton.setChecked(True)
        if self.fileSelection_listWidget.count() == 0:
            self.isDataLoaded = False
        else:
            self.isDataLoaded = True
        if C.isStringElementEmpty([self.energyMin_lineEdit.text(),self.energyMax_lineEdit.text(),self.energySteps_lineEdit.text()]):
            self.energyAxisDefined = False
        else:
            self.energyAxisDefined = True

        if self.hasCalibration & self.energyAxisDefined:
            self.energy_radioButton.setEnabled(True)
        else:
            self.energy_radioButton.setEnabled(False)


    def updateEnergyAxis(self):    
        self.updateGUI()        
        if self.energyAxisDefined:
            self.energyStepsNumber_lineEdit.setText(str(
                af.getNumberOfSteps(
                    C.str2float(self.energyMin_lineEdit.text()),C.str2float(self.energyMax_lineEdit.text()),C.str2float(self.energySteps_lineEdit.text())
                    )))
            if self.energy_radioButton.isChecked():
                self.loadCurrentItem()
    def loadCurrentItem(self):
        self.updateGUI()        
        if self.isDataLoaded:
            self.loadDatafromItem(self.fileSelection_listWidget.item(self.returnCurrentRow()))
    def returnCurrentRow(self):
        currentRow = self.fileSelection_listWidget.currentRow()
        if currentRow == -1:
            currentRow = 0  
        return currentRow

    def getData_energySpace(self,axis1,signal):    
        # signal-=np.mean(signal[0])
        axis1,signal = Filter.ApplyFilter(axis1,signal,start = self.calibration[2]) # Remove unphysical counts
        axis1,signal = af.goFromTimeToEnergy(axis1,signal,self.calibration[0],self.calibration[1],self.calibration[2]) # Convert from time to energy
        axis1,signal = Filter.ApplyFilter(axis1,signal,start = float(self.energyMin_lineEdit.text()), end = float(self.energyMax_lineEdit.text())) # Select energy subset
        axis1,signal = af.linearizeData(axis1,signal,C.str2float(self.energyMin_lineEdit.text()),C.str2float(self.energyMax_lineEdit.text()),C.str2float(self.energySteps_lineEdit.text())) # Linearize energy space       
        return axis1,signal


    def getDataType(self):
        if self.transient_radioButton.isChecked():
            return 'signal_transient'
        elif self.dressingOn_radioButton.isChecked():
            return 'signal_statOn'
        elif self.dressingOff_radioButton.isChecked():
            return 'signal_statOff'
        else:
            return 'signal_transient'

    def exportData(self,):
        if self.isDataLoaded:
            filename_in = self.fileSelection_listWidget.item(self.returnCurrentRow()).text()
            filename = os.path.splitext(self.fileSelection_listWidget.item(self.returnCurrentRow()).text())[0]
            fileName = QFileDialog.getSaveFileName(self,'Export Data',filename+'_export.h5')[0]                
            signal,measure_axis,param_axis = self.loadData(filename_in,doDisplay=False)
            if bool(filename):
                data = dict()
                data['Parameters'] = dict(bin_axis=measure_axis,position=param_axis)
                data['Data'] = signal
                
                FM().storeDic(fileName,data)

        a = 0
    def loadData(self,filename,doDisplay=True):
        try:
            self.signal = FM(filename,'MBES').readFile()     
        except:
            pass
        try:
            self.signal = FM(filename,'TDC').readFile()     
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        self.isDataLoaded = True          
        signal,measure_axis,param_axis = self.preTreatData(self.signal)
        if doDisplay:
            self.showData(signal,measure_axis,param_axis)
        return signal,measure_axis,param_axis
    def preTreatData(self,data):
        if len(data) == 1:
            data = data[0]           
        signal = data['signal']
        measure_axis = data['t_vol']
        param_axis = data['delay']   
        for i,sig in enumerate(signal):
            if self.normalizeSpectrum_checkbox.isChecked():             
                signal[i] = sig/np.sum(data['signal']['signal_statOff'],axis=0)     
        if not self.time_radioButton.isChecked():
            for key in signal.keys():
                KE,signal[key] = self.getData_energySpace(measure_axis,signal[key])  
            measure_axis = KE
        if len(param_axis) < 2: # hack when there is only one point
            param_axis = np.append(param_axis,-param_axis)
            signal = np.append(signal,signal,axis = 1) 
            
        return signal,measure_axis,param_axis

    def showData(self,data,measure_axis,param_axis):  
        data = data[self.getDataType()] 
       
        self.plotPreview_panel.setData(axis_0=param_axis,axis_1=measure_axis, data=data)   

    ################################################## List widget functions ##########################################    

    def listItemRightClicked(self, QPos): 
        sender = self.sender()
        self.listMenu= QMenu(self)
        self.connect(self.listMenu.addAction("Remove Item(s)"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksRemoveItemClicked(who)) 
        self.connect(self.listMenu.addAction("Clear all"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksClearClicked(who)) 
        self.connect(self.listMenu.addAction("Extract data"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listExtractData(who)) 

        parentPosition = sender.mapToGlobal(QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def removeEntry(self,item,sender):
        # Remove entry in list
        sender.takeItem(sender.row(item))

    def removeSelectedItems(self,sender):
        # Remove all selected items
        [self.removeEntry(item,sender) for item in sender.selectedItems()]        

    def clearList(self,sender):    
        # Remove all items    
        [self.removeEntry(sender.item(row),sender) for row in np.flip(np.arange(sender.count()))]    

    # def removeSelectedItems(self,sender):
    #     # Remove all selected items
    #     [self.removeEntry(item,sender) for item in sender.selectedItems()]     
    ################################################## Context menu functions ##########################################    
    # def Qmenu_listExtractData(self,sender):        
    #     self.fileData_panel.show()

    def Qmenu_listPeaksRemoveItemClicked(self,sender):
        self.removeSelectedItems(sender)

    def Qmenu_listPeaksClearClicked(self,sender):
        self.clearList(sender)     
    ################################################## List functions ##########################################    

    def loadDatafromItem(self,item):
        if item:
            # load date from item
            self.loadData(item.text())
        else:
            print('No item available, check input')

    def press_loadButton_function(self):    
        self.path_filenames = QFileDialog.getOpenFileNames(self, 'Choose file',self.path_folder)[0]      
        path = self.path_filenames[0]                  
        self.path_folder = os.path.dirname(path)
        try:
            self.loadData(path)
            [self.addFileToList(filename= path) for path in self.path_filenames if path]
            self.fileSelection_listWidget.setCurrentRow(self.fileSelection_listWidget.count())      
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            print('Error loading file')

    def addFileToList(self,filename):
        self.fileSelection_listWidget.addItem(QListWidgetItem(filename))



    ################################################## RABBIT functions ##########################################    

    def plotRabbitPhase(self):
        if self.isDataLoaded:
            frequency_axis,y_axis = self.plotPreview_panel.outputPhaseViewerWidget.getAxis()
            oscillation_frequency = C.str2float(self.oscillationFrequency_lineEdit.text())
            oscillation_units = self.oscillationUnits_comboBox.currentIndex()
            if oscillation_units == 0:
                oscillation_frequency = C.wavelength2omega(oscillation_frequency)
            elif oscillation_units == 1:
                oscillation_frequency = C.energy2omega(oscillation_frequency)
            elif oscillation_units == 2:
                oscillation_frequency = 2*np.pi*(oscillation_frequency)
            elif oscillation_units == 3:                
                oscillation_frequency = oscillation_frequency

            data = self.plotPreview_panel.outputPhaseViewerWidget.getImageData()
            data = data[np.argmin(np.abs(frequency_axis - oscillation_frequency)),:]

            if self.unwrapPhase_checkBox.isChecked():
                data = np.unwrap(data)
            if self.customUnwrapPhase_checkBox.isChecked():
                data = wrap2pmpi(data)

            self.doPlot1D(y_axis,data,label=f'\u03C9={oscillation_frequency}PHz')

        else:
            print('No data has been loaded')            

    def doPlot1D(self,x,y,label='Plot'):
        if not hasattr(self,'V'):
            self.V = Viewer1DWidget()            
        self.V.addPlot(name=label,x=x,y=y,)
        self.V.show()

def wrap2pmpi(phasedata):
    """It wraps phase from -pi, pi"""
    return (phasedata + np.pi) % (2*np.pi) -np.pi
def main():
    import sys
    app = QApplication([])
    tof = MainPanel()
    tof.show()
    app.exec()

if __name__=="__main__":
    main()




    