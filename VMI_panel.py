from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QRectF,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QPen)
from PySide6.QtWidgets import (QApplication, QGraphicsEllipseItem,QGraphicsLineItem, QPushButton, QSizePolicy, QToolButton,
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
        self.center_x = 0
        self.center_y = 0
        self.rot_angle = 0
        self.dR = 1
        self.dTheta = np.pi/180

        #Initialize some widgets
        self.initialize_plotWidgets()
        #Open File
        # self.loadFile()
        # self.openFile()
        #Load File
        # self.VMI_load_func()
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
        self.update_axis()

    
    def updateGUI(self,param,values):
        for value in values:
            if value[0] in param.childs[0]: #Image parameters
                self.updateImagePlot
                a = 1
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

        # value[0][0] in param.childs[0]
        # self.label.show()
        # self.label.hide()
        # self.plot.showGrid(x = param.childs[1]['x_grid'], y = param.childs[1]['y_grid'], alpha = param.childs[1]['alpha_grid'])                                                
        # self.plot.setTitle(title = param['title'])
        # self.plot.setLabel('bottom', text=param.childs[2]['x_label'])
        # self.plot.setLabel('left', text=param.childs[3]['y_label'])        

    def connectSignal(self):
        self.image_tableWidget.itemSelectionChanged.connect(self.changeItemSelection)
        self.loadFile_button.pressed.connect(self.loadFilefromButton)
        self.folderBase_lineEdit.editingFinished.connect(self.updateBaseFolder)
        self.folderSelection_toolButton.pressed.connect(self.press_selectFolder_function)
        self.VMI_toolBox.sendParameters_signal.connect(self.computeData)
    def computeData(self,parameters):
        print(parameters)
        self.parameterList_VMI_toolbox = parameters
        self.im_polar
        for index in np.arange(self.image_tableWidget.rowCount()):
            data = np.squeeze(self.fileManager.readVMIData_h5(index))   
            self.calculate_polar(data)

            self.im_polar,self.rgrid,self.thetagrid = polar.reproject_image_into_polar(data = self.im,origin = (self.center_y,self.center_x),Jacobian=True,dr=self.dR,dt=self.dTheta)
            self.radial_bins = self.rgrid[:,0]
            self.angular_bins = self.thetagrid[0,:]*180/np.pi            

    def press_selectFolder_function(self):       
        self.folderBase_lineEdit.setText(str(QFileDialog.getExistingDirectory(self, 'Choose directory')))
    def updateBaseFolder(self):
        self.path_folder = self.folderBase_lineEdit.text()
    def changeItemSelection(self,):    
        self.loadImagefromIndex(self.image_tableWidget.currentRow())

    def loadImagefromIndex(self,index):  
        data = np.squeeze(self.fileManager.readVMIData_h5(index))      
        data = np.delete(data,np.arange(0,10),axis=0)
        self.imageViewer.updateViewerWidget(data)

    def loadFilefromButton(self):
        self.path = str(QFileDialog.getOpenFileName(self, 'Import image',self.path_folder)[0])    
        self.loadFile(self.path)

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
            self.datasetSel_label.setText(self.path)
            self.imageNumber_value.setText(str(len(positions)))

    def initialize_plotWidgets(self):
        self.radial_dist = pg.PlotDataItem()
        self.angular_dist = pg.PlotDataItem()
        self.data_dist = pg.PlotDataItem()
        self.image = pg.ImageItem()
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


    def connectVMISignal(self):
        self.toolbox.changingAngle_signal.connect(self.update_angle)
        self.toolbox.changingCenter_signal.connect(self.update_centers)
        self.toolbox.changingRange_signal.connect(self.update_range)
        self.toolbox.showingAxis_signal.connect(self.show_axisLine)
        self.toolbox.showingCenter_signal.connect(self.show_center)
        self.toolbox.showingRange_signal.connect(self.show_range)
        self.toolbox.changingAngularBin_signal.connect(self.update_radialbin)
        self.toolbox.changingRadialBin_signal.connect(self.update_angularbin)
        self.imageSel_value.valueChanged.connect(self.updateData)     
        self.image_view.scene.sigMouseMoved.connect(self.mouse_moved)
        self.updateCenter_signal.connect(self.toolbox.updateCenter)      
        self.toolbox.abel_inversion_pushbutton.clicked.connect(self.AbelInversion)  

    def calculate_polar(self,data):
        dR = self.parameterList_VMI_toolbox['radialBins_spinBox']
        dTheta = self.parameterList_VMI_toolbox['angularBins_spinBox']
        self.im_polar,self.rgrid,self.thetagrid = polar.reproject_image_into_polar(data = data,origin = (self.center_y,self.center_x),Jacobian=True,dr=dR,dt=dTheta)
        self.radial_bins = self.rgrid[:,0]
        self.angular_bins = self.thetagrid[0,:]*180/np.pi
        # self.update_plot()

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

    # def AbelInversion(self):
    #     self.N = 5
    #     self.abel_obj = Abel_object(self.im, self.center_y, self.center_x, self.dTheta, self.dR, self.N, self.Rmax)  
    #     self.abel_obj.precalculate()
    #     self.abel_obj.invert()
    #     self.im_inverted = self.abel_obj.make_inverse_image(self.Rmax,self.N,0)
    #     if not(self.abel_plot_dock):
    #         self.abel_plot_dock = dockarea.Dock("Abel inverted image", size=(600, 600))
    #         self.central_widget.addDock(self.abel_plot_dock, 'right', self.control_dock)     
    #         self.image_inverted = pg.ImageItem()        
    #         self.image_inverted.setImage(self.im_inverted)  # set image to display, used only for tests
    #         self.image_inverted_view = pg.ImageView(imageItem=self.image_inverted, view=pg.PlotItem())     
    #         self.abel_plot_dock.addWidget(self.image_view)
    #         self.image_inverted_view.view.invertY(False)
    #         self.image_inverted_view.setColorMap(self.colormap())                  

    #     self.image_inverted.setImage(self.image_inverted)  # set image to display, used only for tests
        


##############################################Initialize Widget#############################
    def createDock(self):
        self.radial_plot_dock = dockarea.Dock("Radial distribution", size=(600, 600))
        self.angular_plot_dock = dockarea.Dock("Angular distribution", size=(600, 600))
        self.direct_image_dock = dockarea.Dock("Direct Image", size=(600, 600))
        self.data_plot_dock = dockarea.Dock("Data", size=(600, 600))
        self.central_widget.addDock(self.radial_plot_dock, 'right', self.control_dock)                        
        self.central_widget.addDock(self.angular_plot_dock, 'above', self.radial_plot_dock)                       
        self.central_widget.addDock(self.direct_image_dock, 'above', self.angular_plot_dock)     

    def openFile(self): 
        self.createDock()                      
        if self.path is None:
            self.path = str(QFileDialog.getOpenFileName(self, 'Import image','Q:\LIDyL\Atto\ATTOLAB\SE1\SlowRABBIT')[0])    
            # self.path = str(QFileDialog.getOpenFileName(self, 'Import image','D:\\Work\\Saclay\\Git\\analysis_GUI_Qt')[0])        
        self.path_object = pathlib.Path(self.path)             
        try:
            h5file = True
            if h5file:
                self.scan = '000'  # vérifier dans hdfview
                self.path2 = ''.join(['Scan',self.scan,'/Detector000/Data2D/Ch000/Data'])
                with h5py.File(self.path, 'r') as file:                          
                    self.raw_datas = file['Raw_datas']   
                    self.image_number = self.raw_datas[self.path2].shape[0]  
                    self.toolbox.imageCentX_value.setMaximum(self.raw_datas[self.path2].shape[1])
                    self.toolbox.imageCentY_value.setMaximum(self.raw_datas[self.path2].shape[2])
                    self.im = np.asarray(self.raw_datas[self.path2][0]).T
        except Exception:
            print(traceback.format_exception(*sys.exc_info()))   
        self.meanCenter()                            
        self.signal_VMI_panel_creation.emit(['VMI',self.path])

    def readFile(self, index=0):
        try:
            with h5py.File(self.path, 'r') as file:                          
                self.raw_datas = file['Raw_datas']     
                self.im = np.asarray(self.raw_datas[self.path2][index]).T                
        except Exception:
            print(traceback.format_exception(*sys.exc_info())) 

        self.im = rotate(self.im,self.toolbox.imageRot_value.value(), resize=False,center= [self.toolbox.imageCentY_value.value(),self.toolbox.imageCentX_value.value()])                                
        self.calculate_polar()    
    def VMI_load_func(self):
        self.image_index = 0
        self.readFile()
        #LABELS + LINE EDITS
        self.imageSel_value.setSuffix('/'+f'{self.image_number}')
        self.imageSel_value.setMaximum(self.image_number)
        self.imageSel_value.setValue(self.image_index)
        self.dataset_value.setText(f'{self.path_object.stem }')                            
        # self.radial_dist = pg.PlotDataItem()
        # self.angular_dist = pg.PlotDataItem()
        # self.data_dist = pg.PlotDataItem()
        self.radial_dist.setData(x = self.radial_bins, y=np.sum(self.im_polar,axis = 1))
        self.angular_dist.setData(x = self.angular_bins, y=np.sum(self.im_polar,axis = 0))
        # self.angular_dist.setData(x = )
        # self.data_dist.setData(x = )
        self.radial_item = pg.PlotItem()
        self.radial_item.addItem(self.radial_dist)
        self.angular_item = pg.PlotItem()
        self.angular_item.addItem(self.angular_dist)
        self.radial_view = pg.PlotWidget(plotItem = self.radial_item)
        self.angular_view = pg.PlotWidget(plotItem = self.angular_item)
        self.radial_plot_dock.addWidget(self.radial_view)
        self.angular_plot_dock.addWidget(self.angular_view)        
        self.image.setImage(self.im)  # set image to display, used only for tests
        self.image_view = pg.ImageView(imageItem=self.image, view=pg.PlotItem())        
        self.image_view.view.invertY(False)
        self.image_view.setColorMap(self.colormap())    
        self.image_view.view.addItem(self.center_plot)   
        self.image_view.view.addItem(self.x_line_plot)   
        self.image_view.view.addItem(self.y_line_plot)   
        self.image_view.view.addItem(self.RminDisk_plot)   
        self.image_view.view.addItem(self.RmaxDisk_plot)   
        self.direct_image_dock.addWidget(self.image_view)
        self.updatePlots()

    def colormap(self):
        # doing a custom colormap (trying to make it close to the Labview one)
        pos = np.array([0.0, 0.01, 0.2, 0.4, 0.5, 0.8, 0.99, 1.0])
        color = np.array([[0, 0, 0, 255], [128, 0, 255, 255], [0, 0, 255, 255],
                        [0, 255, 255, 255], [0, 255, 0, 255],
                        [255, 255, 0, 255], [255, 0, 0, 255], [255, 255, 255, 255]],
                        dtype=np.ubyte)
        return pg.ColorMap(pos, color)  
    def close_panel_VMI(self, index):
        self.signal_VMI_panel_destruction.emit(self.panel_index)
        print(f'Close event: VMI panel {self.panel_index} is now closed')  
##############################################UPDATE COMPONENTS#############################

    def mouse_moved(self, view_pos):
        try:
            data = self.im
            n_rows, n_cols = data.shape
            scene_pos = self.image_view.getImageItem().mapFromScene(view_pos)

            row, col = int(scene_pos.x()), int(scene_pos.y())  # I inverted x and y

            if (0 <= row < n_rows) and (0 <= col < n_cols):
                value = data[row, col]
                self.coords_lb.setText('x = {:d}, y = {:d}\n value = {:}'.format(row, col, value))
                self.coords_lb.repaint()
            else:
                self.coords_lb.setText('')
            #time.sleep(0.1)        
        except AttributeError:  # when no image is displayed yet
            print(traceback.format_exception(*sys.exc_info()))  


##############################################UPDATE COMPONENTS#############################
    def updateData(self, input=0):
        self.image_index = int(input)
        self.readFile(self.image_index)        
        self.updatePlots()
    def updatePlots(self):
        self.updateRadialPlot()
        self.updateAngularPlot()
        self.updateImagePlot()
    def updateRadialPlot(self):
        self.radial_dist.setData(x=self.radial_bins[self.mask_radial_bins],y=np.sum(self.im_polar[self.mask_radial_bins,:],axis = 1))
    def updateAngularPlot(self):        
        self.angular_dist.setData(x=self.angular_bins[self.mask_angular_bins],y=np.sum(self.im_polar[:,self.mask_angular_bins], axis=0))
    def updateImagePlot(self): 
        self.image.setImage(self.im)  # set image to display, used only for tests
    def update_centers(self,Cx,Cy):
        self.center_x = Cx
        self.center_y = Cy               
        self.Rmin = self.toolbox.Rmin_spinbox.value()
        self.Rmax = self.toolbox.Rmax_spinbox.value()
        self.center_plot.setRect(self.center_x-self.center_plotradius, self.center_y-self.center_plotradius, 2*self.center_plotradius, 2*self.center_plotradius)                
        self.update_axis()
        self.calculate_polar()
        self.update_range(self.Rmin,self.Rmax)
    def update_axis(self):
        line_x = np.array([-1024,0,1024,0])
        line_y = np.array([0,-1024,0,1024])
        line_x[0::2] = line_x[0::2] + self.center_x
        line_y[0::2] = line_y[0::2] + self.center_x
        line_x[1::2] = line_x[1::2] + self.center_y
        line_y[1::2] = line_y[1::2] + self.center_y
        self.x_line_plot.setLine(*line_x)
        self.y_line_plot.setLine(*line_y)

        # self.x_line_plot.setLine(line_x[0],line_x[1],line_x[2],line_x[3])
        # self.y_line_plot.setLine(line_y[0],line_y[1],line_y[2],line_y[3])
    def update_angle(self,theta):
        self.im = rotate(self.im,theta-self.rot_angle, resize=False,center= [self.toolbox.imageCentY_value.value(),self.toolbox.imageCentX_value.value()])                                
        self.rot_angle = theta
        self.updateImagePlot()
    def update_range(self,R1,R2):                
        self.RminDisk_plot.setRect(self.center_x-R1, self.center_y-R1, 2*R1, 2*R1)        
        self.RmaxDisk_plot.setRect(self.center_x-R2, self.center_y-R2, 2*R2, 2*R2)
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
        
      

def main():

    app = QApplication([])
    tof = VMIPanel()
    tof.show()
    app.exec()

if __name__=="__main__":
    main()