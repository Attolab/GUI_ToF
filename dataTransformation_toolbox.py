
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QTreeWidget,QTreeWidgetItem,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow,QHeaderView)
from CustomDataTreeWidget_ui import Ui_CustomDataTreeWidget
from CustomTableWidget import CustomTableWidget,fileSelectionTableWidget
from pyqtgraph import DataTreeWidget
from pyqtgraph.parametertree import Parameter

import numpy as np
from dataTransformation_toolbox_ui import Ui_dataTransformationToolbox


class DataTransformationWidget(Ui_dataTransformationToolbox,QWidget):

    def __init__(self,parent = None,):
        super(DataTransformationWidget, self).__init__(parent)         
        self.setupUi(self)
        self.initializeParameterTree()

        self.connectSignals()


    def initializeParameterTree(self):
        # Create Parameters
        self._operationList = Parameter.create(name='Operation list',type='group',removable=True,showTop = False)
        self.operationList_parameterTree.setParameters(self._operationList)
        self.operationList_parameterTree.setHeaderHidden(True)
    def updateOperationList(self):
        print('Update List')


    def addOperation(self,operation_parameter):
        self._operationList.addChild(operation_parameter)
        # self._operationList.insertChild(0,operation_parameter)
        self.updateOperationList()
    def moveOperationUp(self):
        topLevel = self.operationList_parameterTree.topLevelItem(0)
        parent = self.operationList_parameterTree.currentItem().parent()
        if topLevel == parent:
            start_row = self.operationList_parameterTree.currentIndex().row()    
            if start_row > 0:
                end_row = start_row-1
                child = self._operationList.children()[start_row]
                item = self.operationList_parameterTree.currentItem()
                self._operationList.removeChild(child)
                self._operationList.insertChild(end_row,child)
                self.operationList_parameterTree.setCurrentItem(child.makeTreeItem(0))
    def moveOperationDown(self):
        topLevel = self.operationList_parameterTree.topLevelItem(0)
        parent = self.operationList_parameterTree.currentItem().parent()
        if topLevel == parent:        
            start_row = self.operationList_parameterTree.currentIndex().row()
            if start_row < len(self._operationList.children())-1:
                end_row = start_row + 1
                child = self._operationList.children()[start_row]
                self._operationList.removeChild(child)
                self._operationList.insertChild(end_row,child)
                item = self.operationList_parameterTree.currentItem()
                self.operationList_parameterTree.setCurrentItem(item)            
            # children[start_row],children[end_row] = children[end_row],children[start_row]

            # self._operationList.addChildren(children)
        # item = self.operationList_parameterTree.currentItem()
        # if bool(item) & (self.operationList_parameterTree.currentIndex().row() > 0):
        #     self._operationList.removeChild()
        #     self._operationList.addChildren
        #     # isExpanded = item.isExpanded()            
        #     parent = item.parent()
        #     index = parent.indexOfChild(item)
        #     child = parent.takeChild(index)           
        #     parent.insertChild(index-1,child)
        #     # child.setExpanded(isExpanded)
        #     self.operationList_parameterTree.setCurrentItem(child)
    # def moveOperationDown(self):
    #     item = self.operationList_parameterTree.currentItem()
    #     if bool(item) & (self.operationList_parameterTree.currentIndex().row() < len(self._operationList.children())-1):
    #         parent = item.parent()
    #         index = parent.indexOfChild(item)
    #         child = parent.takeChild(index)
    #         parent.insertChild(index+1,child)
    #         self.operationList_parameterTree.setCurrentItem(child)

    def connectSignals(self):
        self.makeOperation_pushButton.pressed.connect(self.makeOperation)
        self.operactionActionDown_pushButton.pressed.connect(self.moveOperationDown)
        self.operactionActionUp_pushButton.pressed.connect(self.moveOperationUp)        
        # self._operationList.sigChildRemoved(self.updateOperationList)
        self.refreshOperationList_pushButton.pressed.connect(self.clearOperationTree)

    def clearOperationTree(self):
        self.operationList_parameterTree.clear()
        self.initializeParameterTree()

    def getOperationList(self):
        a = 1
    def makeOperation(self):
        index = self.tabWidget.currentIndex()
        if index == 0:
            self.makeBasicOperation()
        if index == 1:
            self.makeFilterOperation()
        if index == 2:
            self.makeInterpolationOperation()      
                              
    def makeOperationName(self,operationType):           
        return f'{operationType}_{len(self._operationList.children())}'
    def makeBasicOperation(self):
        print('Making basic operation:')
        name = self.basicOperationChoice_comboBox.currentText()
        value = self.basicOperation_doubleSpinBox.value()
        operation_params =  {
                'operationType':{
                    'title': 'operationType',
                    'type': 'list',
                    'limits': ['Add','Substract','Multiply','Divide'],
                    'value': name,
                    },               
                'operationFactor': {
                    'title':'operationFactor',                                        
                    'type': 'float',
                    'value': value,
                    'editable':True,
                    },    
                'status': {
                    'title':'Status',                                        
                    'type': 'bool',
                    'value': True,
                    'readonly':True,                                        
                    },      
        }
        self.addOperation(Parameter.create(name=self.makeOperationName('Basic'), type='group',expanded = True,children = operation_params,removable = True,renamable=False))        
    

    def makeInterpolationOperation(self):
        print('Making interpolation operation:')
    def makeFilterOperation(self):
        print('Making filter:')
        name = self.basicOperationChoice_comboBox.currentText()
        name = self.basicOperationChoice_comboBox.currentText()
        value = self.basicOperation_doubleSpinBox.value()
        operation_params =  {
                'operationType':{
                    'title': 'operationType',
                    'type': 'list',
                    'limits': ['Add','Substract','Multiply','Divide'],
                    'value': name,
                    },               
                'operationFactor': {
                    'title':'operationFactor',                                        
                    'type': 'float',
                    'value': value,
                    'editable':True,
                    },    
                'status': {
                    'title':'Status',                                        
                    'type': 'bool',
                    'value': True,
                    'readonly':True,                                        
                    },      
        }
        self.addOperation(Parameter.create(name=self.makeOperationName('Filter'), type='group',expanded = True,children = operation_params,removable = True,renamable=False))        
        
    # def makeBasicOperation(self):
    #     print('Making basic operation:')
    #     name = self.basicOperationChoice_comboBox.currentText()
    #     value = self.basicOperation_doubleSpinBox.value()
    #     operation_params =  {
    #             'operationType':{
    #                 'title': 'operationType',
    #                 'type': 'list',
    #                 'limits': ['Add','Substract','Multiply','Divide'],
    #                 # 'editable':True,
    #                 # 'readonly':True,
    #                 },               
    #             'operationFactor': {
    #                 'title':'operationFactor',                                        
    #                 'type': 'float',
    #                 'value': value,
    #                 'editable':True,
    #                 'readonly':True,                                        
    #                 },    
    #             'status': {
    #                 'title':'Status',                                        
    #                 'type': 'bool',
    #                 'value': True,
    #                 'editable':False,
    #                 'readonly':True,                                        
    #                 },      
    #     }
    #     self.makeOperation(Parameter.create(name=self.makeOperationName('Basic'), type='group',expanded = False,children = operation_params,removable = True,renamable=False))        



def main():
    import numpy as np

    app = QApplication(['test'])
    tof = DataTransformationWidget()
    tof.show()
    app.exec()

if __name__=="__main__":
    main()


