
from ast import Param
from ctypes import alignment
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
from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree import ParameterTree
from signal_processing_toolbox import SignalProcessingToolbox
from CustomQMenu import FileSelectionQMenu
import sys, traceback
import h5py
import numpy as np
import os
from CustomDataTreeWidget import CustomDataTreeWidget
from pyqtgraph import DataTreeWidget

from viewer1D_widget import Viewer1DWidget
from viewer2D_widget import Viewer2DWidget
#for i in *.ui; do pyside6-uic ${i%.ui}.ui > ${i%.ui}_ui.py; done


class ViewerContainer(QWidget):
    showViewer_signal = Signal()
    addViewerWidget_signal = Signal(object)
    def __init__(self, parent=None):
            super().__init__(parent,)
            self.setupUI()
            self.connectSignals()

    def setupUI(self):
        w1 = pg.LayoutWidget(self)
        w1 = QHBoxLayout(self)
        self._browser = ViewerBrowser(self)
        self._browser.setWindowFlag(Qt.WindowStaysOnTopHint)
        # self._browser.setAlignment()
        self._dockArea = ViewerDockArea(self)
        w1.addWidget(self._browser,)
        w1.insertWidget(-1,self._dockArea,alignment=Qt.AlignRight)
        self._browser.addViewer_signal.connect(self._dockArea.addViewerWidget)

    def connectSignals(self):
        self.addViewerWidget_signal.connect(self._dockArea.addViewerWidget)

    def browser(self):
        return self._browser
    def dockArea(self):
        return self._dockArea




class ViewerBrowser(QWidget):
    addViewer_signal = Signal(object)
    def __init__(self, parent=None):
            super().__init__(parent,)
            self.setupUI()

    def setupUI(self):
        w1 = pg.LayoutWidget(self)
        label = QtWidgets.QLabel(""" -- DockArea Example -- 
        This window has 6 Dock widgets in it. Each dock can be dragged
        by its title bar to occupy a different space within the window 
        but note that one dock has its title bar hidden). Additionally,
        the borders between docks may be dragged to resize. Docks that are dragged on top
        of one another are stacked in a tabbed layout. Double-click a dock title
        bar to place it in its own window.
        """)
        saveBtn = QtWidgets.QPushButton('Save dock state')
        restoreBtn = QtWidgets.QPushButton('Restore dock state')
        restoreBtn.setEnabled(False)
        addViewerBtn = QtWidgets.QToolButton()
        tool_btn_menu= QMenu(self)
        self.connect(tool_btn_menu.addAction("Add Viewer 1D"),SIGNAL("triggered()"), self.addViewer1D) 
        self.connect(tool_btn_menu.addAction("Add Viewer 2D"),SIGNAL("triggered()"), self.addViewer2D) 
        addViewerBtn.setMenu(tool_btn_menu)
        addViewerBtn.setDefaultAction(tool_btn_menu.actions()[1])        
        w1.addWidget(label, row=0, col=0)
        w1.addWidget(saveBtn, row=1, col=0)
        w1.addWidget(restoreBtn, row=1, col=1)
        w1.addWidget(addViewerBtn, row=3, col=0)

    def addViewer(self,dim = '1D'):
        self.addViewer_signal.emit(dim)
    def addViewer1D(self,):
        self.addViewer_signal.emit('1D')
    def addViewer2D(self,dim = '1D'):
        self.addViewer_signal.emit('2D')

class ViewerDockArea(DockArea):
    def __init__(self,parent=None):
        super(ViewerDockArea, self).__init__(parent)                
        self._dock = dict()
        self._viewer = dict()
        self.layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

    def addViewerWidget(self,dim):
        # area = self._dock['viewer_dock'].widget()
        d2 = Dock("Dock2 - Console", closable=True,)
        self.addDock(d2,'above',)
        if dim == '1D':
            V = Viewer1DWidget()
        elif dim == '2D':
            V = Viewer2DWidget()
        d2.sigClosed.connect(self.test)
        # self._viewer.append(V)
        # V.closeEvent()
        d2.addWidget(V)
        if self._dock['viewer_dock'].isHidden():            
            self._dock['viewer_dock'].show()
    def test(self,p):
        a = 1
    def quit(self):
        self.close()
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
