from cmath import nan
from PySide6.QtCore import (QSettings,QFileInfo,Signal)
from PySide6 import QtCore
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QCloseEvent,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,QPen)
from PySide6.QtWidgets import (QApplication, QGraphicsEllipseItem,QGraphicsLineItem, QPushButton, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow)
from VMI_toolbox_ui import Ui_VMI_toolbox_panel
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
from widget_manipulation_class import WidgetDataExtraction
import json
def value_is_valid(val):
    if isinstance(val, QPixmap):
        return not val.isNull()
    return True

def restore(settings):
    finfo = QtCore.QFileInfo(settings.fileName())
    if finfo.exists() and finfo.isFile():
        for w in QApplication.allWidgets():
            if w.objectName() and not w.objectName().startswith("qt_"):
                mo = w.metaObject()
                settings.beginGroup(w.objectName())
                for i in range( mo.propertyCount(), mo.propertyOffset()-1, -1):
                    prop = mo.property(i)
                    name = prop.name()
                    last_value = w.property(name)
                    key = "{}/{}".format(w.objectName(), name)
                    try:
                        if not settings.contains(key):
                            continue
                        val = settings.value(key, type=type(last_value),)
                        if (
                            val != last_value
                            and value_is_valid(val)
                            and prop.isValid()
                            and prop.isWritable()
                        ):
                            w.setProperty(name, val)
                    except:
                        pass
                settings.endGroup()

def save(settings):
    for w in QApplication.allWidgets():
        if w.objectName() and not w.objectName().startswith("qt_"):
            settings.beginGroup(w.objectName())
            mo = w.metaObject()
            for i in range( mo.propertyCount(), mo.propertyOffset()-1, -1):
                prop = mo.property(i)
                name = prop.name()
                key = "{}/{}".format(w.objectName(), name)
                val = w.property(name)
                if value_is_valid(val) and prop.isValid() and prop.isWritable():
                    settings.setValue(key, w.property(name))
            settings.endGroup()     


class VMIToolBox(Ui_VMI_toolbox_panel,QWidget):
    settings = QSettings("gui.ini", QSettings.IniFormat)
    sendParameters_signal = Signal(object)
    def __init__(self, *args, **kwargs):
        super(VMIToolBox, self).__init__(*args, **kwargs)
        #Load UI
        self.setupUi(self)
        self.widget_extraction = WidgetDataExtraction(self,self.makeList_QWidget())
        self.item_list = self.widget_extraction.extractValues()
        # self.widget_extraction.initializeValues(item_list)
        # self.settings = QSettings("gui.ini", QSettings.IniFormat)
        # restore(self.settings)
        # #Initialize parameters
        
        self.loadOldParameters()
        self.connectSignals()

    def closeEvent(self, event: QCloseEvent) -> None:
        # save(self.settings)
        super().closeEvent(event)

    def loadOldParameters(self):
        print('Loading old parameters')
        try:
            self.widget_extraction.initializeValues(json.load(open("VMIToolbox_settings.txt")))
        except Exception as e:
            print(e)

    def connectSignals(self):
        self.go_pushButton.pressed.connect(self.launchCalc)

    def launchCalc(self):
        print('I got pressed')
        self.collectParameters()
        self.saveParameters()
        self.sendParameters()

    def collectParameters(self):
        print('Collecting GUI state')
        self.parameters = self.widget_extraction.extractValues()

    def saveParameters(self):
        json.dump(self.widget_extraction.extractValues(), open("VMIToolbox_settings.txt",'w'))
        print('Saving GUI state')

    def sendParameters(self):        
        print('Sending GUI state')
        self.sendParameters_signal.emit(self.widget_extraction.extractValues())

    def getParameters(self):
        return self.widget_extraction.extractValues()

      
    def makeList_QWidget(self):                
        return['dataSelection_lineEdit',
                'dataSorting_comboBox',
                'dataStacking_comboBox',
                'Rmax_doubleSpinBox',         
                'Rmin_doubleSpinBox',
                'shapeFilter_comboBox',
                'angularBins_spinBox',
                'imageBins_spinBox',
                'radialBins_spinBox',
                'abelInversion_comboBox',
                'abelSmooth_doubleSpinBox',
                'abelSymmetrize_checkBox',
                'abelLegendre_spinBox',
                'angularDistributions_checkBox',
                'radialDistributions_checkBox',
                'angularContour_checkBox',
                'radialContour_checkBox',
                'FT_window_comboBox',
                'FT_zeropadding_comboBox',
                'FT_zeropadding_spinBox',
                'FT_zeropaddingpower2_spinBox',
                'saveOutput_checkBox',
                'showOutput_checkBox',                                          
                        ]


def main():
    import sys
    app = QApplication([])
    QtCore.QCoreApplication.setOrganizationName("Eyllanesc")
    QtCore.QCoreApplication.setOrganizationDomain("eyllanesc.com")
    QtCore.QCoreApplication.setApplicationName("MyApp")    
    tof = VMIToolBox()
    tof.show()
    # sys.exit(app.exec())
    app.exec()

if __name__=="__main__":
    main()