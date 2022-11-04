# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VMI_panel.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSplitter, QTableWidgetItem, QToolButton, QVBoxLayout,
    QWidget)

from CustomTableWidget import imageSelectionTableWidget
from VMI_toolbox import VMIToolBox
from pyqtgraph.parametertree import ParameterTree
from viewer2D_widget import Viewer2DWidget

class Ui_VMI_panel(object):
    def setupUi(self, VMI_panel):
        if not VMI_panel.objectName():
            VMI_panel.setObjectName(u"VMI_panel")
        VMI_panel.setEnabled(True)
        VMI_panel.resize(830, 609)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VMI_panel.sizePolicy().hasHeightForWidth())
        VMI_panel.setSizePolicy(sizePolicy)
        VMI_panel.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(VMI_panel)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_2 = QSplitter(VMI_panel)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter_2)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label)

        self.folderBase_lineEdit = QLineEdit(self.widget)
        self.folderBase_lineEdit.setObjectName(u"folderBase_lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.folderBase_lineEdit.sizePolicy().hasHeightForWidth())
        self.folderBase_lineEdit.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.folderBase_lineEdit)

        self.folderSelection_toolButton = QToolButton(self.widget)
        self.folderSelection_toolButton.setObjectName(u"folderSelection_toolButton")

        self.horizontalLayout_5.addWidget(self.folderSelection_toolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.loadFile_button = QPushButton(self.widget)
        self.loadFile_button.setObjectName(u"loadFile_button")

        self.verticalLayout.addWidget(self.loadFile_button)

        self.splitter = QSplitter(self.widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.settings_parameterTree = ParameterTree(self.splitter)
        self.settings_parameterTree.setObjectName(u"settings_parameterTree")
        sizePolicy1.setHeightForWidth(self.settings_parameterTree.sizePolicy().hasHeightForWidth())
        self.settings_parameterTree.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.settings_parameterTree)
        self.image_tableWidget = imageSelectionTableWidget(self.splitter)
        if (self.image_tableWidget.columnCount() < 2):
            self.image_tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.image_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.image_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.image_tableWidget.setObjectName(u"image_tableWidget")
        self.image_tableWidget.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.image_tableWidget.sizePolicy().hasHeightForWidth())
        self.image_tableWidget.setSizePolicy(sizePolicy3)
        self.image_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.splitter.addWidget(self.image_tableWidget)
        self.image_tableWidget.horizontalHeader().setVisible(True)
        self.image_tableWidget.verticalHeader().setVisible(False)
        self.image_tableWidget.verticalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.splitter)

        self.VMI_toolBox = VMIToolBox(self.widget)
        self.VMI_toolBox.setObjectName(u"VMI_toolBox")

        self.verticalLayout.addWidget(self.VMI_toolBox)

        self.splitter_2.addWidget(self.widget)
        self.imageViewer = Viewer2DWidget(self.splitter_2)
        self.imageViewer.setObjectName(u"imageViewer")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.imageViewer.sizePolicy().hasHeightForWidth())
        self.imageViewer.setSizePolicy(sizePolicy4)
        self.splitter_2.addWidget(self.imageViewer)

        self.horizontalLayout.addWidget(self.splitter_2)


        self.retranslateUi(VMI_panel)

        QMetaObject.connectSlotsByName(VMI_panel)
    # setupUi

    def retranslateUi(self, VMI_panel):
        VMI_panel.setWindowTitle(QCoreApplication.translate("VMI_panel", u"Form", None))
        self.label.setText(QCoreApplication.translate("VMI_panel", u"Starting folder", None))
#if QT_CONFIG(tooltip)
        self.folderBase_lineEdit.setToolTip(QCoreApplication.translate("VMI_panel", u"<html><head/><body><p>Use this folder as the base folder when loading data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.folderSelection_toolButton.setText(QCoreApplication.translate("VMI_panel", u"...", None))
        self.loadFile_button.setText(QCoreApplication.translate("VMI_panel", u"Load File", None))
        ___qtablewidgetitem = self.image_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("VMI_panel", u"Image index", None));
        ___qtablewidgetitem1 = self.image_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("VMI_panel", u"Parameter", None));
    # retranslateUi

