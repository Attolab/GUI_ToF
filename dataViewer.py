from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtCore import Qt,Signal
import numpy as np
class DAV_TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(DAV_TableModel, self).__init__()
        self._data = data
        # self.dataChanged.connect(self.test)
    def test(self,a,b):
        print('da')

    def data(self, index, role):
        match role:
            case Qt.DisplayRole:
                # row = index.row()
                # col = index.column()                                
                value = self._data[index.row(), index.column()]
                return str(value)                
            # case Qt.FontRole:
            #     a = 0
            #     A = QtGui.QFont()
            #     A.setBold(True)
            #     return A
            # case Qt.BackgroundRole:
            #     a = 0
            #     return QtGui.QBrush(Qt.red)                
            # case Qt.TextAlignmentRole:
            #     a = 0
            #     return int(Qt.AlignRight | Qt.AlignVCenter)   
            # case Qt.CheckStateRole:
            #     a = 0
            #     return Qt.Checked

    def rowCount(self, index):
        return self._data.shape[0]
    def columnCount(self, index):
        return self._data.shape[1]
    # def flags(self, index):
    #     if not index.isValid():
    #         return 0
    #     return Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable 
    #     # | QtCore.QAbstractTableModel.flags(index)


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == Qt.EditRole:
            self._data[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        # elif role == Qt.CheckStateRole:
        #     a = 1
        #     return True
        return False
        
        # item = self.getItem(index)
        # result = item.setData(index.column(), value)

        # if result:


    # def headerData(self, section, orientation, role):
    #     # section is the index of the column/row.
    #     if role == Qt.DisplayRole:
    #         if orientation == Qt.Horizontal:
    #             return str(self._data.columns[section])

    #         if orientation == Qt.Vertical:
    #             return str(self._data.index[section])
# class DAV_TableView(QtWidgets.QTableView):



# class DAV_TableView(QtWidgets.QTableView):
class DataViewer(QtWidgets.QTabWidget):
    closeTab_signal = Signal(int)
    def __init__(self,parent=None,name='TestPanel'):
        super(DataViewer, self).__init__(parent)                
        self.setObjectName(name)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.name = name
        self._tables = {}
        self.connectSignals()

    def setTab(self,item):
        self.setCurrentIndex(self.indexOf(item))

    def connectSignals(self):    
        self.tabCloseRequested.connect(self.closeTab_function)  

    def closeTab_fromWidget_function(self,item):
        self.closeTab_function(self.indexOf(item))

    def closeTab_function(self,index):
        self.closeTab_signal.emit(index)
        for key,values in self._tables.items():
            if index == self.indexOf(values):
                self._tables.pop(key)
                self.removeTab(index)
                return


    def setTab_fromWidget_function(self,item):
        widget = item.get_widgetDataVariableItem()
        if self.indexOf(widget) == -1:
            self.insertTab(widget,item.text(),self.count())
        self.setTab(widget) 
        self.showTab()

    def showTab(self):
        if not(self.isVisible()):
            self.show()
        self.activateWindow()    

    def makeTab(self,key,data):
        if key not in self._tables.keys():
            dShape = data.shape
            if len(dShape) > 2:
                widget = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                [layout.addWidget(self.makeTable(data[i]),) for i in np.arange(dShape[0])]
                widget.setLayout(layout)
            else:
                widget = self.makeTable(data)             
            area = QtWidgets.QScrollArea()
            area.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
            area.setAlignment(Qt.AlignVCenter)
            # area.setLayout(QtWidgets.QVBoxLayout())
            # area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy(2))
            area.setWidget(widget)   
            area.setWidgetResizable(True)
            self._tables[key] = area
            currentIndex = self.count()
            self.insertTab(currentIndex,self._tables[key],key[-1],)
            self.setTabToolTip(currentIndex,str(key))
            print('Displaying data')
        else:
            self.setTab(self._tables[key])
        self.activateWindow()    

    def makeTable(self,data):
        model = DAV_TableModel(data)
        table = QtWidgets.QTableView()
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        table.setModel(model)
        return table

    def getWidgetIndex(self):
        return [self.indexOf(item) for item in self._tables.values()]
# class MainWindow(QtWidgets.QMainWindow):

#     def __init__(self):
#         super().__init__()

#         self.table = QtWidgets.QTableView()

#         data = np.array([
#           [1.52, 9, 2],
#           [1, 0, -1],
#           [3, 5, 2],
#           [3, 3, 2],
#           [5, 8, 9],
#         ])

#         self.model = DAV_TableModel(data)
#         self.tabwidget = DataViewer()
#         self.tabwidget.insertTab(self.tabwidget.count(),self.table,'test')
#         self.tabwidget.insertTab(self.tabwidget.count(),self.table2,'test2')
#         self.table.setModel(self.model)
#         self.setCentralWidget(self.tabwidget)

def main():
    import numpy as np
    import sys
    app=QtWidgets.QApplication(sys.argv)
    # window=QtWidgets.QMainWindow()
    tabwidget = DataViewer()




    data = np.zeros(shape=(10,50,50))

    tabwidget.makeTab('test',data)
    data = np.array([
        [1.52, 9, 2],
        [1, 0, -1],
        [3, 5, 2],
        [3, 3, 2],
        [5, 8, 9],
    ])
    tabwidget.makeTab('testsda',data)

    # tabwidget.insertTab(tabwidget.count(),table,'test')
    # window.setCentralWidget(tabwidget)
    tabwidget.show()
    app.exec()        

if __name__=="__main__":
    main()
