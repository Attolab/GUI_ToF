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

from calibration_toolbox_ui import Ui_CalibrationToolbox
import pyqtgraph as pg
import numpy as np
import scipy.optimize as opt
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
        self.isNotUpdating = True         
        self.path_calib = 'Calibration/'

    def connectSignals(self):
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
        self.centraFrequency_doubleSpinBox.valueChanged.connect(self.updateListPeaksTable)
        self.showPeaks_ToF_checkBox.stateChanged.connect(self.showPeaksPlot)
        self.showPeaks_KE_checkBox.stateChanged.connect(self.showPeaksEnergy)

    def showPeaksPlot(self):
        for row in range(self.listPeaks_tableWidget.rowCount()):
            t=float(self.listPeaks_tableWidget.item(row,0).text())
            index = np.argmin(np.abs(t - np.array(self.plotRaw_plot.getDisplayDataset().x)))
            y=self.plotRaw_plot.getDisplayDataset().y[index]
            self.plotRaw_view.plot(x=[t], y=[y], symbol="o")
    
    def showPeaksEnergy(self):


        
        print("TODO")

    def setupPlotWidget(self):
        self.labelRaw = pg.LabelItem(justify = "right")
        self.plotRaw_window.addItem(self.labelRaw)
        self.plotRaw_view = self.plotRaw_window.addPlot(row=0,col =0,title="Raw Signal")
        self.plotRaw_view.setLabel('left', 'Signal', units='mV')
        self.plotRaw_view.setLabel('bottom', 'Time', units='ns')
        self.plotRaw_plot = self.plotRaw_view.plot()
        self.plotRaw_fit = self.plotRaw_view.plot()
        self.plotRaw_tablePlot = self.plotRaw_view.plot()
        self.proxyRaw = pg.SignalProxy(self.plotRaw_view.scene().sigMouseMoved, rateLimit=60, slot=self.mouseRawMoved)  
        self.labelCalib = pg.LabelItem(justify = "right")
        self.plotCalib_window.addItem(self.labelCalib)
        self.plotCalib_view = self.plotCalib_window.addPlot(row=0,col =0,title="Transformed Signal")
        self.plotCalib_view.setLabel('left', 'Signal', units='mV')
        self.plotCalib_view.setLabel('bottom', 'Energy', units='eV')        
        self.plotCalib_plot = self.plotCalib_view.plot()     
        self.plotCalib_fit = self.plotCalib_view.plot()
        self.plotCalib_tablePlot = self.plotCalib_view.plot()
        self.proxyCalib = pg.SignalProxy(self.plotCalib_view.scene().sigMouseMoved, rateLimit=60, slot=self.mouseCalibMoved)     
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)


    def mouseRawMoved(self,evt):
        mousePoint = self.plotRaw_view.vb.mapSceneToView(evt[0])
        self.labelRaw.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))


    def mouseCalibMoved(self,evt):
        mousePoint = self.plotCalib_view.vb.mapSceneToView(evt[0])
        self.labelCalib.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))

    def setupToolButton(self):
        tool_btn_menu= QMenu(self)
        self.connect(tool_btn_menu.addAction("Gaussian Fit"),SIGNAL("triggered()"), self.findPeaks_gaussianFit)
        self.connect(tool_btn_menu.addAction("Peak finder (scipy)"),SIGNAL("triggered()"), self.findPeaks_scipyPeakFinder) 
        self.connect(tool_btn_menu.addAction("Custom finder"),SIGNAL("triggered()"), self.findPeaks_custom)  
        self.findPeaks_toolButton.setMenu(tool_btn_menu)
        self.findPeaks_toolButton.setDefaultAction(tool_btn_menu.actions()[0])

        tool_btn_menu= QMenu(self)
        self.connect(tool_btn_menu.addAction("Load current signal"),SIGNAL("triggered()"), self.importSignal_menuFunction)
        self.connect(tool_btn_menu.addAction("Load FT magnitude"),SIGNAL("triggered()"), self.importModuleFT_menuFunction) 
        self.connect(tool_btn_menu.addAction("Load custom signal"),SIGNAL("triggered()"), self.importCustomSignal_menuFunction)  
        self.loadSignal_toolButton.setMenu(tool_btn_menu)
        self.loadSignal_toolButton.setDefaultAction(tool_btn_menu.actions()[1])

        tool_btn_menu= QMenu(self)
        self.connect(tool_btn_menu.addAction("Apply Calibration"),SIGNAL("triggered()"), self.applyCalibration_menuFunction)
        self.connect(tool_btn_menu.addAction("Plot Calibration"),SIGNAL("triggered()"), self.plotCalibration_menuFunction) 
        self.connect(tool_btn_menu.addAction("Save Calibration"),SIGNAL("triggered()"), self.saveCalibration_menuFunction)  
        self.connect(tool_btn_menu.addAction("Load Calibration"),SIGNAL("triggered()"), self.loadCalibration_menuFunction)          
        self.calibration_toolButton.setMenu(tool_btn_menu)
        self.calibration_toolButton.setDefaultAction(tool_btn_menu.actions()[0])        

    def findPeaks_gaussianFit(self):
        self.findPeaks()
    def findPeaks_scipyPeakFinder(self):
        self.findPeaks()
    def findPeaks_custom(self):
        self.findPeaks()

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
        [self.loadFile(filename) for filename in self.path_filenames]   

    def loadFile(self,fileName):
        coeffs = FM(fileName).readCalibration()
        self.addEntry(self.coeffCalib_tableWidget,coeffs)

    def importSignal_menuFunction(self):
        print('Action 1 activated.')
        self.signal_requestInput.emit('Signal')
    def importModuleFT_menuFunction(self):
        print('Action 2 activated.')
        self.signal_requestInput.emit('FT')
    def importCustomSignal_menuFunction(self):
        print('Action 3 activated.')    

    def findPeaks(self):
        param_lsq,number_of_peaks = PeakFitter.n_gaussian_fit(y=np.abs(self.y),x=self.x,prominence = 5e-2*np.max(self.y))
        amplitudes, peak_positions, peak_widths = PeakFitter.extract_gaussian_parameters(param_lsq, number_of_peaks)

        self.clearTable(self.listPeaks_tableWidget)
        [self.addEntry(sender= self.listPeaks_tableWidget, value = [peak,None]) for peak in peak_positions]

        # self.showPeaks()
    def getData(self,input):
        self.x = input[0]
        self.y = input[1]    
        self.plotRaw_plot.setData(x=self.x,y=self.y)

    def press_fitButton_function(self):
        if self.listPeaks_tableWidget.rowCount() > 3:
            self.updateFit()
        else:
            print('Need at least three entries in table')

    def updateFit(self):
        table_value = np.array([[self.listPeaks_tableWidget.item(row,0).data(0),self.listPeaks_tableWidget.item(row,1).data(0)] 
                                                            for row in range(self.listPeaks_tableWidget.rowCount())]).astype(float).T  
        self.p_opt, self.pcov = opt.curve_fit(af.ToF2eV, table_value[0], table_value[1], bounds = (0,np.inf),p0 = [1e8,50,50])
        self.addEntry(sender = self.coeffCalib_tableWidget,value=self.p_opt)     
        self.updateCalibration()
    def getCalibration(self):
        return [float(item.text()) for item in self.coeffCalib_tableWidget.selectedItems()]                

    def updateCalibration(self):
        alpha,beta,t0 = self.getCalibration()                
        self.x_fit = af.ToF2eV(self.x,alpha,beta,t0)
        jac = af.ToF2eV_Jac(self.x,alpha,t0)
        self.x2,self.y2 = af.goFromTimeToEnergy(self.x,self.y,alpha,beta,t0)
        mask = jac >=0
        self.x_fit = self.x_fit[mask]
        self.y_fit = self.y[mask] * jac[mask]
        self.plotCalib_plot.setData(x=self.x_fit,y=self.y_fit)
        

    def updateListPeaksTable(self,item):        
        if isinstance(item,int):
            # If a row is given, extract column value
            item = self.listPeaks_tableWidget.item(self.listPeaks_tableWidget.currentRow(),1)
        if np.logical_and(self.autoFillTable_checkBox.isChecked(), self.isNotUpdating):
            if item.column() == 1:            
                if item.text():        
                    self.isNotUpdating = False     
                    n_row = self.listPeaks_tableWidget.rowCount()    
                    energy = self.makeEnergyList(n_row,item.row(),float(item.text().replace(',', '.')))
                    [self.listPeaks_tableWidget.item(row,1).setData(0,energy[row]) for row in range(n_row)]
                    [self.listPeaks_tableWidget.item(row,1).setText(f'{energy[row]:.3f}') for row in range(n_row)]
                    self.isNotUpdating = True       

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
       
    def listItemRightClicked(self, QPos): 
        sender = self.sender()
        self.listMenu= QMenu(self)
        self.connect(self.listMenu.addAction("Add Item"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksAddItemClicked(who))
        self.connect(self.listMenu.addAction("Remove Item(s)"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksRemoveItemClicked(who)) 
        self.connect(self.listMenu.addAction("Clear all"),SIGNAL("triggered()"), lambda who=sender: self.Qmenu_listPeaksClearClicked(who)) 
        parentPosition = sender.mapToGlobal(QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()     
    def clearTable(self,sender):
        [sender.removeRow(0) for row in range(sender.rowCount())]

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




    