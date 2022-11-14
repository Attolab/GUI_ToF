# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewer1D_widget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QPushButton, QSizePolicy, QTabWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

from CustomTableWidget import ROITableWidget
from CustomToolButton import ROIToolButton
from ParameterTree import CustomParameterTree
from pyqtgraph import GraphicsLayoutWidget
from pyqtgraph.parametertree import ParameterTree

class Ui_Viewer1DWidget(object):
    def setupUi(self, Viewer1DWidget):
        if not Viewer1DWidget.objectName():
            Viewer1DWidget.setObjectName(u"Viewer1DWidget")
        Viewer1DWidget.resize(795, 443)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Viewer1DWidget.sizePolicy().hasHeightForWidth())
        Viewer1DWidget.setSizePolicy(sizePolicy)
        Viewer1DWidget.setLocale(QLocale(QLocale.C, QLocale.AnyCountry))
        self.horizontalLayout = QHBoxLayout(Viewer1DWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.viewer_GraphicsLayoutWidget = GraphicsLayoutWidget(Viewer1DWidget)
        self.viewer_GraphicsLayoutWidget.setObjectName(u"viewer_GraphicsLayoutWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.viewer_GraphicsLayoutWidget.sizePolicy().hasHeightForWidth())
        self.viewer_GraphicsLayoutWidget.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.viewer_GraphicsLayoutWidget)

        self.options_checkBox = QCheckBox(Viewer1DWidget)
        self.options_checkBox.setObjectName(u"options_checkBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.options_checkBox.sizePolicy().hasHeightForWidth())
        self.options_checkBox.setSizePolicy(sizePolicy2)
        self.options_checkBox.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout_4.addWidget(self.options_checkBox)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.tabWidget = QTabWidget(Viewer1DWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy4)
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plot_ParameterTree = CustomParameterTree(self.tab)
        self.plot_ParameterTree.setObjectName(u"plot_ParameterTree")
        sizePolicy4.setHeightForWidth(self.plot_ParameterTree.sizePolicy().hasHeightForWidth())
        self.plot_ParameterTree.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.plot_ParameterTree)

        self.addPlot_pushButton = QPushButton(self.tab)
        self.addPlot_pushButton.setObjectName(u"addPlot_pushButton")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.addPlot_pushButton.sizePolicy().hasHeightForWidth())
        self.addPlot_pushButton.setSizePolicy(sizePolicy5)

        self.verticalLayout.addWidget(self.addPlot_pushButton)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        sizePolicy4.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy4)
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.makeROI_toolButton = ROIToolButton(self.tab_2)
        self.makeROI_toolButton.setObjectName(u"makeROI_toolButton")
        sizePolicy5.setHeightForWidth(self.makeROI_toolButton.sizePolicy().hasHeightForWidth())
        self.makeROI_toolButton.setSizePolicy(sizePolicy5)
        self.makeROI_toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.makeROI_toolButton.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.makeROI_toolButton.setAutoRaise(True)
        self.makeROI_toolButton.setArrowType(Qt.RightArrow)

        self.verticalLayout_2.addWidget(self.makeROI_toolButton)

        self.tableROI_tableWidget = ROITableWidget(self.tab_2)
        if (self.tableROI_tableWidget.columnCount() < 3):
            self.tableROI_tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableROI_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableROI_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableROI_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableROI_tableWidget.setObjectName(u"tableROI_tableWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.tableROI_tableWidget.sizePolicy().hasHeightForWidth())
        self.tableROI_tableWidget.setSizePolicy(sizePolicy6)
        self.tableROI_tableWidget.setMinimumSize(QSize(0, 0))
        self.tableROI_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableROI_tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.tableROI_tableWidget)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.settings_ParameterTree = ParameterTree(self.tab_3)
        self.settings_ParameterTree.setObjectName(u"settings_ParameterTree")
        sizePolicy4.setHeightForWidth(self.settings_ParameterTree.sizePolicy().hasHeightForWidth())
        self.settings_ParameterTree.setSizePolicy(sizePolicy4)

        self.verticalLayout_3.addWidget(self.settings_ParameterTree)

        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Viewer1DWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Viewer1DWidget)
    # setupUi

    def retranslateUi(self, Viewer1DWidget):
        Viewer1DWidget.setWindowTitle(QCoreApplication.translate("Viewer1DWidget", u"Form", None))
        self.options_checkBox.setText(QCoreApplication.translate("Viewer1DWidget", u"options", None))
        self.addPlot_pushButton.setText(QCoreApplication.translate("Viewer1DWidget", u"AddPlot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Viewer1DWidget", u"Plot", None))
        self.makeROI_toolButton.setText(QCoreApplication.translate("Viewer1DWidget", u"Add ROI", None))
        ___qtablewidgetitem = self.tableROI_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Viewer1DWidget", u"Name", None));
        ___qtablewidgetitem1 = self.tableROI_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Viewer1DWidget", u"Orientation", None));
        ___qtablewidgetitem2 = self.tableROI_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Viewer1DWidget", u"Type", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Viewer1DWidget", u"ROI", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Viewer1DWidget", u"Settings", None))
    # retranslateUi

