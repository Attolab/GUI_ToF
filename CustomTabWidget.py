from PySide6 import QtGui,QtCore,QtWidgets

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,SIGNAL,
    QSize, QTime, QUrl, Qt,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QPushButton, QSizePolicy, QToolButton,QMenu,QTableWidget,QCheckBox,
    QVBoxLayout, QWidget,QTableWidgetItem,QFileDialog,QDockWidget,QMainWindow,QHeaderView)

from CustomTableWidget import CustomTableWidget,fileSelectionTableWidget
from pyqtgraph import DataTreeWidget

class WorkspaceTabWidget(QtWidgets.QTabWidget):
    newWorkspace_signal = Signal(object)
    """Tab Widget that that can have new tabs easily added to it."""
    def __init__(self,parent=None,name = 'TabWidget'):
        super(WorkspaceTabWidget, self).__init__(parent) 
        self.setObjectName(name)
        self.plusbutton = QtWidgets.QToolButton()
        icon = QtGui.QIcon.fromTheme("window-new")
        self.plusbutton.setIcon(icon)
        self.setCornerWidget(self.plusbutton,corner = QtGui.Qt.TopRightCorner)

        # Properties
        self.setMovable(True)
        self.setTabsClosable(False)
        self.plusbutton.pressed.connect(self.addNewTab)
        self.tabCloseRequested.connect(self.removeTab)

    def addNewTab(self,name = None,data = None):        
        if not name:
            name = str(self.count())              

        Q = QWidget()
        L = QVBoxLayout()
        Q.setLayout(L)
        workspace_tableWidget = QTableWidget()
        workspace_tableWidget.setColumnCount(3)
        workspace_tableWidget.head
        workspace_tableWidget.setItem()
        name = QTableWidgetItem('name')
        desc = QTableWidgetItem("shape=%s dtype=%s" % (data.shape, data.dtype))
        typeStr = QTableWidgetItem(type(data).__name__)
        workspace_tableWidget.
        if data is not None:
            workspace_tableWidget.setData(data)
        L.addWidget(workspace_tableWidget)
        self.addTab(Q,name)
        # self.emit(Q)


def main():
    import sys
    import numpy as np
    app = QtWidgets.QApplication(['test'])
    tof = WorkspaceTabWidget(name='Test')
    tof.addNewTab('Global',np.ones((1,5)))    
    # tof.addTab(QtWidgets.QTableWidget(),'Global')
    # tof.addTab(QtWidgets.QTableWidget(),'1')
    tof.show()
    app.exec()

if __name__=="__main__":
    main()


