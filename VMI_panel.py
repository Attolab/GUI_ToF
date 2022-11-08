from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QRectF,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QCloseEvent,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QPen)
from PySide6.QtWidgets import (QApplication, QGraphicsEllipseItem,QGraphicsLineItem, QPushButton, QSizePolicy, QToolButton,QMessageBox,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow)
from VMI_panel_ui import Ui_VMI_panel
import pyqtgraph as pg
from skimage.transform import rotate
import pyqtgraph  as pg  
from pyqtgraph import dockarea
import sys, traceback, time
from file_manager import FileManager as FM
import h5py
import numpy as np
import pathlib
from abel.tools import polar
from ParameterTree import VMIParameter
import re
import json
import os,time
from collections import OrderedDict
from abel_davis_class import Abel_object
class VMIPanel(Ui_VMI_panel,QWidget):
    signal_VMI_panel_creation = Signal(object)
    signal_VMI_panel_destruction = Signal(object)
    updateCenter_signal = Signal(float,float)
    def __init__(self, parent=None, index=0, path=None):
        super(VMIPanel, self).__init__(parent)
        #Load UI
        self.setupUi(self)
        self.central_widget = dockarea.DockArea()

        #Initialize parameters
        self.panel_index = index
        self.path = path
        self.centerX = 0
        self.centerY = 0
        self.rot_angle = 0
        self.dR = 1
        self.dTheta = np.pi/180
        self.nImages = 0
        #Initialize some widgets
        self.initialize_plotWidgets()
        #Connect signals
        # self.connectVMISignal()
        self.connectSignal()
        self.viewerGroupParameter = VMIParameter(name="VMI_settings",title="VMI settings", tip='',
                     children=[],expanded = True)
        

        if os.path.exists("VMIPanel_parameters.txt"):
            with open("VMIPanel_parameters.txt",'r') as f:
                try:
                    self.viewerGroupParameter.restoreState(eval(f.read()))
                except:
                    print('Previous settings could not be loaded')            
        else:
            self.initializeDefaultWidgets()

        self.viewerGroupParameter.valueChanging_signal.connect(self.updateGUI)

        self.settings_parameterTree.setParameters(self.viewerGroupParameter)     

        self.imageViewer.view_2D.addItem(self.x_line_plot)
        self.imageViewer.view_2D.addItem(self.y_line_plot)
        self.imageViewer.view_2D.addItem(self.RminDisk_plot)
        self.imageViewer.view_2D.addItem(self.RmaxDisk_plot)        
        self.imageViewer.view_2D.addItem(self.center_plot)
       
        self.updateImageViewer()


    ## SAVING PARAMETER STATE ###
    def closeEvent(self, event: QCloseEvent) -> None:
        with open("VMIPanel_parameters.txt",'w') as f:
            f.write(repr(self.viewerGroupParameter.saveState()))
        return super().closeEvent(event)




    def updateImageViewer(self): 
        ## Store values to make syntax simpler later on       
        self.centerX = self.viewerGroupParameter.child('image_parameters').child('centerX').value()
        self.centerY = self.viewerGroupParameter.child('image_parameters').child('centerY').value()
        self.rot_angle = self.viewerGroupParameter.child('image_parameters').child('theta').value()     
        self.cropX = self.viewerGroupParameter.child('image_parameters').child('cropX').value()
        self.cropY = self.viewerGroupParameter.child('image_parameters').child('cropY').value()
        self.isTransposed = self.viewerGroupParameter.child('image_parameters').child('transpose').value()
        self.Rmax = self.viewerGroupParameter.child('image_parameters').child('Rmax').value()
        self.showAxis = self.viewerGroupParameter.child('display_parameters').child('axis').child('show_plot').value()
        self.showRange = self.viewerGroupParameter.child('display_parameters').child('range').child('show_plot').value()
        self.showRange = self.viewerGroupParameter.child('display_parameters').child('center').child('show_plot').value()
        self.updateWidgets()
        if self.path:
            self.data = self.getData()          
            self.updateImagePlot(self.transformData(self.data))
    def updateGUI(self,param,values):
        for value in values:
            path = param.childPath(value[0])
            if path[0] == param.childs[0].name(): #Image parameters
                self.updateImageViewer()
            elif path[0] == param.childs[1].name(): #Display parameters
                if path[1] == 'axis':
                    if path[-1] == 'show_plot':
                        if value[-1]:
                            self.x_line_plot.show()
                            self.y_line_plot.show()
                        else:
                            self.x_line_plot.hide()
                            self.y_line_plot.hide()                            
                    elif path[-1] == 'pen_param':
                        self.x_line_plot.setPen(value[-1])
                        self.y_line_plot.setPen(value[-1])
                elif path[1] == 'range':
                    if path[-1] == 'show_plot':
                        if value[-1]:
                            self.RminDisk_plot.show()
                            self.RmaxDisk_plot.show()
                        else:
                            self.RminDisk_plot.hide()
                            self.RmaxDisk_plot.hide()                            
                    elif path[-1] == 'pen_param':
                        self.RminDisk_plot.setPen(value[-1])
                        self.RmaxDisk_plot.setPen(value[-1])
                elif path[1] == 'center':
                    if path[-1] == 'show_plot':
                        if value[-1]:
                            self.center_plot.show()
                        else:
                            self.center_plot.hide()
                    elif path[-1] == 'pen_param':
                        self.center_plot.setPen(value[-1])

    def updateImagePlot(self,data):     
        if data is not None:
            self.imageViewer.updateViewerWidget(data)
    def updateWidgets(self):
        self.updateAxis()
        self.RmaxDisk_plot.setRect(self.centerX-self.Rmax, self.centerY-self.Rmax, 2*self.Rmax, 2*self.Rmax)
        self.center_plot.setRect(self.centerX-self.center_plotradius, self.centerY-self.center_plotradius, 2*self.center_plotradius, 2*self.center_plotradius)                
    def updateAxis(self):
        line_x = np.array([-1024,0,1024,0])
        line_y = np.array([0,-1024,0,1024])
        line_x[0::2] = line_x[0::2] + self.centerX
        line_y[0::2] = line_y[0::2] + self.centerX
        line_x[1::2] = line_x[1::2] + self.centerY
        line_y[1::2] = line_y[1::2] + self.centerY
        self.x_line_plot.setLine(*line_x)
        self.y_line_plot.setLine(*line_y)


    def connectSignal(self):
        self.image_tableWidget.itemSelectionChanged.connect(self.changeItemSelection)
        self.loadFile_button.pressed.connect(self.loadFilefromButton)
        self.folderBase_lineEdit.editingFinished.connect(self.updateBaseFolder)
        self.folderSelection_toolButton.pressed.connect(self.press_selectFolder_function)
        self.VMI_toolBox.sendParameters_signal.connect(self.computeData)
        self.VMI_toolBox.abelInversion_pushButton.pressed.connect(self.computeAbel)
    

    def computeAbel(self,):
        parameters = self.VMI_toolBox.getParameters()        
        abel_obj = Abel_object(self.transformData(self.data), self.centerY, self.centerX, 0.1, 1, parameters['abelLegendre_spinBox'], parameters['Rmax_doubleSpinBox'])    
        abel_obj.precalculate()
        abel_obj.invert()
        abel_obj.reconstruct()


    def computeData(self,parameters):
        print(parameters)
        self.parameterList_VMI_toolbox = parameters
        # Separation by a semi-column will relaunch the loop
        tokens_compute = re.findall('[^;]+',self.parameterList_VMI_toolbox['dataSelection_lineEdit'])
        for token_c in tokens_compute:
            tokens_stack = re.findall('[^,]+',token_c)
            output = []
            # Loop through inputs separated by comma
            for token_s in tokens_stack:
                tokens_stack2 = re.findall('[^:]+',token_s)
                L = len(tokens_stack2)
                if L == 1:
                    if tokens_stack2[0] == 'x':
                        output_temp = np.arange(0,self.nImages)
                    else:
                        output_temp = int(tokens_stack2[0])
                elif L == 2:
                    l_t = int(tokens_stack2[0])
                    if l_t < 0:
                        l_t = 0                        
                    u_t = int(tokens_stack2[1])+1
                    if u_t > self.nImages:
                        u_t = self.nImages
                    output_temp = np.arange(l_t,u_t)
                elif L == 3:
                    l_t = int(tokens_stack2[0])
                    if l_t < 0:
                        l_t = 0                        
                    u_t = int(tokens_stack2[1])+1
                    if u_t > self.nImages:
                        u_t = self.nImages
                    s_t = int(tokens_stack2[2])
                    output_temp = np.arange(l_t,u_t,s_t)
                else:
                    print('Input not recognized')
                    output_temp = []
                output.append(output_temp)
            if len(output)> 1:
                output = np.concatenate(output)
                output = np.sort(output)
            for index in output:
                if hasattr(self,'fileManager'):
                    data = np.squeeze(self.fileManager.readVMIData_h5(index))   
                    self.calculate_polar(data)
                    self.im_polar,self.rgrid,self.thetagrid = polar.reproject_image_into_polar(data = self.im,origin = (self.centerY,self.centerX),Jacobian=True,dr=self.dR,dt=self.dTheta)
                    self.radial_bins = self.rgrid[:,0]
                    self.angular_bins = self.thetagrid[0,:]*180/np.pi            
                else:
                    print('No file has been loaded')

    def press_selectFolder_function(self):       
        self.folderBase_lineEdit.setText(str(QFileDialog.getExistingDirectory(self, 'Choose directory')))
    def updateBaseFolder(self):
        self.path_folder = self.folderBase_lineEdit.text()
    def changeItemSelection(self,):    
        self.loadImagefromIndex(self.image_tableWidget.currentRow())
    


#################################### DATA LOADING AND MANIPULATION ###################################
    def getData(self,index = 0):
        if self.path:
            data = self.loadData(index)
            return data            
            

    def loadData(self,index):
        return np.squeeze(self.fileManager.readVMIData_h5(index))  
    
    def transformData(self,data):
        if self.isTransposed:
            data = data.T        
        # Crop
        cropX = np.arange(np.abs(self.cropX))
        cropY = np.arange(np.abs(self.cropY))
        if self.cropX < 0:
            cropX = -np.fliplr(cropX)
        if self.cropY < 0:
            cropY = -np.fliplr(cropY)            
        data[:,cropX] = 0
        data[cropY,:] = 0
        # Rotate
        data = rotate(data,-self.rot_angle, resize=False,center= [self.centerY,self.centerX])                                        
        return data

    def loadImagefromIndex(self,index):  
        self.data = self.getData(index) 
        self.updateImagePlot(self.transformData(self.data))

    def loadFilefromButton(self):
        if hasattr(self,'path_folder'):
            self.path = str(QFileDialog.getOpenFileName(self, 'Import image',self.path_folder)[0])    
        else:
            import os
            self.path = str(QFileDialog.getOpenFileName(self, 'Import image',)[0])
            self.path_folder = os.path.dirname(self.path)
            self.folderBase_lineEdit.setText(self.path_folder)
        self.loadFile()

    def loadFile(self,):
        if self.path:
            self.fileManager = FM(self.path)
            positions = self.fileManager.ExtractMetaData_h5()
            indexes = np.arange(len(positions))            
            # Disconnect signal
            self.image_tableWidget.itemSelectionChanged.disconnect()
            # Remove previous rows
            [self.image_tableWidget.removeRow(row) for row in np.flip(np.arange(self.image_tableWidget.rowCount()))]
            # Add new entries
            [self.image_tableWidget.addEntry(str(index),str(position))for index,position in zip(indexes,positions)]
            self.image_tableWidget.itemSelectionChanged.connect(self.changeItemSelection)
            self.image_tableWidget.setCurrentItem(self.image_tableWidget.selectRow(0))
            filename = self.path
            self.nImages= len(positions)

#################################### PLOT WIDGET ###################################

    def initialize_plotWidgets(self):
        self.center_plot = QGraphicsEllipseItem()  
        self.center_plotradius = 10
        self.x_line_plot = QGraphicsLineItem()
        self.y_line_plot = QGraphicsLineItem()
        self.RminDisk_plot = QGraphicsEllipseItem()  
        self.RminDisk_plotradius = 10
        self.RmaxDisk_plot = QGraphicsEllipseItem()  
        self.RmaxDisk_plotradius = 10


    def initializeDefaultWidgets(self,):
        range_pen = pg.mkPen('y', width=3, style=Qt.DashLine)
        center_pen = pg.mkPen('r', width=3, style=Qt.DashLine)
        axis_pen = pg.mkPen('w', width=3, style=Qt.DotLine)    
        param = self.viewerGroupParameter.child('display_parameters').child('range').child('pen_param')
        param.updateFromPen(param,range_pen)
        param = self.viewerGroupParameter.child('display_parameters').child('center').child('pen_param')
        param.updateFromPen(param,center_pen)
        param = self.viewerGroupParameter.child('display_parameters').child('axis').child('pen_param')
        param.updateFromPen(param,axis_pen)                     

    def calculate_polar(self,data):
        dR = self.parameterList_VMI_toolbox['radialBins_spinBox']
        dTheta = self.parameterList_VMI_toolbox['angularBins_spinBox']
        self.im_polar,self.rgrid,self.thetagrid = polar.reproject_image_into_polar(data = data,origin = (self.centerY,self.centerX),Jacobian=True,dr=dR,dt=dTheta)
        self.radial_bins = self.rgrid[:,0]
        self.angular_bins = self.thetagrid[0,:]*180/np.pi

##############################################Initialize Widget#############################
    def createDock(self):
        self.radial_plot_dock = dockarea.Dock("Radial distribution", size=(600, 600))
        self.angular_plot_dock = dockarea.Dock("Angular distribution", size=(600, 600))
        self.direct_image_dock = dockarea.Dock("Direct Image", size=(600, 600))
        self.data_plot_dock = dockarea.Dock("Data", size=(600, 600))
        self.central_widget.addDock(self.radial_plot_dock, 'right', self.control_dock)                        
        self.central_widget.addDock(self.angular_plot_dock, 'above', self.radial_plot_dock)                       
        self.central_widget.addDock(self.direct_image_dock, 'above', self.angular_plot_dock)     



    # def update_range(self,R1,R2):                
    #     self.RminDisk_plot.setRect(self.centerX-R1, self.centerY-R1, 2*R1, 2*R1)        
    #     self.RmaxDisk_plot.setRect(self.centerX-R2, self.centerY-R2, 2*R2, 2*R2)
    # def makeMask(self):
    #     self.mask_angular_bins = np.logical_and(self.angular_bins >= -180, self.angular_bins < 180)
    #     self.mask_radial_bins = np.logical_and(self.radial_bins > self.Rmin, self.radial_bins < self.Rmax)

    # def meanCenter(self):              
    #     Cx = np.sum(self.im.mean(axis = 1)*np.arange(self.im.shape[1]))/np.sum(self.im.mean(axis = 1))
    #     Cy = np.sum(self.im.mean(axis = 0)*np.arange(self.im.shape[0]))/np.sum(self.im.mean(axis = 0))


    def makeList_QWidget(self):                
        return['folderBase_lineEdit',                                        
                        ]

def main():

    app = QApplication([])
    tof = VMIPanel()
    tof.show()
    app.exec()

if __name__=="__main__":
    main()