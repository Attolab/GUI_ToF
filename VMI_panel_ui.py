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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDockWidget, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidgetItem,
    QToolButton, QVBoxLayout, QWidget)

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
        self.horizontalLayout_6 = QHBoxLayout(VMI_panel)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(VMI_panel)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label)

        self.folderBase_lineEdit = QLineEdit(VMI_panel)
        self.folderBase_lineEdit.setObjectName(u"folderBase_lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.folderBase_lineEdit.sizePolicy().hasHeightForWidth())
        self.folderBase_lineEdit.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.folderBase_lineEdit)

        self.folderSelection_toolButton = QToolButton(VMI_panel)
        self.folderSelection_toolButton.setObjectName(u"folderSelection_toolButton")

        self.horizontalLayout_5.addWidget(self.folderSelection_toolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.loadFile_button = QPushButton(VMI_panel)
        self.loadFile_button.setObjectName(u"loadFile_button")

        self.verticalLayout.addWidget(self.loadFile_button)

        self.settings_parameterTree = ParameterTree(VMI_panel)
        self.settings_parameterTree.setObjectName(u"settings_parameterTree")
        sizePolicy1.setHeightForWidth(self.settings_parameterTree.sizePolicy().hasHeightForWidth())
        self.settings_parameterTree.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.settings_parameterTree)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.dataset_label = QLabel(VMI_panel)
        self.dataset_label.setObjectName(u"dataset_label")

        self.horizontalLayout.addWidget(self.dataset_label)

        self.datasetSel_label = QLabel(VMI_panel)
        self.datasetSel_label.setObjectName(u"datasetSel_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.datasetSel_label.sizePolicy().hasHeightForWidth())
        self.datasetSel_label.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.datasetSel_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.imageNumber_label = QLabel(VMI_panel)
        self.imageNumber_label.setObjectName(u"imageNumber_label")
        sizePolicy1.setHeightForWidth(self.imageNumber_label.sizePolicy().hasHeightForWidth())
        self.imageNumber_label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.imageNumber_label)

        self.imageNumber_value = QLabel(VMI_panel)
        self.imageNumber_value.setObjectName(u"imageNumber_value")
        sizePolicy3.setHeightForWidth(self.imageNumber_value.sizePolicy().hasHeightForWidth())
        self.imageNumber_value.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.imageNumber_value)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.image_tableWidget = imageSelectionTableWidget(VMI_panel)
        if (self.image_tableWidget.columnCount() < 2):
            self.image_tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.image_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.image_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.image_tableWidget.setObjectName(u"image_tableWidget")
        self.image_tableWidget.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.image_tableWidget.sizePolicy().hasHeightForWidth())
        self.image_tableWidget.setSizePolicy(sizePolicy4)
        self.image_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.image_tableWidget.horizontalHeader().setVisible(True)
        self.image_tableWidget.verticalHeader().setVisible(False)

        self.horizontalLayout_3.addWidget(self.image_tableWidget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.dockWidget = QDockWidget(VMI_panel)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setFloating(True)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.horizontalLayout_4 = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.VMI_toolBox = VMIToolBox(self.dockWidgetContents)
        self.VMI_toolBox.setObjectName(u"VMI_toolBox")

        self.horizontalLayout_4.addWidget(self.VMI_toolBox)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.verticalLayout.addWidget(self.dockWidget)

        self.ApplyButton = QPushButton(VMI_panel)
        self.ApplyButton.setObjectName(u"ApplyButton")

        self.verticalLayout.addWidget(self.ApplyButton)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.imageViewer = Viewer2DWidget(VMI_panel)
        self.imageViewer.setObjectName(u"imageViewer")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.imageViewer.sizePolicy().hasHeightForWidth())
        self.imageViewer.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.imageViewer)


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
        self.dataset_label.setText(QCoreApplication.translate("VMI_panel", u"Dataset", None))
        self.datasetSel_label.setText(QCoreApplication.translate("VMI_panel", u"TextLabel", None))
        self.imageNumber_label.setText(QCoreApplication.translate("VMI_panel", u"Number of images", None))
        self.imageNumber_value.setText(QCoreApplication.translate("VMI_panel", u"TextLabel", None))
        ___qtablewidgetitem = self.image_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("VMI_panel", u"Image index", None));
        ___qtablewidgetitem1 = self.image_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("VMI_panel", u"Parameter", None));
        self.ApplyButton.setText(QCoreApplication.translate("VMI_panel", u"ToolBox", None))
    # retranslateUi

