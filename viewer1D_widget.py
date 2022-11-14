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
from re import I
from turtle import Pen
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,Signal,QItemSelectionModel,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QAction,
    QFont, QFontDatabase, QGradient, QIcon,QTransform,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QCloseEvent)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QPushButton,QListWidgetItem,QTableWidgetItem,QAbstractItemView,
    QSizePolicy, QWidget, QFileDialog,QMenu)
import pyqtgraph as pg
from CustomROI import CustomLinearRegionItem
from usefulclass import ClassManipulation
from viewer1D_widget_ui import Ui_Viewer1DWidget
import numpy as np
import matplotlib.pyplot as plt
# app = pg.mkQApp("Parameter Tree Example")
from ParameterTree import PlotGroupParameter,Viewer1DGroupParameter

class Viewer1DWidget(Ui_Viewer1DWidget,QWidget):
    signal_importCurrentData = Signal()
    signal_importCustomData = Signal()
    def __init__(self,parent=None,name = 'Viewer1D'):
        super(Viewer1DWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.ROI = []
        self.plot_list = []        
        self.label = pg.LabelItem(justify = "right")
        self.viewer_GraphicsLayoutWidget.addItem(self.label)
        self.plot,self.view_1D = self.setupPlotWidget(self.viewer_GraphicsLayoutWidget,title=name,row = 0, col = 0)
        self.setupTreeParameterWidget()
        self.proxy = pg.SignalProxy(self.view_1D.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)     
        self.connectSignals()
        self.addPlot_pushButton.clicked.connect(self.addPlot)
        self.updateGUI()
        if parent:
            self.setParent(parent)
    def connectSignals(self):     
        self.makeROI_toolButton.toolButtonClicked_signal.connect(self.addROI)
        self.tableROI_tableWidget.removeItem_signal.connect(self.removeROITableItem)        
        self.options_checkBox.stateChanged.connect(self.updateGUI)
        
    def showHideWidget(self,items,show_bool = True):
        if show_bool:        
            [item.show() for item in items]
        else:
            [item.hide() for item in items]

    def updateGUI(self):
        self.showHideWidget([self.tabWidget],self.options_checkBox.isChecked())
        # self.adjustSize()

    def setupTreeParameterWidget(self):
        contextMenu = {'Expand/Collapse':
                        [
                            {'Expand':[]},
                            {'Collapse':[]}
                        ],
                        'Clear':[],
                        'Load':
                        [
                            {'File':
                            [
                                {'.txt':[]},
                                {'.py':[]},
                                {'.something':[]}
                            ] }
                        ]
                        }        
        contextMenu = {'Load':[],
                        'Clear':[],
                        }                                 
        contextActions = ['Expand All','Collapse All']
        self.plotGroupParameter = PlotGroupParameter(name="plot_list",title="Plot List", tip='',
                     children=[],context=contextActions,menu= contextMenu)
        self.plotGroupParameter.sigChildRemoved.connect(self.removePlotTree)      
        self.plotGroupParameter.valueChanging_signal.connect(self.updatePlotDataItem)
        self.plotGroupParameter.duplicatePlot_signal.connect(self.duplicatePlot)
        self.plotGroupParameter.sigContextMenu.connect(self.contextMenuEventParameter)
        self.plot_ParameterTree.setParameters(self.plotGroupParameter)
        self.plot_ParameterTree.itemSelected_signal.connect(self.updatePlotSelection)
        self.plot_ParameterTree.plot_list = self.plot_list

        contextMenu = {'Save settings':[],
                        'Copy settings':[],
                        'Load settings':[],
                        }   
        self.viewerGroupParameter = Viewer1DGroupParameter(name="viewer_options",title="Viewer settings", tip='',
                     children=[],context=contextActions,menu= contextMenu,expanded = False)
        self.viewerGroupParameter.valueChanging_signal.connect(self.updatePlotWidget)

        self.settings_ParameterTree.setParameters(self.viewerGroupParameter)
    def contextMenuEventParameter(self,object,path):
        dic = ClassManipulation.makeDictfromTuple(path)
        if path[0] == 'Clear':
            object.clearChildren()
        elif path[0] == 'Load':
            print('Opening dialog box')





        a = 1
    def test(self,group_parameter,contextMenu):
        if (contextMenu =='Expand All') | (contextMenu =='Collapse All'):
            self.plotGroupParameter.activate(contextMenu)
        print(self.plot_ParameterTree.selectedItems())




        # self.view_1D.scene().sigMouseClicked.connect(self.onClick)        

    # def onClick(self,event):
    #     items = self.viewer_GraphicsLayoutWidget.scene().items(event.scenePos())
    #     print( "Plots:", [x for x in items if isinstance(x, pg.PlotCurveItem)])
    #     [x for x in items if isinstance(x, pg.PlotCurveItem)]
    #     event.accept()
    #     self.view_1D.raiseContextMenu(event)
    #     if pg.PlotCurveItem in items:
    #         print(0)

    def getDataFromPlot(self,plot,):
        return plot.xData,plot.yData


    def duplicatePlot(self,plotParameter):
        name = plotParameter.name()+'_copy'
        for plotDataItem,plotParameterGroup in self.plot_list:
            if plotParameter == plotParameterGroup:
        # for index in range(len(self.plot_list)):
            # if self.plotGroupParameter.childs[index] == plotParameter:  
            # plotElements = self.plot_list[index]
            # if plotParameter in plotElements:
                x,y = self.getDataFromPlot(plotDataItem) 
                self.addPlot(name=name,x=x,y=y)

    def addPlot(self,name = None, x = np.arange(1000),y = None):
        if y is None:
            y = np.random.normal(0,100)+np.random.normal(size=(1000,))
        plot_dataItem = pg.PlotDataItem(x,y)
        color_plot = pg.intColor(len(self.plot_list))
        plot_dataItem.setPen(color_plot)
        plot_dataItem.setCurveClickable(True,width = 3)
        plot_dataItem.sigClicked.connect(self.plotDataGotClicked)
        self.plot.addItem(plot_dataItem)

        index = len(self.plot_list)
        self.plotGroupParameter.addNew(parameters=plot_dataItem.opts['pen'],name = name)  
        # self.plotGroupParameter.sigChildRemoved.connect(self.removePlotTree)      
        # self.plotGroupParameter.valueChanging_signal.connect(self.updatePlotDataItem)
        # self.plotGroupParameter.duplicatePlot_signal.connect(self.duplicatePlot)
        self.plot_list.append([plot_dataItem,self.plotGroupParameter.childs[index]])

    def updatePlotDataItem(self,plotParameter,item):
        name = plotParameter.name()
        for index in range(len(self.plot_list)):
            if self.plotGroupParameter.childs[index] == plotParameter.parent():
                if name == 'show_plot':
                    self.showPlot(item,index)
                elif name == 'pen_param':
                    self.setPenPlot(item,index)

    def plotDataGotClicked(self,ev): 
        print('Got clicked')
        # self.tablePlot_tableWidget.setCurrentCell([i for i in range(len(self.plot_list)) if self.plot_list[i] == ev][0],0)

        
    def updatePlotWidget(self,param):
        self.label.show()
        self.label.hide()
        self.plot.showGrid(x = param.childs[1]['x_grid'], y = param.childs[1]['y_grid'], alpha = param.childs[1]['alpha_grid'])                                                
        self.plot.setTitle(title = param['title'])
        self.plot.setLabel('bottom', text=param.childs[2]['x_label'])
        self.plot.setLabel('left', text=param.childs[3]['y_label'])


    def setupPlotWidget(self,layout,title = '', row = None, col = None):
        plot = layout.addPlot(title=title,labels={'bottom': ('x axis title'), 'left': ('y axis title')}
                                ,row = row, col = col,enableMenu = True)
        plot.ctrlMenu = None
        plot.showGrid(x = True, y = True, alpha = 0.3)                                                
        # self.legend = pg.LegendItem()
        # self.legend.setParentItem(plot)
        view = plot.getViewBox()
        return plot,view

    def mouseMoved(self,evt):
        mousePoint = self.plot.vb.mapSceneToView(evt[0])
        self.label.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))



    def selectPlot(self,row):        
        if row in self.plot_ParameterTree.get_selectedRows():
            shadowpen = self.plot_list[row][0].pen()
            shadowpen.setWidth(shadowpen.width()+1)
            self.plot_list[row][0].setShadowPen(shadowpen)
        else:
            self.plot_list[row][0].setShadowPen(None)

    def setPenPlot(self,pen,row):
        self.plot_list[row][0].setPen(pen)
        if row in self.plot_ParameterTree.get_selectedRows():
            shadowpen = pg.mkPen(pen)
            shadowpen.setWidth(shadowpen.width()+1)
            self.plot_list[row][0].setShadowPen(shadowpen)

    def showPlot(self,status,row):
        if status:
            self.plot_list[row][0].show()
        else:
            self.plot_list[row][0].hide()

    def showHideWidget(self,items,show_bool = True):
        if show_bool:        
            [item.show() for item in items]
        else:
            [item.hide() for item in items]

    ################################################## ROI functions ##########################################    

    def addROI(self,toolButton,action):
        if action.data() == 'IL_H':
            ROI = self.addROI_infiniteLineItem(np.sum(self.view_1D.viewRange()[1])/2,0,'y')
        elif action.data() == 'IL_V':  
            ROI = self.addROI_infiniteLineItem(np.sum(self.view_1D.viewRange()[0])/2,90,'x')          
        elif action.data() == 'LR_H':            
            ROI = self.addROI_linearRegionItem(self.view_1D.viewRange()[1],'horizontal')
        elif action.data() == 'LR_V':                        
            ROI = self.addROI_linearRegionItem(self.view_1D.viewRange()[0],'vertical')            
        self.ROI.append(ROI)
        # Show ROI item in viewer
        self.plot.addItem(self.ROI[-1])   
        # Store ROI item in table
        self.tableROI_tableWidget.addEntry(orientation=action.data())

    def addROI_linearRegionItem(self,edges,orientation):
        # Create ROI item
        lr = CustomLinearRegionItem(self.makeInitialShape(edges),orientation=orientation)        
        lr.leftDoubleClicked.connect(self.gotLeftDoubleClicked)
        lr.singleMiddleClicked.connect(self.gotMiddleSingleClicked)
        lr.setZValue(10)
        return lr

    def addROI_infiniteLineItem(self,pos,angle,label):
        # self.view_1D.viewRange()[1]
        # pos = np.sum(self.view_1D.viewRange()[0])/2
        il = pg.InfiniteLine(pos = pos,movable=True, angle=angle, label=label+'={value:0.2f}', 
                       labelOpts={'position':0.1, 'color': (200,200,100), 'fill': (200,200,200,50), 'movable': True})
        il.setZValue(10)
        return il

    def makeInitialShape(self,edges):      
        lengths = edges[0] + np.diff(edges)*np.array([2,3])/5
        return lengths

    def gotMiddleSingleClicked(self,ROI_clicked):
        print('I got destroyed')
        for index, ROI in enumerate(self.ROI): 
            if ROI_clicked == ROI:
                self.removeROI(ROI)
                self.tableROI_tableWidget.removeRow(index)
                return
    def gotLeftDoubleClicked(self,ROI_clicked):
        print('I got doubleclicked')
        for index, ROI in enumerate(self.ROI): 
            if ROI_clicked == ROI:
                self.tableROI_tableWidget.selectRow(index)
                return

    def removePlot(self,item):
        self.plot.removeItem(item[0]) 
        self.plot_list.remove(item)
    def removePlotTree(self,obj,child):
        removedItems = [plotItem for plotItem in self.plot_list if child == plotItem[1]]
        [self.removePlot(item) for item in removedItems]
        
    def clearPlot(self):
        a = 1
        # a = requestRemove
        [self.removePlot(item) for item in self.plot_list]

    def updatePlotSelection(self,row,status):    
        if len(self.plot_list) > row:
            plotDataItem =  self.plot_list[row][0]
            if status == 'unselected':   
                plotDataItem.setShadowPen(None)
            elif status == 'selected':
                shadowpen = pg.mkPen(plotDataItem.opts['pen'])
                shadowpen.setWidth(shadowpen.width()+1)
                plotDataItem.setShadowPen(shadowpen)

    def removeROI(self,item):
        self.plot.removeItem(item) 
        self.ROI.remove(item)

    def updateROISelection(self,row,status):
        if len(self.ROI) > row:
            self.ROI[row].changeROIColor(status)
    def removeROITableItem(self,row):
        self.removeROI(self.ROI[row])

    ################################################## Context menu functions ##########################################  
    def axisToIndex(self,axis,scale,offset):
        return int((axis-offset)/scale)
    def indexToAxis(self,index,scale,offset):        
        return (index*scale+offset)

    def getImageRegion(self,edges,orientation,parameters):
        axis_plot = self.makeAxis(parameters)       
        if orientation == 'H':
            l_b,h_b = [self.axisToIndex(edge,parameters[1][1],parameters[1][2]) for edge in edges]
            ROI_zone = self.getImageData()[:,l_b:h_b]
            axis_plot[1] = axis_plot[1][np.logical_and(axis_plot[1] >= edges[0],axis_plot[1] <= edges[1])]
        elif orientation == 'V':
            l_b,h_b = [self.axisToIndex(edge,parameters[0][1],parameters[0][2]) for edge in edges]
            ROI_zone = self.getImageData()[l_b:h_b,:]
            axis_plot[0] = axis_plot[0][np.logical_and(axis_plot[0] >= edges[0],axis_plot[0] <= edges[1])]
        return ROI_zone,axis_plot
    
    def getAxis(self):
        return self.makeAxis(self.getImageTransformParameters())

    def makeAxis(self,parameters):
        axis = []
        for parameter in parameters:
            n,scale,offset = parameter
            axis.append(np.arange(n)*scale+offset)
        return axis

    def getOrientationIndex(self,orientation):
        if orientation == 'H':
            return 0
        elif orientation == 'V':
            return 1


    def sendQMenuCommand(self,command):
        if command == 'COM':
            self.getCOM()
        elif command == 'Sum':
            self.getSum()
        elif command == 'Max':            
            self.getMax()
        elif command == 'Min':            
            self.getMin()

    def getCOM(self):
        image_parameters = self.getImageTransformParameters()
        for row in self.tableROI_tableWidget.get_selectedRows():
            orientation = self.tableROI_tableWidget.item(row,1).text()
            image_ROI,axis_plot = self.getImageRegion(self.ROI[row].getRegion(),orientation,image_parameters)
            if orientation == 'H':
                xAxis_plot = axis_plot[0]
                max_ROI = axis_plot[1][np.argmax(image_ROI,axis=1)]
            elif orientation == 'V':     
                xAxis_plot = axis_plot[1]       
                max_ROI = axis_plot[0][np.argmax(image_ROI,axis=0)]
            plt.plot(xAxis_plot,max_ROI,label=self.tableROI_tableWidget.item(row,0).text)
        plt.show() 
          
    def getMax(self) :
        image_parameters = self.getImageTransformParameters()        
        for row in self.tableROI_tableWidget.get_selectedRows():
            orientation = self.tableROI_tableWidget.item(row,1).text()
            image_ROI,axis_plot = self.getImageRegion(self.ROI[row].getRegion(),orientation,image_parameters)
            if orientation == 'H':
                xAxis_plot = axis_plot[0]
                max_ROI = axis_plot[1][np.argmax(image_ROI,axis=1)]
            elif orientation == 'V':     
                xAxis_plot = axis_plot[1]       
                max_ROI = axis_plot[0][np.argmax(image_ROI,axis=0)]
            plt.plot(xAxis_plot,max_ROI,label=self.tableROI_tableWidget.item(row,0).text)
        plt.show()    
            
    def getSum(self) :
        image_parameters = self.getImageTransformParameters()
        for row in self.tableROI_tableWidget.get_selectedRows():
            orientation = self.tableROI_tableWidget.item(row,1).text()
            image_ROI,axis_plot = self.getImageRegion(self.ROI[row].getRegion(),orientation,image_parameters)
            if orientation == 'H':
                xAxis_plot = axis_plot[0]                
                sum_ROI = np.sum(image_ROI,axis=1)
            elif orientation == 'V':    
                xAxis_plot = axis_plot[1]        
                sum_ROI = np.sum(image_ROI,axis=0)
            plt.plot(xAxis_plot,sum_ROI,label=self.tableROI_tableWidget.item(row,0).text)
        plt.show()


def main():
    import sys
    app = QApplication([])
    tof = Viewer1DWidget()
    tof.show()
    app.exec()

if __name__=="__main__":
    main()




    