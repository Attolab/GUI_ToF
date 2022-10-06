from encodings import normalize_encoding
from pyqtgraph import TableWidget

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QPushButton, QSizePolicy, QToolButton,QMenu,QTableWidget,QCheckBox,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow,QHeaderView)
import numpy as np

import pyqtgraph as pg
from CustomQMenu import *


class CustomTableWidget(QTableWidget):
    removeItem_signal = Signal(int)
    itemSelected_signal = Signal(int,str)
    def __init__(self,parent=None):
        super(CustomTableWidget, self).__init__(parent)
        self.connectSignals()
        # self.check_columnwidth()
    def connectSignals(self):
        # Table connection              
        self.itemSelectionChanged.connect(self.tableItemLeftClicked)

    def get_selectedRows(self):
        return np.flip(np.unique([self.row(item) for item in self.selectedItems()]))

    def tableItemLeftClicked(self,):
        row_sel = self.get_selectedRows()
        for row in np.arange(self.rowCount()):
            if row in row_sel:
                self.itemSelected_signal.emit(row,'selected')
            else:
                self.itemSelected_signal.emit(row,'unselected')

    def removeEntry_table(self,row):
        # Send signal to remove ROI
        self.removeItem_signal.emit(row)            
        # Remove entry in table
        self.removeRow(row)

    def removeSelectedItems_table(self):
        # Remove all selected items
        for row in self.get_selectedRows():
            self.removeEntry_table(row)           

    def clearTable(self):    
        # Remove all items    
        for row in np.flip(np.arange(self.rowCount())):
            self.removeEntry_table(row)   

    ## TO DO######
    def check_columnwidth(self):
        header = self.horizontalHeader()    
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  

class PlotTableWidget(CustomTableWidget):
    checkBox_signal = Signal(bool,int)    
    colorButton_signal = Signal(object,int)
    QMenu_signal = Signal(str)
    def __init__(self,parent=None):
        super(PlotTableWidget, self).__init__(parent)
        # Connect QContextMenu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self,SIGNAL("customContextMenuRequested(QPoint)" ), self.tableItemRightClicked)    
    def check_columnwidth(self):
        header = self.horizontalHeader()    
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  
        # Method to add an entry to the table
    def addEntry(self,name=None,show=True,color = (255,255,255)):
        nRow = self.rowCount()        
        self.insertRow(nRow)
        if not(name):
            name = f'{nRow}'     
        item = QTableWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsEditable)    
        self.setItem(nRow,0,item)
        colorButton_item = pg.ColorButton()
        colorButton_item.setColor(color)
        colorButton_item.sigColorChanged.connect(self.colorButtonTable_changed)
        colorButton_item.sigColorChanged.connect(lambda i, a=nRow:self.colorButtonTable_changed(i, a))
        self.setCellWidget(nRow,1, colorButton_item) 
        item = QCheckBox()
        item.setChecked(show)
        item.stateChanged.connect( lambda i, a=nRow: self.checkBoxTable_changed(i, a) )
        self.setCellWidget(nRow,2, item) 
        self.clearSelection()
        self.setCurrentCell(nRow,1) 
        self.check_columnwidth()
    def getColorButton(self,row):
        # self.colorButton_signal.emit(self.cellWidget(row,1).color(),row)
        return self.cellWidget(row,1).color()
    def colorButtonTable_changed(self,button,row):
        self.colorButton_signal.emit(button.color(),row)
    def checkBoxTable_changed(self,value,row):
        self.checkBox_signal.emit(value != 0,row)
        # Method when user rightclicked on table
    def tableItemRightClicked(self, QPos): 
        sender = self.sender()
        parentPosition = sender.mapToGlobal(QPoint(0, 0))        
        self.Qmenu = CustomQMenu('Menu',)
        self.Qmenu.removeItem_signal.connect(self.removeSelectedItems_table)
        self.Qmenu.clearTable_signal.connect(self.clearTable)
        self.Qmenu.move(parentPosition + QPos)
        self.Qmenu.show()  

    def QMenu_function(self,command):
        self.QMenu_signal.emit(command)    

class ROITableWidget(CustomTableWidget):

    QMenu_signal = Signal(str)
    def __init__(self,parent=None):
        super(ROITableWidget, self).__init__(parent)
        # Connect QContextMenu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self,SIGNAL("customContextMenuRequested(QPoint)" ), self.tableItemRightClicked)    

        # Method to add an entry to the table
    def addEntry(self,name=None,orientation='H',type='LRI'):
        nRow = self.rowCount()        
        self.insertRow(nRow)
        if not(name):
            name = f'{nRow}'          
        if orientation == 'horizontal':
            orientation ='H'
        elif orientation == 'vertical':
            orientation ='V'
        item = QTableWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsEditable)    
        self.setItem(nRow,0,item)
        item = QTableWidgetItem(orientation)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)        
        self.setItem(nRow,1,item)
        self.clearSelection()
        self.setCurrentItem(item)   

        # Method when user rightclicked on table
    def tableItemRightClicked(self, QPos): 
        sender = self.sender()
        parentPosition = sender.mapToGlobal(QPoint(0, 0))        
        self.Qmenu = CustomQMenu('Menu',)
        self.Qmenu.removeItem_signal.connect(self.removeSelectedItems_table)
        self.Qmenu.clearTable_signal.connect(self.clearTable)
        self.ROIMenu = ROIOperationQMenu("Operation")
        self.Qmenu.addMenu(self.ROIMenu)
        self.ROIMenu.QActionOperation_signal.connect(self.QMenu_function)
        self.Qmenu.move(parentPosition + QPos)
        self.Qmenu.show()  

    def QMenu_function(self,command):
        self.QMenu_signal.emit(command)    

class fileSelectionTableWidget(TableWidget):

    QMenu_signal = Signal(str)
    def __init__(self,parent=None):
        super(fileSelectionTableWidget, self).__init__(parent)
        # Connect QContextMenu
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.connect(self,SIGNAL("customContextMenuRequested(QPoint)" ), self.tableItemRightClicked)    
        # Method to add an entry to the table
    def addEntry(self,name=None,orientation='H',type='LRI'):
        nRow = self.rowCount()        
        self.insertRow(nRow)
        if not(name):
            name = f'{nRow}'          
        if orientation == 'horizontal':
            orientation ='H'
        elif orientation == 'vertical':
            orientation ='V'
        item = QTableWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsEditable)    
        self.setItem(nRow,0,item)
        item = QTableWidgetItem(orientation)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)        
        self.setItem(nRow,1,item)
        self.clearSelection()
        self.setCurrentItem(item)   

        # Method when user rightclicked on table
    def tableItemRightClicked(self, QPos): 
        sender = self.sender()
        parentPosition = sender.mapToGlobal(QPoint(0, 0))                
        self.Qmenu = FileSelectionQMenu('Menu',)
        self.Qmenu.removeItem_signal.connect(self.removeSelectedItems_table)
        self.Qmenu.clearTable_signal.connect(self.clearTable)
        self.Qmenu.move(parentPosition + QPos)
        self.Qmenu.show()  

    def QMenu_function(self,command):
        self.QMenu_signal.emit(command)   


class imageSelectionTableWidget(QTableWidget):
    QMenu_signal = Signal(str)
    def __init__(self,parent=None):
        super(imageSelectionTableWidget, self).__init__(parent)
        # Connect QContextMenu
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.connect(self,SIGNAL("customContextMenuRequested(QPoint)" ), self.tableItemRightClicked)    
        # Method to add an entry to the table
    
    def addEntry(self,index=0,parameter=0):
        nRow = self.rowCount()        
        self.insertRow(nRow)
        item = QTableWidgetItem(index)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)        
        self.setItem(nRow,0,item)
        item = QTableWidgetItem(parameter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)        
        self.setItem(nRow,1,item)
        self.clearSelection()
        self.setCurrentItem(item)   

        # Method when user rightclicked on table
    def tableItemRightClicked(self, QPos): 
        sender = self.sender()
        parentPosition = sender.mapToGlobal(QPoint(0, 0))                
        self.Qmenu = FileSelectionQMenu('Menu',)
        self.Qmenu.removeItem_signal.connect(self.removeSelectedItems_table)
        self.Qmenu.clearTable_signal.connect(self.clearTable)
        self.Qmenu.move(parentPosition + QPos)
        self.Qmenu.show()  

    def QMenu_function(self,command):
        self.QMenu_signal.emit(command)             

def main():
    import sys
    app = QApplication([])
    # test = ROITableWidget()
    test = fileSelectionTableWidget()
    test.addEntry('test')
    test.show()
    app.exec()
if __name__=="__main__":
    main()
