from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QRectF,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
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
        self.viewerGroupParameter.valueChanging_signal.connect(self.updateGUI)


        self.settings_parameterTree.setParameters(self.viewerGroupParameter)     

        self.imageViewer.view_2D.addItem(self.x_line_plot)
        self.imageViewer.view_2D.addItem(self.y_line_plot)
        self.imageViewer.view_2D.addItem(self.RminDisk_plot)
        self.imageViewer.view_2D.addItem(self.RmaxDisk_plot)        
        self.imageViewer.view_2D.addItem(self.center_plot)
       
        self.updateImageViewer()


    def updateImageViewer(self):
        self.centerX = self.viewerGroupParameter.child('image_parameters').child('centerX').value()
        self.centerY = self.viewerGroupParameter.child('image_parameters').child('centerY').value()
        self.rot_angle = self.viewerGroupParameter.child('image_parameters').child('theta').value()     
        self.cropX = self.viewerGroupParameter.child('image_parameters').child('cropX').value()
        self.cropY = self.viewerGroupParameter.child('image_parameters').child('cropY').value()
        self.isTransposed = self.viewerGroupParameter.child('image_parameters').child('transpose').value()
        self.Rmax = self.viewerGroupParameter.child('image_parameters').child('Rmax').value()
        self.data = self.getData()
        self.updateAxis()
        self.updateWidgets()
        self.updateImagePlot(self.data)

    def updateGUI(self,param,values):
        for value in values:
            if value[0] in param.childs[0]: #Image parameters
                self.updateImageViewer()
                # a = 1
            elif value[0] in param.childs[1]: #Display parameters
                if param.childs[1]['show_axis']:
                    self.x_line_plot.show()
                    self.y_line_plot.show()
                else:
                    self.x_line_plot.hide()
                    self.y_line_plot.hide()                    
                if param.childs[1]['show_range']:
                    self.RminDisk_plot.show()    
                    self.RmaxDisk_plot.show()      
                else:
                    self.RminDisk_plot.hide()
                    self.RmaxDisk_plot.hide()       

                if param.childs[1]['show_center']:
                    self.center_plot.show()
                else:
                    self.center_plot.hide()
    
    def connectSignal(self):
        self.image_tableWidget.itemSelectionChanged.connect(self.changeItemSelection)
        self.loadFile_button.pressed.connect(self.loadFilefromButton)
        self.folderBase_lineEdit.editingFinished.connect(self.updateBaseFolder)
        self.folderSelection_toolButton.pressed.connect(self.press_selectFolder_function)
        self.VMI_toolBox.sendParameters_signal.connect(self.computeData)

    
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
            if self.isTransposed:
                data = data.T
            data = self.transformData(data)
            return data

    def loadData(self,index):
        return np.squeeze(self.fileManager.readVMIData_h5(index))  
    
    def transformData(self,data):
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
        # data = self.getData(index)
        self.imageViewer.updateViewerWidget(self.getData(index))

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
        # self.radial_dist = pg.PlotDataItem()
        # self.angular_dist = pg.PlotDataItem()
        # self.data_dist = pg.PlotDataItem()
        # self.image = pg.ImageItem()
        self.center_plot = QGraphicsEllipseItem()  
        self.center_plotradius = 10
        self.center_plot.setPen(pg.mkPen('r', width=3, style=Qt.DashLine))                     
        self.x_line_plot = QGraphicsLineItem()
        self.x_line_plot.setPen(pg.mkPen('w', width=3, style=Qt.DotLine)) 
        self.y_line_plot = QGraphicsLineItem()
        self.y_line_plot.setPen(pg.mkPen('w', width=3, style=Qt.DotLine))       
        self.RminDisk_plot = QGraphicsEllipseItem()  
        self.RminDisk_plotradius = 10
        self.RminDisk_plot.setPen(pg.mkPen('y', width=3, style=Qt.DashLine))     
        self.RmaxDisk_plot = QGraphicsEllipseItem()  
        self.RmaxDisk_plotradius = 10
        self.RmaxDisk_plot.setPen(pg.mkPen('y', width=3, style=Qt.DashLine))   


    def calculate_polar(self,data):
        dR = self.parameterList_VMI_toolbox['radialBins_spinBox']
        dTheta = self.parameterList_VMI_toolbox['angularBins_spinBox']
        self.im_polar,self.rgrid,self.thetagrid = polar.reproject_image_into_polar(data = data,origin = (self.centerY,self.centerX),Jacobian=True,dr=dR,dt=dTheta)
        self.radial_bins = self.rgrid[:,0]
        self.angular_bins = self.thetagrid[0,:]*180/np.pi

    def update_plot(self):
        self.makeMask()
        self.updateRadialPlot()
        self.updateAngularPlot()
        
    def makeMask(self):
        self.mask_angular_bins = np.logical_and(self.angular_bins >= -180, self.angular_bins < 180)
        self.mask_radial_bins = np.logical_and(self.radial_bins > self.Rmin, self.radial_bins < self.Rmax)

    def meanCenter(self):              
        Cx = np.sum(self.im.mean(axis = 1)*np.arange(self.im.shape[1]))/np.sum(self.im.mean(axis = 1))
        Cy = np.sum(self.im.mean(axis = 0)*np.arange(self.im.shape[0]))/np.sum(self.im.mean(axis = 0))
        self.toolbox.imageCentX_value.setValue(Cx)
        self.toolbox.imageCentY_value.setValue(Cy)        
        self.update_centers(Cx,Cy)

##############################################Initialize Widget#############################
    def createDock(self):
        self.radial_plot_dock = dockarea.Dock("Radial distribution", size=(600, 600))
        self.angular_plot_dock = dockarea.Dock("Angular distribution", size=(600, 600))
        self.direct_image_dock = dockarea.Dock("Direct Image", size=(600, 600))
        self.data_plot_dock = dockarea.Dock("Data", size=(600, 600))
        self.central_widget.addDock(self.radial_plot_dock, 'right', self.control_dock)                        
        self.central_widget.addDock(self.angular_plot_dock, 'above', self.radial_plot_dock)                       
        self.central_widget.addDock(self.direct_image_dock, 'above', self.angular_plot_dock)     

##############################################UPDATE COMPONENTS#############################
    # def updateData(self, input=0):
    #     self.image_index = int(input)
    #     self.readFile(self.image_index)        
    #     self.updatePlots()
    # def updatePlots(self):
    #     self.updateRadialPlot()
    #     self.updateAngularPlot()
    #     self.updateImagePlot()
    # def updateRadialPlot(self):
    #     self.radial_dist.setData(x=self.radial_bins[self.mask_radial_bins],y=np.sum(self.im_polar[self.mask_radial_bins,:],axis = 1))
    # def updateAngularPlot(self):        
    #     self.angular_dist.setData(x=self.angular_bins[self.mask_angular_bins],y=np.sum(self.im_polar[:,self.mask_angular_bins], axis=0))
    def updateImagePlot(self,data):     
        if data is not None:
            self.imageViewer.updateViewerWidget(data)

    def update_centers(self,Cx,Cy):
        self.centerX = Cx
        self.centerY = Cy               
        self.Rmin = self.toolbox.Rmin_spinbox.value()
        self.Rmax = self.toolbox.Rmax_spinbox.value()
        self.center_plot.setRect(self.centerX-self.center_plotradius, self.centerY-self.center_plotradius, 2*self.center_plotradius, 2*self.center_plotradius)                
        self.updateAxis()
        self.calculate_polar()
        self.update_range(self.Rmin,self.Rmax)


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
    def updateRmax(self):                
        self.RmaxDisk_plot.setRect(self.centerX-Rmax, self.centerY-Rmax, 2*Rmax, 2*Rmax)

    def update_range(self,R1,R2):                
        self.RminDisk_plot.setRect(self.centerX-R1, self.centerY-R1, 2*R1, 2*R1)        
        self.RmaxDisk_plot.setRect(self.centerX-R2, self.centerY-R2, 2*R2, 2*R2)
        self.update_plot()
    def update_angularbin(self,dTheta):
        self.dTheta = dTheta     
        self.calculate_polar()   
    def update_radialbin(self,dR):
        self.dR = dR
        self.calculate_polar()
    def show_range(self,status):
        self.RmaxDisk_plot.setVisible(status)
        self.RminDisk_plot.setVisible(status)
    def show_center(self,status):
        self.center_plot.setVisible(status)   
    def show_axisLine(self,status):
        self.x_line_plot.setVisible(status)
        self.y_line_plot.setVisible(status)
        


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