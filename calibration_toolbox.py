##############################################################################
##
# This file is part of pymepixviewer
#
# https://arxiv.org/abs/1905.07999
#
#
# pymepixviewer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pymepixviewer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pymepixviewer.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from re import T
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,QRegularExpression,
    QMetaObject, QObject, QPoint, QRect,Signal,SIGNAL,QFile,QDataStream,QFileInfo,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QRegularExpressionValidator,
    QFont, QFontDatabase, QGradient, QIcon,QTransform,QAction,QDoubleValidator,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QCloseEvent)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QPushButton,QFileDialog,
    QTableWidgetItem,QStyledItemDelegate,QLineEdit,
    QSizePolicy, QWidget,QMenu)
from calibration_parameters import Calibration_parameters

from calibration_toolbox_ui import Ui_CalibrationToolbox
import pyqtgraph as pg
import numpy as np
import scipy.optimize as opt
import scipy.signal as sgn
from usefulclass import PeakFinder, PeakFitter
from analysis_functions import AnalysisFunctions as af
from file_manager import FileManager as FM

class CalibrationToolBox(Ui_CalibrationToolbox,QWidget):
    signal_requestInput = Signal(str)
    signal_applyCalibration = Signal(object)

    # signal_updateFit = Signal(str)
    def __init__(self,parent=None):
        super(CalibrationToolBox, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.connectSignals()
        self.setupToolButton()
        self.setupPlotWidget()
        self.x = 1.
        self.y = 1.
        self.path_calib = 'Calibration/'
        self.parameter_list = dict([("inputAxis0Mult_lineEdit_2",0.05),("inputAxis0Mult_lineEdit",5),("inputAxis0Mult_lineEdit_3",0.5), ("inputAxis0Mult_lineEdit_4",1e8), ("inputAxis0Mult_lineEdit_5",0), ("inputAxis0Mult_lineEdit_6",0)])

        
    def connectSignals(self):
        #Set up widgets, buttons and checkboxes
        self.listPeaks_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listPeaks_tableWidget.connect(self.listPeaks_tableWidget,SIGNAL("customContextMenuRequested(QPoint)" ), self.listItemRightClicked)    
        self.coeffCalib_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.coeffCalib_tableWidget.connect(self.coeffCalib_tableWidget,SIGNAL("customContextMenuRequested(QPoint)" ), self.listItemRightClicked)    
        delegate = NumericDelegate(self.coeffCalib_tableWidget)
        self.coeffCalib_tableWidget.setItemDelegate(delegate)  
        delegate = NumericDelegate(self.listPeaks_tableWidget)
        self.listPeaks_tableWidget.setItemDelegate(delegate)  
        self.fitPeaks_pushButton.pressed.connect(self.press_fitButton_function)
        self.listPeaks_tableWidget.itemChanged.connect(self.updateListPeaksTable)
        self.considerSBs_checkBox.stateChanged.connect(self.updateListPeaksTable)
        # self.centraFrequency_doubleSpinBox.valueChanged.connect(self.updateListPeaksTable)
        self.showPeaks_ToF_checkBox.stateChanged.connect(self.showPeaksPlot)
        self.showPeaks_KE_checkBox.stateChanged.connect(self.showPeaksEnergy)
        self.parametersButton.clicked.connect(self.openParameters)

    def setupPlotWidget(self):
        #Creation of items in windows, tables and plots, data is set using setData later
        self.labelRaw = pg.LabelItem(justify = "right")
        self.plotRaw_window.addItem(self.labelRaw)
        self.plotRaw_view = self.plotRaw_window.addPlot(row=0,col =0,title="Raw Signal")
        self.plotRaw_view.setLabel('left', 'Signal', units='mV')
        self.plotRaw_view.setLabel('bottom', 'Time', units='ns')
        self.plotRaw_plot = self.plotRaw_view.plot()
        self.plotRaw_peaks = self.plotRaw_view.plot()
        self.plotRaw_tablePlot = self.plotRaw_view.plot()
        self.proxyRaw = pg.SignalProxy(self.plotRaw_view.scene().sigMouseMoved, rateLimit=60, slot=self.mouseRawMoved)  
        self.labelCalib = pg.LabelItem(justify = "right")
        self.plotCalib_window.addItem(self.labelCalib)
        self.plotCalib_view = self.plotCalib_window.addPlot(row=0,col =0,title="Transformed Signal")
        self.plotCalib_view.setLabel('left', 'Signal', units='mV')
        self.plotCalib_view.setLabel('bottom', 'Energy', units='eV')        
        self.plotCalib_plot = self.plotCalib_view.plot()     
        self.plotCalib_peaks = self.plotCalib_view.plot()
        self.plotCalib_tablePlot = self.plotCalib_view.plot()
        self.proxyCalib = pg.SignalProxy(self.plotCalib_view.scene().sigMouseMoved, rateLimit=60, slot=self.mouseCalibMoved)     
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
    
    def setupToolButton(self):
        #Set up buttons with multiple choices
        tool_btn_menu= QMenu(self)
        #Different peak finder methods
        self.connect(tool_btn_menu.addAction("Peak finder (scipy)"),SIGNAL("triggered()"), self.findPeaks_scipyPeakFinder) 
        self.connect(tool_btn_menu.addAction("Gaussian Fit"),SIGNAL("triggered()"), self.findPeaks_gaussianFit)
        self.connect(tool_btn_menu.addAction("Custom finder"),SIGNAL("triggered()"), self.findPeaks_custom)  
        self.findPeaks_toolButton.setMenu(tool_btn_menu)
        self.findPeaks_toolButton.setDefaultAction(tool_btn_menu.actions()[0])

        tool_btn_menu= QMenu(self)
        #Different signal loading methods
        self.connect(tool_btn_menu.addAction("Load current signal"),SIGNAL("triggered()"), self.importSignal_menuFunction)
        self.connect(tool_btn_menu.addAction("Load FT magnitude"),SIGNAL("triggered()"), self.importModuleFT_menuFunction) 
        self.connect(tool_btn_menu.addAction("Load custom signal"),SIGNAL("triggered()"), self.importCustomSignal_menuFunction)  
        self.loadSignal_toolButton.setMenu(tool_btn_menu)
        self.loadSignal_toolButton.setDefaultAction(tool_btn_menu.actions()[0])

        tool_btn_menu= QMenu(self)
        #Different calibration choices
        self.connect(tool_btn_menu.addAction("Apply Calibration"),SIGNAL("triggered()"), self.applyCalibration_menuFunction)
        self.connect(tool_btn_menu.addAction("Plot Calibration"),SIGNAL("triggered()"), self.plotCalibration_menuFunction) 
        self.connect(tool_btn_menu.addAction("Save Calibration"),SIGNAL("triggered()"), self.saveCalibration_menuFunction)  
        self.connect(tool_btn_menu.addAction("Load Calibration"),SIGNAL("triggered()"), self.loadCalibration_menuFunction)          
        self.calibration_toolButton.setMenu(tool_btn_menu)
        self.calibration_toolButton.setDefaultAction(tool_btn_menu.actions()[0])        
    
############################################ Mouse interaction ###############################################################

    def mouseRawMoved(self,evt):
        mousePoint = self.plotRaw_view.vb.mapSceneToView(evt[0])
        self.labelRaw.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))

    def mouseCalibMoved(self,evt):
        mousePoint = self.plotCalib_view.vb.mapSceneToView(evt[0])
        self.labelCalib.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))

    def listItemRightClicked(self, QPos): 
        sender = self.sender()
        self.listMenu= QMenu(self)
        self.connect(self.listMenu.addAction("Add Item"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksAddItemClicked(who))
        self.connect(self.listMenu.addAction("Remove Item(s)"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksRemoveItemClicked(who)) 
        self.connect(self.listMenu.addAction("Clear all"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksClearClicked(who)) 
        parentPosition = sender.mapToGlobal(QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()     

################################################## Peak finder methods ##########################################################

    def findPeaks_gaussianFit(self):
        #Use of the Peak Fitter class in usefulclass.py to compute gaussian fits around the peaks 
        prominence_factor = self.parameter_list["inputAxis0Mult_lineEdit_2"]
        distance = self.parameter_list["inputAxis0Mult_lineEdit"]
        rel_height = self.parameter_list["inputAxis0Mult_lineEdit_3"]
        param_lsq,number_of_peaks = PeakFitter.n_gaussian_fit(y=np.abs(self.y),x=self.x,prominence = prominence_factor*np.max(self.y), distance=distance, rel_height=rel_height)
        amplitudes, peak_positions, peak_widths = PeakFitter.extract_gaussian_parameters(param_lsq, number_of_peaks)
        self.clearTable(self.listPeaks_tableWidget)
        [self.addEntry(sender= self.listPeaks_tableWidget, value = [peak,None]) for peak in peak_positions]
        self.updatePeakPosition()

    def findPeaks_scipyPeakFinder(self):
        #Simple use of the scipy find_peaks method
        prominence_factor = float(self.parameter_list["inputAxis0Mult_lineEdit_2"])
        distance = float(self.parameter_list["inputAxis0Mult_lineEdit"])
        rel_height = float(self.parameter_list["inputAxis0Mult_lineEdit_3"])

        peaks_index,properties = sgn.find_peaks(x=np.abs(self.y), prominence = prominence_factor*np.max(self.y), distance = distance, rel_height=rel_height)

        self.clearTable(self.listPeaks_tableWidget)
        [self.addEntry(sender= self.listPeaks_tableWidget, value = [self.x[index],None]) for index in peaks_index]
        self.updatePeakPosition()
    
    def findPeaks_custom(self):
        #not implemented yet, tbd in the future
        self.findPeaks_gaussianFit()


################################### Calibration file loading and saving ####################################################

    def applyCalibration_menuFunction(self):
        self.updateCalibration()
        self.signal_applyCalibration.emit(self.getCalibration())

    def plotCalibration_menuFunction(self):
        print('Pressed plot calibration')

    def saveCalibration_menuFunction(self):
        fileName = QFileDialog.getSaveFileName(self,'Calibration',self.path_calib)[0]
        self.path_calib = QFileInfo(fileName).path()
        FM(fileName).writeCalibration(self.coeffCalib_tableWidget.selectedItems())

    def loadCalibration_menuFunction(self):
        self.path_filenames = QFileDialog.getOpenFileNames(self, 'Choose file',self.path_calib)[0]        
        self.path_calib = QFileInfo(fileName).path() 
        [self.loadFile(filename) for filename in self.path_filenames]   

    def loadFile(self,fileName):
        coeffs = FM(fileName).readCalibration()
        self.path_calib = QFileInfo(fileName).path()
        self.addEntry(self.coeffCalib_tableWidget,coeffs)

    def importSignal_menuFunction(self):
        print('Action 1 activated.')
        self.signal_requestInput.emit('Signal')
    def importModuleFT_menuFunction(self):
        print('Action 2 activated.')
        self.signal_requestInput.emit('FT')
    def importCustomSignal_menuFunction(self):
        import csv
        #open folder to choose file according to type
        if hasattr(self,'path_folder'):
            self.path_filenames = QFileDialog.getOpenFileNames(self, 'Choose file',self.path_folder)[0]
        else:
            self.path_filenames = QFileDialog.getOpenFileNames(self, 'Choose file')[0]


        self.path = self.path_filenames[0]
        # if self.path[-3:]=="npy":
        #     output = [tof,np.load(self.path)]
        # elif self.path[-3:]=="csv":
        with open(self.path) as file_name:
            file_read = csv.reader(file_name)
            array = list(file_read)
            array = array[1:]
            x = [float(array[i][0]) for i in range(len(array))]
            y = [float(array[i][1]) for i in range(len(array))]
            output = [np.array(x),np.array(y)] 
        self.getData(output)
        # self.signal_requestInput.emit("custom")
        print('Action 3 activated.')    

    
    ########################################## Calibration methods ######################################################

    def getData(self,input):
        #Data setting in the raw plot
        self.x = input[0]
        self.y = input[1]-input[1][0] #corrects initial offset for calibration
        self.plotRaw_plot.setData(x=self.x,y=self.y)

    def press_fitButton_function(self):
        #Fit Peaks function
        if self.listPeaks_tableWidget.rowCount() > 3:
            self.updateFit()
        else:
            print('Need at least three entries in table')

    def updateFit(self):

        #Fetching the time and energy values in the table widget
        table_value = np.array([[self.listPeaks_tableWidget.item(row,0).data(0),self.listPeaks_tableWidget.item(row,1).data(0)] 
                                                            for row in range(self.listPeaks_tableWidget.rowCount())]).astype(float).T 

        #Using the scipy curve_fit calibration function 
        self.p_opt, self.pcov = opt.curve_fit(af.ToF2eV, table_value[0], table_value[1], bounds = (-np.inf,np.inf), p0 = (self.parameter_list["inputAxis0Mult_lineEdit_4"],self.parameter_list["inputAxis0Mult_lineEdit_5"],self.parameter_list["inputAxis0Mult_lineEdit_6"]))

        #Computation of R²
        Ecal=[af.ToF2eV(t,self.p_opt[0],self.p_opt[1],self.p_opt[2]) for t in table_value[0]]

        residuals = [table_value[1][i] - Ecal[i] for i in range(len(table_value[0]))]

        ss_res = np.sum([residuals[i]**2 for i in range(len(residuals))])
        ss_tot = np.sum((table_value[1]-np.mean(table_value[1]))**2)
        r_squared = 1 - (ss_res / ss_tot)

        #Update of the parameters table widget
        self.addEntry(sender = self.coeffCalib_tableWidget,value=(self.p_opt[0],self.p_opt[1],self.p_opt[2],r_squared))
        
        self.updateCalibration()

       #This was once used to calibrate time on energy raher than energy on time, searching for a correspondance bewteen a time vector
       #and an energy vector, since there is no inverse function to the one that links energy to time with no approximation.

        # table_value = np.array([[self.listPeaks_tableWidget.item(row,0).data(0),self.listPeaks_tableWidget.item(row,1).data(0)] 
        #                                                     for row in range(self.listPeaks_tableWidget.rowCount())]).astype(float).T
        #self.p_opt, self.pcov = opt.curve_fit(CalibrationToolBox.neweV2ToF, table_value[1], table_value[0], bounds = (1e15,np.inf))
        #print(self.p_opt[0]) 

        #l_list = [i*1e15 for i in range(1,1000)]
        #l_min = 1e15
        #tcal_min=[CalibrationToolBox.neweV2ToF(E,l_min) for E in table_value[1]]
        #residuals_min = [table_value[0][i] - tcal_min[i] for i in range(len(table_value[1]))]
        #ss_res_min = np.sum([residuals_min[i]**2 for i in range(len(residuals_min))])
        #ss_tot_min = np.sum((table_value[0]-np.mean(table_value[0]))**2)
        #r_squared_min = 1 - (ss_res_min / ss_tot_min)
        #for l in l_list:
            #tcal=[CalibrationToolBox.neweV2ToF(E,l) for E in table_value[1]]
            #residuals = [table_value[0][i] - tcal[i] for i in range(len(table_value[1]))]
            #ss_res = np.sum([residuals[i]**2 for i in range(len(residuals))])
            #ss_tot = np.sum((table_value[0]-np.mean(table_value[0]))**2)
            #r_squared = 1 - (ss_res / ss_tot)
            #print(r_squared)
            #if r_squared>r_squared_min:
                #l_min=l
        #print(l_min)

        #self.updateCalibrationPotential(l_min)


    def getCalibration(self):
        #Returns the calibration parameters
        return [float(item.text()) for item in self.coeffCalib_tableWidget.selectedItems()]                

    def updateCalibration(self):
        #Computation of the calibrated plot
        alpha,beta,t0,r_squared = self.getCalibration()                
        self.x_fit = af.ToF2eV(self.x,alpha,beta,t0)
        jac = af.ToF2eV_Jac(self.x,alpha,t0)
        #Truncation of the plot (jacobian and limitation to low energies)
        mask = jac >=0
        self.x_fit = self.x_fit[mask]
        self.y_fit = self.y[mask] / jac[mask]
        mask = self.x_fit < 150
        self.x_fit = self.x_fit[mask]
        self.y_fit = self.y_fit[mask]
        #Plotting with certain limits
        self.plotCalib_plot.setData(x=self.x_fit,y=self.y_fit)

    #The following two functions are used exclusively for the forementioned calibration, which in the end failed.
    
    def updateCalibrationPotential(self,l):
    
        alpha = 18013482.633733194
        beta = -8.281556118297484
        t0 = 63.75584484048288
        V = -20

        #Create E axis to check which energies to keep
        E_list = [i*0.05 for i in range(1,3000)]
        self.x_fit = np.array([])
        self.y_fit = np.array([])
        index = 1

        #for each time, check which energy corresponds to it with brute force
        for j in range(len(self.x)):
    
            t = self.x[j]

            for i in range(1,len(E_list)):

                t_cal = af.eV2ToF_potential(E_list[i],alpha,beta,t0,V,l)

                #check if the previous energy corresponds better, add it to the list
                if t_cal<t:

                    t_bis = af.eV2ToF_potential(E_list[i],alpha,beta,t0,V,l)

                    if abs(t_cal-t)>abs(t_bis-t):
                        self.x_fit=np.append(self.x_fit,E_list[i-1])
                        index=i-1
                    else:
                        self.x_fit=np.append(self.x_fit,E_list[i])
                        index=i
                    
                    #time is an inverse function of energy, to each time corresponds one energy only
                    self.y_fit=np.append(self.y_fit,self.y[j])
                    print("index="+str(index))
                    break
        
        #(f-1)'=1/(f'°f-1)
        jac = 1/af.eV2ToF_Jac_potential(self.x_fit,alpha,beta,V,l)

        #Truncation of the plot (jacobian and limitation to low energies)
        mask = jac >=0
        self.x_fit = self.x_fit[mask]
        self.y_fit = self.y_fit[mask] * jac[mask]
        mask = self.x_fit < 150
        self.x_fit = self.x_fit[mask]
        self.y_fit = self.y_fit[mask]

        #Plotting with certain limits
        self.plotCalib_plot.setData(x=self.x_fit,y=self.y_fit)
    
    def neweV2ToF(E,l):
        t0 = 63.75584484048288
        alpha = 18013482.633733194
        beta = -8.281556118297484
        V = -20
        L = np.sqrt(2*alpha/9.1e-31)
        return t0 + np.sqrt(9.1e-31/2)*(l/np.sqrt(E-beta) + (L-l)/np.sqrt(E-beta+V))


###################################### Show Peaks Widget #############################################################
    def makePeaks(self,plot_data):
        #checks if the checkbox is checked or not
            nRow = self.listPeaks_tableWidget.rowCount()
            x = np.zeros(nRow)
            y = np.zeros(nRow)
            x_data,y_data = plot_data.getData()
            for row in range(nRow):     
                #retrieve list of peak times
                x[row] = float(self.listPeaks_tableWidget.item(row,0).text())        
                #retrieve list of signal amplitude at x       
                y[row] = y_data[np.argmin(np.abs(x[row] - x_data))] 
            return x,y
    def showPeaksPlot(self):
        #checks if the checkbox is checked or not
        if self.showPeaks_ToF_checkBox.isChecked():
            t_peaks,y_peaks = self.makePeaks(self.plotRaw_plot)
            self.plotRaw_peaks.setData(x=t_peaks, y=y_peaks, symbol="o")
            self.plotRaw_peaks.setVisible(True)
        else:
            self.plotRaw_peaks.setVisible(False)

    def showPeaksEnergy(self):
         #checks if the checkbox is checked or not
        boolean = self.showPeaks_KE_checkBox.isChecked()
        
        t_list=[]
        y=[]

        for row in range(self.listPeaks_tableWidget.rowCount()):
            t_list.append(float(self.listPeaks_tableWidget.item(row,0).text()))
        
        #transformation of time of flight into energy
        alpha,beta,t0,r_squared = self.getCalibration()
        E_list=[af.ToF2eV(t,alpha,beta,t0) for t in t_list]

        for E in E_list:
            index = np.argmin(np.abs(E - np.array(self.plotCalib_plot.getDisplayDataset().x)))
            y.append(self.plotCalib_plot.getDisplayDataset().y[index])

        self.plotCalib_peaks.setData(x=E_list, y=y, symbol="o")
        self.plotCalib_peaks.setVisible(boolean)


##################################### Table Widget specific methods #############################################################

    def updateListPeaksTable(self,item):  
        item.setText(item.text().replace(',', '.'))
        if isinstance(item,int):
            # If a row is given, extract column value
            item = self.listPeaks_tableWidget.item(self.listPeaks_tableWidget.currentRow(),1)
        if self.autoFillTable_checkBox.isChecked():
            if item.column() == 1:            
                if item.text():        
                    self.listPeaks_tableWidget.itemChanged.disconnect(self.updateListPeaksTable)
                    n_row = self.listPeaks_tableWidget.rowCount()    
                    energy = self.makeEnergyList(n_row,item.row(),float(item.text().replace(',', '.')))
                    [self.listPeaks_tableWidget.item(row,1).setData(0,energy[row]) for row in range(n_row)]
                    [self.listPeaks_tableWidget.item(row,1).setText(f'{energy[row]:.3f}') for row in range(n_row)]
                    # self.isNotUpdating = True       
                    self.listPeaks_tableWidget.itemChanged.connect(self.updateListPeaksTable)


    def makeEnergyList(self,n_index,starting_index,starting_value):
        # Make an energy array from a starting index
        energy_spacing = 2**(not(self.considerSBs_checkBox.isChecked()))*af.nm2eV(self.centraFrequency_doubleSpinBox.value())
        return starting_value + energy_spacing*(starting_index-np.arange(n_index))

    def makeTableItem(self,value):
        # Make a table item
        item = QTableWidgetItem()
        if value:
            item.setData(0,value)
            item.setText(str(value))
        return item

    def addEntry(self, sender, value = []):
        # Add a new entry to table
        col_iterator= range(sender.columnCount())
        if not len(value):
            value = [None for col in col_iterator]
        sender.insertRow(sender.rowCount())        
        [sender.setItem(sender.rowCount()-1,col,self.makeTableItem(value[col])) for col in col_iterator]
        sender.selectRow(sender.rowCount()-1)

    def removeEntry(self,row,sender):
        # Remove entry to listPeaks_tableWidget
        sender.removeRow(row) 

    def removeSelectedItems(self,sender):
        # row_index = [index.row() for index in sender.selectedIndexes() if index.column()==0].sort(reverse = True)
        row_index = np.flip(np.sort([index.row() for index in sender.selectedIndexes() if index.column()==0]))
        [self.removeEntry(row,sender) for row in row_index]
       

    def clearTable(self,sender):
        [sender.removeRow(0) for row in range(sender.rowCount())]

    ################################################# Calibration Parameters Widget ###########################################

    def openParameters(self):
        self.update_Parameters()
        self._calibration_parameters.show()

    def update_Parameters(self):
        #if there is already a window open
        if (hasattr(self,'_calibration_parameters')):
            self.parameter_list = dict(self._calibration_parameters.widget_extraction.extractValues())
        #if there is no window open, open one
        else:
            self._calibration_parameters = Calibration_parameters(item_list = self.parameter_list)
            self._calibration_parameters.emitParameters.connect(self.updateSettings)
        
    def updateSettings(self):
        self.update_Parameters()
        self._calibration_parameters.widget_extraction.initializeValues(self.parameter_list)
        self.updatePeakPosition()
        #automatically find peaks with new parameters
        #self.findPeaks_scipyPeakFinder()
    
    def updatePeakPosition(self):
        self.showPeaksPlot()
        # self.showPeaksEnergy()


    ################################################## Context menu functions ##########################################  
  
    def Qmenu_listPeaksRemoveItemClicked(self,sender):
        self.removeSelectedItems(sender)

    def Qmenu_listPeaksAddItemClicked(self,sender):
        self.addEntry(sender)

    def Qmenu_listPeaksClearClicked(self,sender):
        self.clearTable(sender)

        
## DELEGATE TO ONLY ACCEPT DOUBLE INPUT##
class NumericDelegate(QStyledItemDelegate):    
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            validator = QDoubleValidator(editor)        
            editor.setValidator(validator)
        return editor



def main():
    app = QApplication([])
    calib = CalibrationToolBox()
    calib.show()
    app.exec()

if __name__=="__main__":
    main()




    