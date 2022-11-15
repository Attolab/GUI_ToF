# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewerContainer_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QTabWidget, QToolButton, QVBoxLayout, QWidget)

from ParameterTree import CustomParameterTree
from pyqtgraph.parametertree import ParameterTree
from viewerDockArea import ViewerDockArea

class Ui_ViewerContainer(object):
    def setupUi(self, ViewerContainer):
        if not ViewerContainer.objectName():
            ViewerContainer.setObjectName(u"ViewerContainer")
        ViewerContainer.resize(662, 398)
        self.horizontalLayout_2 = QHBoxLayout(ViewerContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(ViewerContainer)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.viewer_ParameterTree = CustomParameterTree(self.tab)
        self.viewer_ParameterTree.setObjectName(u"viewer_ParameterTree")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.viewer_ParameterTree.sizePolicy().hasHeightForWidth())
        self.viewer_ParameterTree.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.viewer_ParameterTree)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_toolButton = QToolButton(self.tab)
        self.add_toolButton.setObjectName(u"add_toolButton")

        self.horizontalLayout.addWidget(self.add_toolButton)

        self.load_pushButton = QPushButton(self.tab)
        self.load_pushButton.setObjectName(u"load_pushButton")

        self.horizontalLayout.addWidget(self.load_pushButton)

        self.save_pushButton = QPushButton(self.tab)
        self.save_pushButton.setObjectName(u"save_pushButton")

        self.horizontalLayout.addWidget(self.save_pushButton)

        self.clear_pushButton = QPushButton(self.tab)
        self.clear_pushButton.setObjectName(u"clear_pushButton")

        self.horizontalLayout.addWidget(self.clear_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        sizePolicy1.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.operations_ParameterTree = ParameterTree(self.tab_2)
        self.operations_ParameterTree.setObjectName(u"operations_ParameterTree")
        sizePolicy1.setHeightForWidth(self.operations_ParameterTree.sizePolicy().hasHeightForWidth())
        self.operations_ParameterTree.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.operations_ParameterTree)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout_2.addWidget(self.operations_ParameterTree)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.settings_ParameterTree = ParameterTree(self.tab_3)
        self.settings_ParameterTree.setObjectName(u"settings_ParameterTree")
        sizePolicy1.setHeightForWidth(self.settings_ParameterTree.sizePolicy().hasHeightForWidth())
        self.settings_ParameterTree.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.settings_ParameterTree)

        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.viewer_dockArea = ViewerDockArea(ViewerContainer)
        self.viewer_dockArea.setObjectName(u"viewer_dockArea")

        self.horizontalLayout_2.addWidget(self.viewer_dockArea)


        self.retranslateUi(ViewerContainer)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ViewerContainer)
    # setupUi

    def retranslateUi(self, ViewerContainer):
        ViewerContainer.setWindowTitle(QCoreApplication.translate("ViewerContainer", u"Form", None))
        self.add_toolButton.setText(QCoreApplication.translate("ViewerContainer", u"Add", None))
        self.load_pushButton.setText(QCoreApplication.translate("ViewerContainer", u"Load", None))
        self.save_pushButton.setText(QCoreApplication.translate("ViewerContainer", u"Save", None))
        self.clear_pushButton.setText(QCoreApplication.translate("ViewerContainer", u"Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("ViewerContainer", u"Viewer", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("ViewerContainer", u"Operations", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("ViewerContainer", u"Settings", None))
    # retranslateUi

