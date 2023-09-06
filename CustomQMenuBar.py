
from encodings import normalize_encoding
from pyqtgraph import TableWidget

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QPushButton, QSizePolicy, QToolButton,QMenu,QTableWidget,QCheckBox,QMenuBar,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow,QHeaderView)
import numpy as np

import pyqtgraph as pg



class CustomQMenuBar(QMenuBar):
    removeItem_signal = Signal()
    clearTable_signal = Signal()
    def __init__(self,parent=None):
        super(CustomQMenuBar, self).__init__(parent)
        self.menuFile = QMenu('File')
        self.addMenu()
        self.removeItem_action = QAction("Remove Item(s)",self)
        self.removeItem_action.triggered.connect(self.removeItem_signal.emit)

        self.clearTable_action = QAction("Clear all",self)
        self.clearTable_action.triggered.connect(self.clearTable_signal.emit)

        self.addAction(self.removeItem_action)
        self.addAction(self.clearTable_action)        


class functionOperationQMenu(QMenu):
    findPeak_signal = Signal()
    doFFT_signal = Signal()
    def __init__(self,parent=None):
        super(CustomQMenu, self).__init__(parent)
        self.findPeak_action = QAction("Find Peak(s)",self)
        self.findPeak_action.triggered.connect(self.findPeak_signal.emit)

        self.doFFT_action = QAction("FFT",self)
        self.doFFT_action.triggered.connect(self.doFFT_signal.emit)

        self.addAction(self.doFFT_action)
        self.addAction(self.findPeak_action)     



class ROIOperationQMenu(QMenu):
    QActionOperation_signal = Signal(str)
    def __init__(self,parent=None):
        super(ROIOperationQMenu, self).__init__(parent)

        self.COM_action = QAction("COM",self)
        self.sum_action = QAction("Sum",self)
        self.findMax_action = QAction("Max",self)
        self.findMin_action = QAction("Min",self)

        self.COM_action.setData('COM')
        self.sum_action.setData('Sum')
        self.findMax_action.setData('Max')
        self.findMin_action.setData('Min')

        self.COM_action.triggered.connect(self.QAction_function)
        self.sum_action.triggered.connect(self.QAction_function)
        self.findMax_action.triggered.connect(self.QAction_function)
        self.findMin_action.triggered.connect(self.QAction_function)

        self.addAction(self.COM_action)
        self.addAction(self.sum_action)
        self.addAction(self.findMax_action)
        self.addAction(self.findMin_action)      


    def QAction_function(self):
        self.QActionOperation_signal.emit(self.sender().data())    