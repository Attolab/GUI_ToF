# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VMI_toolbox.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_VMI_toolbox_panel(object):
    def setupUi(self, VMI_toolbox_panel):
        if not VMI_toolbox_panel.objectName():
            VMI_toolbox_panel.setObjectName(u"VMI_toolbox_panel")
        VMI_toolbox_panel.resize(560, 524)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VMI_toolbox_panel.sizePolicy().hasHeightForWidth())
        VMI_toolbox_panel.setSizePolicy(sizePolicy)
        VMI_toolbox_panel.setMinimumSize(QSize(0, 0))
        self.verticalLayout_3 = QVBoxLayout(VMI_toolbox_panel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_7 = QGroupBox(VMI_toolbox_panel)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.groupBox_7)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_5 = QGroupBox(self.groupBox_7)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.imageBins_label = QLabel(self.groupBox_5)
        self.imageBins_label.setObjectName(u"imageBins_label")

        self.gridLayout.addWidget(self.imageBins_label, 0, 0, 1, 1)

        self.radialBins_label = QLabel(self.groupBox_5)
        self.radialBins_label.setObjectName(u"radialBins_label")

        self.gridLayout.addWidget(self.radialBins_label, 0, 1, 1, 1)

        self.angularBins_label = QLabel(self.groupBox_5)
        self.angularBins_label.setObjectName(u"angularBins_label")

        self.gridLayout.addWidget(self.angularBins_label, 0, 2, 1, 1)

        self.imageBins_spinBox = QSpinBox(self.groupBox_5)
        self.imageBins_spinBox.setObjectName(u"imageBins_spinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imageBins_spinBox.sizePolicy().hasHeightForWidth())
        self.imageBins_spinBox.setSizePolicy(sizePolicy1)
        self.imageBins_spinBox.setMaximum(1000000000)
        self.imageBins_spinBox.setValue(1)

        self.gridLayout.addWidget(self.imageBins_spinBox, 1, 0, 1, 1)

        self.radialBins_spinBox = QSpinBox(self.groupBox_5)
        self.radialBins_spinBox.setObjectName(u"radialBins_spinBox")
        sizePolicy1.setHeightForWidth(self.radialBins_spinBox.sizePolicy().hasHeightForWidth())
        self.radialBins_spinBox.setSizePolicy(sizePolicy1)
        self.radialBins_spinBox.setMaximum(1000000000)
        self.radialBins_spinBox.setValue(1)

        self.gridLayout.addWidget(self.radialBins_spinBox, 1, 1, 1, 1)

        self.angularBins_spinBox = QSpinBox(self.groupBox_5)
        self.angularBins_spinBox.setObjectName(u"angularBins_spinBox")
        sizePolicy1.setHeightForWidth(self.angularBins_spinBox.sizePolicy().hasHeightForWidth())
        self.angularBins_spinBox.setSizePolicy(sizePolicy1)
        self.angularBins_spinBox.setMaximum(1000000000)
        self.angularBins_spinBox.setValue(1)

        self.gridLayout.addWidget(self.angularBins_spinBox, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_5, 1, 0, 1, 2)

        self.groupBox_3 = QGroupBox(self.groupBox_7)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setEnabled(True)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setCheckable(True)
        self.formLayout_4 = QFormLayout(self.groupBox_3)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.shapeFilter_label = QLabel(self.groupBox_3)
        self.shapeFilter_label.setObjectName(u"shapeFilter_label")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.shapeFilter_label)

        self.Range_label = QLabel(self.groupBox_3)
        self.Range_label.setObjectName(u"Range_label")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.Range_label)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(6)
        self.Rmin_label = QLabel(self.groupBox_3)
        self.Rmin_label.setObjectName(u"Rmin_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.Rmin_label)

        self.Rmin_doubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.Rmin_doubleSpinBox.setObjectName(u"Rmin_doubleSpinBox")
        sizePolicy1.setHeightForWidth(self.Rmin_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.Rmin_doubleSpinBox.setSizePolicy(sizePolicy1)
        self.Rmin_doubleSpinBox.setMaximum(1000000.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.Rmin_doubleSpinBox)

        self.Rmax_label = QLabel(self.groupBox_3)
        self.Rmax_label.setObjectName(u"Rmax_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.Rmax_label)

        self.Rmax_doubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.Rmax_doubleSpinBox.setObjectName(u"Rmax_doubleSpinBox")
        sizePolicy1.setHeightForWidth(self.Rmax_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.Rmax_doubleSpinBox.setSizePolicy(sizePolicy1)
        self.Rmax_doubleSpinBox.setMaximum(1000000.000000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.Rmax_doubleSpinBox)


        self.formLayout_4.setLayout(2, QFormLayout.FieldRole, self.formLayout_2)

        self.shapeFilter_comboBox = QComboBox(self.groupBox_3)
        self.shapeFilter_comboBox.addItem("")
        self.shapeFilter_comboBox.addItem("")
        self.shapeFilter_comboBox.setObjectName(u"shapeFilter_comboBox")
        self.shapeFilter_comboBox.setMaxCount(10)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.shapeFilter_comboBox)


        self.gridLayout_2.addWidget(self.groupBox_3, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBox_7)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.formLayout_3 = QFormLayout(self.groupBox_2)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.dataSelection_label = QLabel(self.groupBox_2)
        self.dataSelection_label.setObjectName(u"dataSelection_label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.dataSelection_label)

        self.dataSelection_lineEdit = QLineEdit(self.groupBox_2)
        self.dataSelection_lineEdit.setObjectName(u"dataSelection_lineEdit")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.dataSelection_lineEdit)

        self.dataSorting_label = QLabel(self.groupBox_2)
        self.dataSorting_label.setObjectName(u"dataSorting_label")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.dataSorting_label)

        self.dataSorting_comboBox = QComboBox(self.groupBox_2)
        self.dataSorting_comboBox.addItem("")
        self.dataSorting_comboBox.addItem("")
        self.dataSorting_comboBox.addItem("")
        self.dataSorting_comboBox.setObjectName(u"dataSorting_comboBox")
        self.dataSorting_comboBox.setMaxCount(10)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.dataSorting_comboBox)

        self.dataStacking_label = QLabel(self.groupBox_2)
        self.dataStacking_label.setObjectName(u"dataStacking_label")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.dataStacking_label)

        self.dataStacking_comboBox = QComboBox(self.groupBox_2)
        self.dataStacking_comboBox.addItem("")
        self.dataStacking_comboBox.addItem("")
        self.dataStacking_comboBox.addItem("")
        self.dataStacking_comboBox.setObjectName(u"dataStacking_comboBox")
        self.dataStacking_comboBox.setMaxCount(10)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.dataStacking_comboBox)


        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(VMI_toolbox_panel)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.horizontalLayout = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_4 = QGroupBox(self.groupBox_8)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radialDistributions_checkBox = QCheckBox(self.groupBox_4)
        self.radialDistributions_checkBox.setObjectName(u"radialDistributions_checkBox")

        self.verticalLayout.addWidget(self.radialDistributions_checkBox)

        self.angularDistributions_checkBox = QCheckBox(self.groupBox_4)
        self.angularDistributions_checkBox.setObjectName(u"angularDistributions_checkBox")

        self.verticalLayout.addWidget(self.angularDistributions_checkBox)


        self.horizontalLayout.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.groupBox_8)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.angularContour_checkBox = QCheckBox(self.groupBox_6)
        self.angularContour_checkBox.setObjectName(u"angularContour_checkBox")

        self.verticalLayout_2.addWidget(self.angularContour_checkBox)

        self.radialContour_checkBox = QCheckBox(self.groupBox_6)
        self.radialContour_checkBox.setObjectName(u"radialContour_checkBox")

        self.verticalLayout_2.addWidget(self.radialContour_checkBox)


        self.horizontalLayout.addWidget(self.groupBox_6)

        self.groupBox = QGroupBox(self.groupBox_8)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.abel_inversion_sel_label = QLabel(self.groupBox)
        self.abel_inversion_sel_label.setObjectName(u"abel_inversion_sel_label")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label, 0, 0, 1, 1)

        self.abelInversion_comboBox = QComboBox(self.groupBox)
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.addItem("")
        self.abelInversion_comboBox.setObjectName(u"abelInversion_comboBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.abelInversion_comboBox.sizePolicy().hasHeightForWidth())
        self.abelInversion_comboBox.setSizePolicy(sizePolicy2)
        self.abelInversion_comboBox.setInputMethodHints(Qt.ImhNone)
        self.abelInversion_comboBox.setMaxCount(10)
        self.abelInversion_comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)

        self.gridLayout_3.addWidget(self.abelInversion_comboBox, 0, 1, 1, 2)

        self.abel_inversion_sel_label_2 = QLabel(self.groupBox)
        self.abel_inversion_sel_label_2.setObjectName(u"abel_inversion_sel_label_2")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label_2, 1, 0, 1, 2)

        self.abelLegendre_spinBox = QSpinBox(self.groupBox)
        self.abelLegendre_spinBox.setObjectName(u"abelLegendre_spinBox")
        sizePolicy2.setHeightForWidth(self.abelLegendre_spinBox.sizePolicy().hasHeightForWidth())
        self.abelLegendre_spinBox.setSizePolicy(sizePolicy2)
        self.abelLegendre_spinBox.setMaximum(1000000000)
        self.abelLegendre_spinBox.setSingleStep(2)
        self.abelLegendre_spinBox.setValue(2)

        self.gridLayout_3.addWidget(self.abelLegendre_spinBox, 1, 2, 1, 1)

        self.abel_inversion_sel_label_3 = QLabel(self.groupBox)
        self.abel_inversion_sel_label_3.setObjectName(u"abel_inversion_sel_label_3")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label_3, 2, 0, 1, 2)

        self.abelSymmetrize_checkBox = QCheckBox(self.groupBox)
        self.abelSymmetrize_checkBox.setObjectName(u"abelSymmetrize_checkBox")
        self.abelSymmetrize_checkBox.setTristate(False)

        self.gridLayout_3.addWidget(self.abelSymmetrize_checkBox, 2, 2, 1, 1)

        self.abel_inversion_sel_label_4 = QLabel(self.groupBox)
        self.abel_inversion_sel_label_4.setObjectName(u"abel_inversion_sel_label_4")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label_4, 3, 0, 1, 1)

        self.abelSmooth_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.abelSmooth_doubleSpinBox.setObjectName(u"abelSmooth_doubleSpinBox")
        sizePolicy2.setHeightForWidth(self.abelSmooth_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.abelSmooth_doubleSpinBox.setSizePolicy(sizePolicy2)
        self.abelSmooth_doubleSpinBox.setMaximum(1000000.000000000000000)

        self.gridLayout_3.addWidget(self.abelSmooth_doubleSpinBox, 3, 2, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox)


        self.verticalLayout_3.addWidget(self.groupBox_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.go_pushButton = QPushButton(VMI_toolbox_panel)
        self.go_pushButton.setObjectName(u"go_pushButton")

        self.horizontalLayout_3.addWidget(self.go_pushButton)

        self.showOutput_checkBox = QCheckBox(VMI_toolbox_panel)
        self.showOutput_checkBox.setObjectName(u"showOutput_checkBox")

        self.horizontalLayout_3.addWidget(self.showOutput_checkBox)

        self.saveOutput_checkBox = QCheckBox(VMI_toolbox_panel)
        self.saveOutput_checkBox.setObjectName(u"saveOutput_checkBox")

        self.horizontalLayout_3.addWidget(self.saveOutput_checkBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.retranslateUi(VMI_toolbox_panel)

        QMetaObject.connectSlotsByName(VMI_toolbox_panel)
    # setupUi

    def retranslateUi(self, VMI_toolbox_panel):
        VMI_toolbox_panel.setWindowTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Form", None))
        self.groupBox_7.setTitle("")
        self.groupBox_5.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Bins", None))
        self.imageBins_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Image", None))
        self.radialBins_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Radial", None))
        self.angularBins_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Angular", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Data filtering", None))
        self.shapeFilter_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Selection", None))
        self.Range_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Range", None))
        self.Rmin_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Rmin", None))
        self.Rmax_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Rmax", None))
        self.shapeFilter_comboBox.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"Rectangle", None))
        self.shapeFilter_comboBox.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Ellipse", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Data selection and ordering", None))
        self.dataSelection_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Selection", None))
        self.dataSorting_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Sort by", None))
        self.dataSorting_comboBox.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"Image number", None))
        self.dataSorting_comboBox.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Parameter", None))
        self.dataSorting_comboBox.setItemText(2, QCoreApplication.translate("VMI_toolbox_panel", u"Time", None))

        self.dataStacking_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Stack ", None))
        self.dataStacking_comboBox.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"No stack", None))
        self.dataStacking_comboBox.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Same parameter", None))
        self.dataStacking_comboBox.setItemText(2, QCoreApplication.translate("VMI_toolbox_panel", u"Stack all", None))

        self.groupBox_8.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Output", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Distributions", None))
        self.radialDistributions_checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Radial", None))
        self.angularDistributions_checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Angular", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Contour", None))
        self.angularContour_checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Radial", None))
        self.radialContour_checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Angular", None))
        self.groupBox.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Abel inversion", None))
        self.abel_inversion_sel_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Algorithm", None))
        self.abelInversion_comboBox.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"Abel Davis", None))
        self.abelInversion_comboBox.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Basex", None))
        self.abelInversion_comboBox.setItemText(2, QCoreApplication.translate("VMI_toolbox_panel", u"Dasch", None))
        self.abelInversion_comboBox.setItemText(3, QCoreApplication.translate("VMI_toolbox_panel", u"Direct", None))
        self.abelInversion_comboBox.setItemText(4, QCoreApplication.translate("VMI_toolbox_panel", u"Hansenlaw", None))
        self.abelInversion_comboBox.setItemText(5, QCoreApplication.translate("VMI_toolbox_panel", u"Linbasex", None))
        self.abelInversion_comboBox.setItemText(6, QCoreApplication.translate("VMI_toolbox_panel", u"Onion peeling", None))

        self.abel_inversion_sel_label_2.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Legendre polynomial", None))
        self.abel_inversion_sel_label_3.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Symmetrize", None))
        self.abelSymmetrize_checkBox.setText("")
        self.abel_inversion_sel_label_4.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Smooth", None))
        self.go_pushButton.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Try me!", None))
        self.showOutput_checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Show output", None))
        self.saveOutput_checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Save output", None))
    # retranslateUi

