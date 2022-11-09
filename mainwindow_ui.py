# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(491, 328)
        MainWindow.setDockNestingEnabled(True)
        self.menuFile_restartAction = QAction(MainWindow)
        self.menuFile_restartAction.setObjectName(u"menuFile_restartAction")
        self.actionMain_close = QAction(MainWindow)
        self.actionMain_close.setObjectName(u"actionMain_close")
        self.actionMain_restart = QAction(MainWindow)
        self.actionMain_restart.setObjectName(u"actionMain_restart")
        self.actiong = QAction(MainWindow)
        self.actiong.setObjectName(u"actiong")
        self.actionFile_load = QAction(MainWindow)
        self.actionFile_load.setObjectName(u"actionFile_load")
        self.actionMain_restoreState = QAction(MainWindow)
        self.actionMain_restoreState.setObjectName(u"actionMain_restoreState")
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionData = QAction(MainWindow)
        self.actionData.setObjectName(u"actionData")
        self.actionViewer1D_create = QAction(MainWindow)
        self.actionViewer1D_create.setObjectName(u"actionViewer1D_create")
        self.actionViewer2D_create = QAction(MainWindow)
        self.actionViewer2D_create.setObjectName(u"actionViewer2D_create")
        self.actionViewer_close = QAction(MainWindow)
        self.actionViewer_close.setObjectName(u"actionViewer_close")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionToF = QAction(MainWindow)
        self.actionToF.setObjectName(u"actionToF")
        self.actionVMI = QAction(MainWindow)
        self.actionVMI.setObjectName(u"actionVMI")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 491, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSession = QMenu(self.menuFile)
        self.menuSession.setObjectName(u"menuSession")
        self.menuRecent = QMenu(self.menuSession)
        self.menuRecent.setObjectName(u"menuRecent")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuViewer = QMenu(self.menubar)
        self.menuViewer.setObjectName(u"menuViewer")
        self.menuCreate = QMenu(self.menuViewer)
        self.menuCreate.setObjectName(u"menuCreate")
        self.menuOpened_Viewer = QMenu(self.menuViewer)
        self.menuOpened_Viewer.setObjectName(u"menuOpened_Viewer")
        self.menuWidgets = QMenu(self.menubar)
        self.menuWidgets.setObjectName(u"menuWidgets")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWidgets.menuAction())
        self.menubar.addAction(self.menuViewer.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menuFile.addAction(self.actionFile_load)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuSession.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionMain_restart)
        self.menuFile.addAction(self.actionMain_close)
        self.menuFile.addSeparator()
        self.menuSession.addAction(self.actionSave)
        self.menuSession.addAction(self.actionLoad)
        self.menuSession.addAction(self.menuRecent.menuAction())
        self.menuSession.addAction(self.actionClose)
        self.menuRecent.addSeparator()
        self.menuEdit.addAction(self.actionMain_restoreState)
        self.menuViewer.addAction(self.menuCreate.menuAction())
        self.menuViewer.addAction(self.menuOpened_Viewer.menuAction())
        self.menuViewer.addAction(self.actionViewer_close)
        self.menuCreate.addAction(self.actionViewer1D_create)
        self.menuCreate.addAction(self.actionViewer2D_create)
        self.menuOpened_Viewer.addSeparator()
        self.menuWidgets.addAction(self.actionToF)
        self.menuWidgets.addAction(self.actionVMI)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuFile_restartAction.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.actionMain_close.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionMain_restart.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.actiong.setText(QCoreApplication.translate("MainWindow", u"g", None))
        self.actionFile_load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionMain_restoreState.setText(QCoreApplication.translate("MainWindow", u"Restore initial state", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionData.setText(QCoreApplication.translate("MainWindow", u"Data", None))
        self.actionViewer1D_create.setText(QCoreApplication.translate("MainWindow", u"1D", None))
        self.actionViewer2D_create.setText(QCoreApplication.translate("MainWindow", u"2D", None))
        self.actionViewer_close.setText(QCoreApplication.translate("MainWindow", u"Close all", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionToF.setText(QCoreApplication.translate("MainWindow", u"ToF", None))
        self.actionVMI.setText(QCoreApplication.translate("MainWindow", u"VMI", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSession.setTitle(QCoreApplication.translate("MainWindow", u"Session", None))
        self.menuRecent.setTitle(QCoreApplication.translate("MainWindow", u"Recent", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuViewer.setTitle(QCoreApplication.translate("MainWindow", u"Viewer", None))
        self.menuCreate.setTitle(QCoreApplication.translate("MainWindow", u"Create", None))
        self.menuOpened_Viewer.setTitle(QCoreApplication.translate("MainWindow", u"Opened Viewer", None))
        self.menuWidgets.setTitle(QCoreApplication.translate("MainWindow", u"Panel", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

