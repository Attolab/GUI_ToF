# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewer2D_widget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QSizePolicy,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

from CustomTableWidget import ROITableWidget
from pyqtgraph import GraphicsLayoutWidget

class Ui_Viewer2DWidget(object):
    def setupUi(self, Viewer2DWidget):
        if not Viewer2DWidget.objectName():
            Viewer2DWidget.setObjectName(u"Viewer2DWidget")
        Viewer2DWidget.resize(1007, 602)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Viewer2DWidget.sizePolicy().hasHeightForWidth())
        Viewer2DWidget.setSizePolicy(sizePolicy)
        Viewer2DWidget.setLocale(QLocale(QLocale.C, QLocale.AnyCountry))
        self.horizontalLayout_3 = QHBoxLayout(Viewer2DWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Viewer2DWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.show2D_checkBox = QCheckBox(Viewer2DWidget)
        self.show2D_checkBox.setObjectName(u"show2D_checkBox")
        self.show2D_checkBox.setChecked(True)
        self.show2D_checkBox.setTristate(False)

        self.horizontalLayout.addWidget(self.show2D_checkBox)

        self.showROI_checkBox = QCheckBox(Viewer2DWidget)
        self.showROI_checkBox.setObjectName(u"showROI_checkBox")
        self.showROI_checkBox.setChecked(True)

        self.horizontalLayout.addWidget(self.showROI_checkBox)

        self.showHist_checkBox = QCheckBox(Viewer2DWidget)
        self.showHist_checkBox.setObjectName(u"showHist_checkBox")
        self.showHist_checkBox.setChecked(False)
        self.showHist_checkBox.setTristate(False)

        self.horizontalLayout.addWidget(self.showHist_checkBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.viewer_GraphicsLayoutWidget = GraphicsLayoutWidget(Viewer2DWidget)
        self.viewer_GraphicsLayoutWidget.setObjectName(u"viewer_GraphicsLayoutWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.viewer_GraphicsLayoutWidget.sizePolicy().hasHeightForWidth())
        self.viewer_GraphicsLayoutWidget.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.viewer_GraphicsLayoutWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Viewer2DWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.autoRange_checkBox = QCheckBox(Viewer2DWidget)
        self.autoRange_checkBox.setObjectName(u"autoRange_checkBox")
        self.autoRange_checkBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.autoRange_checkBox)

        self.autoLevels_checkBox = QCheckBox(Viewer2DWidget)
        self.autoLevels_checkBox.setObjectName(u"autoLevels_checkBox")
        self.autoLevels_checkBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.autoLevels_checkBox)

        self.options_checkBox = QCheckBox(Viewer2DWidget)
        self.options_checkBox.setObjectName(u"options_checkBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.options_checkBox.sizePolicy().hasHeightForWidth())
        self.options_checkBox.setSizePolicy(sizePolicy2)
        self.options_checkBox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_2.addWidget(self.options_checkBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.groupBox = QGroupBox(Viewer2DWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.makeROI_toolButton = QToolButton(self.groupBox)
        self.makeROI_toolButton.setObjectName(u"makeROI_toolButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.makeROI_toolButton.sizePolicy().hasHeightForWidth())
        self.makeROI_toolButton.setSizePolicy(sizePolicy3)
        self.makeROI_toolButton.setMinimumSize(QSize(150, 0))
        self.makeROI_toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.makeROI_toolButton.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.makeROI_toolButton.setAutoRaise(False)
        self.makeROI_toolButton.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.makeROI_toolButton)

        self.tableROI_tableWidget = ROITableWidget(self.groupBox)
        if (self.tableROI_tableWidget.columnCount() < 2):
            self.tableROI_tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableROI_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableROI_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableROI_tableWidget.setObjectName(u"tableROI_tableWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tableROI_tableWidget.sizePolicy().hasHeightForWidth())
        self.tableROI_tableWidget.setSizePolicy(sizePolicy4)
        self.tableROI_tableWidget.setMinimumSize(QSize(100, 0))
        self.tableROI_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableROI_tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableROI_tableWidget)


        self.horizontalLayout_3.addWidget(self.groupBox)


        self.retranslateUi(Viewer2DWidget)

        QMetaObject.connectSlotsByName(Viewer2DWidget)
    # setupUi

    def retranslateUi(self, Viewer2DWidget):
        Viewer2DWidget.setWindowTitle(QCoreApplication.translate("Viewer2DWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("Viewer2DWidget", u"Display", None))
        self.show2D_checkBox.setText(QCoreApplication.translate("Viewer2DWidget", u"Viewer", None))
        self.showROI_checkBox.setText(QCoreApplication.translate("Viewer2DWidget", u"ROI", None))
        self.showHist_checkBox.setText(QCoreApplication.translate("Viewer2DWidget", u"Hist", None))
        self.label_2.setText(QCoreApplication.translate("Viewer2DWidget", u"Color", None))
        self.autoRange_checkBox.setText(QCoreApplication.translate("Viewer2DWidget", u"AutoRange", None))
        self.autoLevels_checkBox.setText(QCoreApplication.translate("Viewer2DWidget", u"AutoLevels", None))
        self.options_checkBox.setText(QCoreApplication.translate("Viewer2DWidget", u"options", None))
        self.groupBox.setTitle(QCoreApplication.translate("Viewer2DWidget", u"Options", None))
        self.makeROI_toolButton.setText(QCoreApplication.translate("Viewer2DWidget", u"Add ROI", None))
        ___qtablewidgetitem = self.tableROI_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Viewer2DWidget", u"Name", None));
        ___qtablewidgetitem1 = self.tableROI_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Viewer2DWidget", u"Type", None));
    # retranslateUi

