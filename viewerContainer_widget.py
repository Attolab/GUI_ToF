
from ast import Param
from ctypes import alignment
from inspect import Parameter
from PySide6 import QtWidgets
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,SIGNAL,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt,Signal,QProcess)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform, QWindow,QCloseEvent)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,QVBoxLayout,
    QSizePolicy, QStatusBar, QTabWidget, QWidget,QDockWidget,QFileDialog,QTableWidgetItem,QHBoxLayout)
import pyqtgraph as pg
from mainwindow_ui import Ui_MainWindow
from fileSelection_panel import FileSelectionPanel
# from panels.DockTitleBar import DockTitleBar
from main_panel import MainPanel
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
import sys, traceback
import h5py
import numpy as np
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter,ParameterTree
from pyqtgraph.parametertree.parameterTypes import GroupParameter

from viewer1D_widget import Viewer1DWidget
from viewer2D_widget import Viewer2DWidget
from viewerContainer_widget_ui import Ui_ViewerContainer
#for i in *.ui; do pyside6-uic ${i%.ui}.ui > ${i%.ui}_ui.py; done


class ViewerContainer(Ui_ViewerContainer,QWidget):
    showViewer_signal = Signal()
    addViewerWidget_signal = Signal(object)
    def __init__(self, parent=None):
            super(ViewerContainer,self).__init__(parent,)
            self.setupUi(self)

            # Parameter.cre
            # self.viewer_ParameterTree.setParameters()
            # self.connectSignals()

    # def setupUI(self):
    #     w1 = pg.LayoutWidget(self)
    #     w1 = QHBoxLayout(self)
    #     self._browser = ViewerBrowser(self)
    #     self._browser.setWindowFlag(Qt.WindowStaysOnTopHint)
    #     # self._browser.setAlignment()
    #     self._dockArea = ViewerDockArea(self)
    #     w1.addWidget(self._browser,)
    #     w1.insertWidget(-1,self._dockArea,alignment=Qt.AlignRight)
    #     self._browser.addViewer_signal.connect(self._dockArea.addViewerWidget)

    # def connectSignals(self):
    #     self.addViewerWidget_signal.connect(self._dockArea.addViewerWidget)

    def browser(self):
        return self._browser
    def dockArea(self):
        return self._dockArea
class ViewerContainerParameter(GroupParameter):
    def __init__(self, **opts):
        # opts['type'] = 'group'
        pTypes.GroupParameter.__init__(self, **opts)

    def addNew(self, **opts):
        parameters = opts.get('parameters', None)
        name = opts.get('name', None)
        if name:
            name = self.makeNextNameEntry(name)
        else:
            name = self.makeNextNameEntry()
        pen_param = Parameter.create(name='pen_param',title='Pen parameters', type='pen',expanded = False)
        if parameters:
            pen_param.updateFromPen(pen_param,parameters)
        show_plot = Parameter.create(name= 'show_plot', title = 'Show',type= 'bool', value= True,expanded = False)
        show_plot.sigValueChanged.connect(self.valueChanging)
        pen_param.sigValueChanging.connect(self.valueChanging)
        p = Parameter.create(name=name, type='group', children=[show_plot,pen_param], removable=True, renamable=True,
            menu={'Duplicate':[],'Data Treatment':[{'Filter':[]},{'Smoothing':[]}]})   
        p.sigRemoved.connect(self.removingPlotGroup)
        p.sigContextMenu.connect(self.contextMenuTriggered)      
        self.addChildren(
            [p,])
        print([[childs.name(),childs.value()] for childs in pen_param.childs])

        grid_params =  {
                    'x_grid': {
                        'title':'x',                                        
                        'type': 'bool',
                        'value': True,
                        },   
                    'y_grid': {
                        'title':'y',                                        
                        'type': 'bool',
                        'value': True,
                        },    
                    'alpha_grid': {
                        'title':'alpha',                                        
                        'type': 'slider',
                        'span': np.linspace(0,1.0,11),
                        'value': 0.3,
                        },                            
                }               


class ViewerDockArea(DockArea):
    def __init__(self,parent=None):
        super(ViewerDockArea, self).__init__(parent)                
        self._dock = dict()
        self._viewer = dict()
        self.layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

    def addViewerWidget(self,dim,pos = 'above'):
        # Making dock to put widget inside
        name = self.makeNextNameEntry()
        dock_temp = Dock(name, closable=True,)
        self._dock[name] = dock_temp
        self.addDock(dock_temp,pos,)

        if dim == '1D':
            V = Viewer1DWidget()
        elif dim == '2D':
            V = Viewer2DWidget()
        dock_temp.sigClosed.connect(self.removeViewerWidget)
        # self._viewer.append(V)
        # V.closeEvent()
        dock_temp.addWidget(V)
        if self.parent().isHidden():            
            self.parent().show()
    def removeViewerWidget(self,dock):
        del self._dock[dock.name()]
        
    def quit(self):
        self.close()

    def makeNextNameEntry(self,baseName='Dock'):        
        hasFoundName = False
        i = 0
        while not hasFoundName:
            name = baseName+"_%d" % i
            if not(np.any([name == key for key in list(self._dock.keys())])):
                hasFoundName=True
                return name
            i = i+1        
def restart():
    QCoreApplication.quit()
    status = QProcess.startDetached(sys.executable, sys.argv)
    print(f'Exiting status: {status}')
        #  
def main():
    import sys
    app = QApplication([])
    app = pg.mkQApp("DockArea Example")
    win = QtWidgets.QMainWindow()
    area = ViewerContainer()
    win.setCentralWidget(area)
    win.resize(1000,500)
    win.setWindowTitle('pyqtgraph example: dockarea')
    # tools = ViewerDockArea()
    win.show()
    app.exec()
if __name__=="__main__":
    main()
