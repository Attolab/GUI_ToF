
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QShortcut,
    QFont, QFontDatabase, QGradient, QIcon,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QTreeWidget,QTreeWidgetItem,QStyledItemDelegate,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow,QHeaderView)
from CustomDataTreeWidget_ui import Ui_CustomDataTreeWidget
import numpy as np
from CustomQMenu import DataSelectionQMenu
from editableTreeModel import TreeModel,NoEditDelegate
from dataContainer import DataContainer
from dataViewer import DataViewer
import copy
class CustomDataTreeWidget(Ui_CustomDataTreeWidget,QWidget):
    showVariable_signal = Signal(object,object)
    operation_signal = Signal(object)
    removeSelectedRows_signal = Signal(object)
    def __init__(self,parent = None, data = None):
        super(CustomDataTreeWidget, self).__init__(parent)         
        self.setupUi(self)
        self.setWindowTitle(QCoreApplication.translate("CustomDataTreeWidget", u"Data Browser", None))        
        self.setupWindows()

        self.DC = DataContainer() # Class containing data stored as dic, share similar adress structure with nodes structure of treeModel         
        self.DW = DataViewer() # QTabwidget that contains a tableview to display/edit data
        # Initializing tree view and model
        headers = ["Name", "Type", "Descriptions"]         
        self.model = TreeModel(headers, [])
        # delegate = NoEditDelegate() # Custom delegate to make 
        # self.treeView.setItemDelegate(delegate)
        self.treeView.setModel(self.model)
        self.treeView.expandAll()
        self.treeView.resizeColumnToContents(0)
        self.makeBinding()
        self.connectSignals()  
    def connectSignals(self):
        self.add_pushButton.pressed.connect(self.addEntry_pushButton)
        self.treeView.doubleClicked.connect(self.doubleClicked_treeWidget_function)
        self.removeSelectedRows_signal.connect(self.model.removeNodesEntry)
        self.model.nodeKeyChanged_signal.connect(self.DC.updateEntry)
        self.model.nodeKeyRemoved_signal.connect(self.DC.removeEntry)
        # self.model.sendAdress_signal.connect(self.DC.showData)
        self.showVariable_signal.connect(self.DW.makeTab)
    def makeBinding(self):
        self.shortcut = []
        self.shortcut.append(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_V),self.treeView).activated.connect(self.pasteSelectedItems))
        self.shortcut.append(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C),self.treeView).activated.connect(self.storeSelectedItemsKeys))
        self.shortcut.append(QShortcut(QKeySequence(Qt.Key_Delete),self.treeView).activated.connect(self.removeSelectedItems))

    def setupWindows(self):
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.connect(self.treeView,SIGNAL("customContextMenuRequested(QPoint)" ), self.listItemRightClicked)        
        self.dataTreeView_QMenu = DataSelectionQMenu(selection=bool(self.treeView.selectedIndexes()))  
        self.dataTreeView_QMenu.QActionOperation_signal.connect(self.readQMenuSignal)        

    def storeData(self,data):
        data = self.extractDictEntry(data.value())
        self.addData(data)

    def extractDictEntry(self,entry):
        data = {}
        for key,value in entry.items():
            if type(value) is dict:
                data[key] = self.extractDictEntry(value)
            else:
                # self._data[key] = value
                data[key] = value
        return data

    def listItemRightClicked(self,QPos):
        self.dataTreeView_QMenu.updateSelection(self.treeView.selectedIndexes())
        parentPosition = self.treeView.mapToGlobal(QPoint(0, 0))        
        self.dataTreeView_QMenu.move(parentPosition + QPos)
        self.dataTreeView_QMenu.show() 


    def addEntry_pushButton(self):
        data = {'Type':{"Project A": np.ones((5,1)),
                "Project B": np.zeros((5,5)),
                "Project C": np.ones((1,5)),
                "Project D": np.ones((2,5,5))}}   
        data = {'test':data}
        self.addData(data)

    def addData(self,data,hideRoot=True):  
        self.DC.addData(data)
        self.model.buildTree(data,self.model.rootItem,hideRoot = hideRoot)        
        self.treeView.expandAll()
        self.treeView.resizeColumnToContents(0)        
        
    def doubleClicked_treeWidget_function(self,index):
        if self.DW.isHidden():
            self.DW.show()
        # #Find items
        item = self.model.getItem(index,)
        # for child in item.childItems:
        if not(item.childItems):
            key = self.model.getAdress(self.model.getItem(index,))    
            data = self.DC.data(key)
            self.showVariable_signal.emit(key,data)

            print(data)
        print(self.model.getItem(index).data(0))        
 ################################################## Read Context menu ##########################################    
    def readQMenuSignal(self,input):
        print(input)
        if input  == 'copy':
            self.copySelectedItems()
        elif input  == 'rename':
            self.renameItem()            
        elif input  == 'ExtractMBES':
            self.getData('MBES','store')            
        elif input == 'SaveData':
            print('Saving data... or not')
        elif input == 'removeItems':
            self.removeSelectedItems()
        elif input == 'clearList':                        
            self.clearAll()

#  ################################################## Functions ##########################################    

    def getSelectedItems(self):
        selected_items = []
        [selected_items.append(self.model.getItem(index)) for index in self.treeView.selectedIndexes() 
                                                                if self.model.getItem(index) not in selected_items]
        return selected_items

    def storeSelectedItemsKeys(self):
        self.storedItems = self.getSelectedItems()

    def pasteSelectedItems(self):
        [self.copyItem(item) for item in self.storedItems]
        
    def copySelectedItems(self):        
        [self.copyItem(item) for item in self.getSelectedItems()]
        
    def getSelectedKeys(self,item):
        # Store keys of item and of its children
        for k,v in self.model.nodes.items():
            if item == v:
                break
        if item.childItems:
            for item_c in item.childItems:
                self.getSelectedKeys(item_c)            
        else:
            self.selected_keys.append((k,item))

    def copyItem(self,item):
        # Copy item and its children
        for k,v in self.model.nodes.items():
            if item == v:
                break
        key_pos = item.getDepth()-1
        new_key = k[key_pos]+'_copy'
        self.selected_keys = []
        self.getSelectedKeys(item)
        temp_dicList = []
        for k_sel,item_sel in self.selected_keys:
            key_dic = (new_key,) + k_sel[key_pos+1::1] #Prepare dic entry
            data = copy.deepcopy(self.DC.data(k_sel))
            temp_dicList.append(self.makeDict(key_dic[-1::-1],data)) #Make dic
        combined = {}
        for record in temp_dicList: #Reorder dic
            self.combine_into(record, combined)     
        self.addData(combined)


    def combine_into(self,d: dict, combined: dict) -> None:
        #Merge nested dics with similar keys
        for k, v in d.items():
            if isinstance(v, dict):
                self.combine_into(v, combined.setdefault(k, {}))
            else:
                combined[k] = v


    def makeDict(self,tuple,data):
        # Fast build of dic from a tuple
        tree_dict = data
        for key in tuple:
            tree_dict = {key: tree_dict}        
        return tree_dict

    def removeSelectedItems(self):
        # Remove selected items from tree (and its childs)
        while self.treeView.selectedIndexes():
            index = self.treeView.selectedIndexes()[0]
            item = self.model.getItem(index)
            self.removeSelectedRows_signal.emit(item)
            self.model.removeRow(index.row(),index.parent())


    def clearAll(self):
        self.model.clear()
        self.DC.clearData()

from PySide6 import QtCore
class DAV_TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(DAV_TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Note: self._data[index.row()][index.column()] will also work
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

def main():
    import numpy as np
    data = {'Type':{"Project A": np.ones((5,1)),
            "Project B": np.zeros((5,1)),
            "Project C": np.ones((5,1))}}    
    import sys
    app = QApplication(['test'])
    tof = CustomDataTreeWidget(data = data)

    tof.show()
    app.exec()

if __name__=="__main__":
    main()


