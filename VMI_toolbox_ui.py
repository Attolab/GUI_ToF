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
        VMI_toolbox_panel.resize(568, 560)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VMI_toolbox_panel.sizePolicy().hasHeightForWidth())
        VMI_toolbox_panel.setSizePolicy(sizePolicy)
        VMI_toolbox_panel.setMinimumSize(QSize(271, 297))
        self.verticalLayout_3 = QVBoxLayout(VMI_toolbox_panel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_7 = QGroupBox(VMI_toolbox_panel)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.groupBox_7)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_2 = QGroupBox(self.groupBox_7)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_3 = QFormLayout(self.groupBox_2)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.abel_inversion_sel_label_12 = QLabel(self.groupBox_2)
        self.abel_inversion_sel_label_12.setObjectName(u"abel_inversion_sel_label_12")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.abel_inversion_sel_label_12)

        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.abel_inversion_sel_label_5 = QLabel(self.groupBox_2)
        self.abel_inversion_sel_label_5.setObjectName(u"abel_inversion_sel_label_5")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.abel_inversion_sel_label_5)

        self.abel_inversion_sel_combobox_2 = QComboBox(self.groupBox_2)
        self.abel_inversion_sel_combobox_2.addItem("")
        self.abel_inversion_sel_combobox_2.addItem("")
        self.abel_inversion_sel_combobox_2.addItem("")
        self.abel_inversion_sel_combobox_2.setObjectName(u"abel_inversion_sel_combobox_2")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.abel_inversion_sel_combobox_2)

        self.abel_inversion_sel_label_6 = QLabel(self.groupBox_2)
        self.abel_inversion_sel_label_6.setObjectName(u"abel_inversion_sel_label_6")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.abel_inversion_sel_label_6)

        self.abel_inversion_sel_combobox_3 = QComboBox(self.groupBox_2)
        self.abel_inversion_sel_combobox_3.addItem("")
        self.abel_inversion_sel_combobox_3.addItem("")
        self.abel_inversion_sel_combobox_3.addItem("")
        self.abel_inversion_sel_combobox_3.setObjectName(u"abel_inversion_sel_combobox_3")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.abel_inversion_sel_combobox_3)


        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.groupBox_7)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.formLayout_4 = QFormLayout(self.groupBox_3)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.abel_inversion_sel_label_13 = QLabel(self.groupBox_3)
        self.abel_inversion_sel_label_13.setObjectName(u"abel_inversion_sel_label_13")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.abel_inversion_sel_label_13)

        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.lineEdit_2)

        self.abel_inversion_sel_label_14 = QLabel(self.groupBox_3)
        self.abel_inversion_sel_label_14.setObjectName(u"abel_inversion_sel_label_14")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.abel_inversion_sel_label_14)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(6)
        self.abel_inversion_sel_label_10 = QLabel(self.groupBox_3)
        self.abel_inversion_sel_label_10.setObjectName(u"abel_inversion_sel_label_10")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.abel_inversion_sel_label_10)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.abel_inversion_sel_label_11 = QLabel(self.groupBox_3)
        self.abel_inversion_sel_label_11.setObjectName(u"abel_inversion_sel_label_11")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.abel_inversion_sel_label_11)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_3)


        self.formLayout_4.setLayout(1, QFormLayout.FieldRole, self.formLayout_2)


        self.gridLayout_2.addWidget(self.groupBox_3, 0, 1, 1, 1)

        self.groupBox_5 = QGroupBox(self.groupBox_7)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.abel_inversion_sel_label_7 = QLabel(self.groupBox_5)
        self.abel_inversion_sel_label_7.setObjectName(u"abel_inversion_sel_label_7")

        self.gridLayout.addWidget(self.abel_inversion_sel_label_7, 0, 0, 1, 1)

        self.abel_inversion_sel_label_8 = QLabel(self.groupBox_5)
        self.abel_inversion_sel_label_8.setObjectName(u"abel_inversion_sel_label_8")

        self.gridLayout.addWidget(self.abel_inversion_sel_label_8, 0, 1, 1, 1)

        self.abel_inversion_sel_label_9 = QLabel(self.groupBox_5)
        self.abel_inversion_sel_label_9.setObjectName(u"abel_inversion_sel_label_9")

        self.gridLayout.addWidget(self.abel_inversion_sel_label_9, 0, 2, 1, 1)

        self.spinBox = QSpinBox(self.groupBox_5)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setValue(1)

        self.gridLayout.addWidget(self.spinBox, 1, 0, 1, 1)

        self.spinBox_2 = QSpinBox(self.groupBox_5)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMaximum(1000000000)
        self.spinBox_2.setValue(1)

        self.gridLayout.addWidget(self.spinBox_2, 1, 1, 1, 1)

        self.spinBox_3 = QSpinBox(self.groupBox_5)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setMaximum(1000000000)
        self.spinBox_3.setValue(1)

        self.gridLayout.addWidget(self.spinBox_3, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_5, 1, 0, 1, 2)


        self.verticalLayout_3.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(VMI_toolbox_panel)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_4 = QGroupBox(self.groupBox_8)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox_3 = QCheckBox(self.groupBox_4)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.groupBox_4)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout.addWidget(self.checkBox_4)


        self.horizontalLayout.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.groupBox_8)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox_5 = QCheckBox(self.groupBox_6)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout_2.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.groupBox_6)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout_2.addWidget(self.checkBox_6)


        self.horizontalLayout.addWidget(self.groupBox_6)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(self.groupBox_8)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.abel_inversion_sel_label = QLabel(self.groupBox)
        self.abel_inversion_sel_label.setObjectName(u"abel_inversion_sel_label")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label, 0, 0, 1, 1)

        self.abel_inversion_sel_combobox = QComboBox(self.groupBox)
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.addItem("")
        self.abel_inversion_sel_combobox.setObjectName(u"abel_inversion_sel_combobox")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_combobox, 0, 1, 1, 2)

        self.abel_inversion_sel_label_2 = QLabel(self.groupBox)
        self.abel_inversion_sel_label_2.setObjectName(u"abel_inversion_sel_label_2")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label_2, 1, 0, 1, 2)

        self.spinBox_4 = QSpinBox(self.groupBox)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setMaximum(1000000000)
        self.spinBox_4.setSingleStep(2)
        self.spinBox_4.setValue(2)

        self.gridLayout_3.addWidget(self.spinBox_4, 1, 2, 1, 1)

        self.abel_inversion_sel_label_3 = QLabel(self.groupBox)
        self.abel_inversion_sel_label_3.setObjectName(u"abel_inversion_sel_label_3")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label_3, 2, 0, 1, 2)

        self.checkBox_7 = QCheckBox(self.groupBox)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.gridLayout_3.addWidget(self.checkBox_7, 2, 2, 1, 1)

        self.abel_inversion_sel_label_4 = QLabel(self.groupBox)
        self.abel_inversion_sel_label_4.setObjectName(u"abel_inversion_sel_label_4")

        self.gridLayout_3.addWidget(self.abel_inversion_sel_label_4, 3, 0, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")

        self.gridLayout_3.addWidget(self.doubleSpinBox_4, 3, 2, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox)


        self.verticalLayout_3.addWidget(self.groupBox_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(VMI_toolbox_panel)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.checkBox = QCheckBox(VMI_toolbox_panel)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_3.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(VMI_toolbox_panel)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_3.addWidget(self.checkBox_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.retranslateUi(VMI_toolbox_panel)

        QMetaObject.connectSlotsByName(VMI_toolbox_panel)
    # setupUi

    def retranslateUi(self, VMI_toolbox_panel):
        VMI_toolbox_panel.setWindowTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Form", None))
        self.groupBox_7.setTitle("")
        self.groupBox_2.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Data selection and ordering", None))
        self.abel_inversion_sel_label_12.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Selection", None))
        self.abel_inversion_sel_label_5.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Sort by", None))
        self.abel_inversion_sel_combobox_2.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"Image number", None))
        self.abel_inversion_sel_combobox_2.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Parameter", None))
        self.abel_inversion_sel_combobox_2.setItemText(2, QCoreApplication.translate("VMI_toolbox_panel", u"Time", None))

        self.abel_inversion_sel_label_6.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Stack ", None))
        self.abel_inversion_sel_combobox_3.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"No stack", None))
        self.abel_inversion_sel_combobox_3.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Same parameter", None))
        self.abel_inversion_sel_combobox_3.setItemText(2, QCoreApplication.translate("VMI_toolbox_panel", u"Stack all", None))

        self.groupBox_3.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Data filtering", None))
        self.abel_inversion_sel_label_13.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Selection", None))
        self.abel_inversion_sel_label_14.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Range", None))
        self.abel_inversion_sel_label_10.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Rmin", None))
        self.abel_inversion_sel_label_11.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Rmax", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Bins", None))
        self.abel_inversion_sel_label_7.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Image", None))
        self.abel_inversion_sel_label_8.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Radial", None))
        self.abel_inversion_sel_label_9.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Angular", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Output", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Distributions", None))
        self.checkBox_3.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Radial", None))
        self.checkBox_4.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Angular", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Contour", None))
        self.checkBox_5.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Radial", None))
        self.checkBox_6.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Angular", None))
        self.groupBox.setTitle(QCoreApplication.translate("VMI_toolbox_panel", u"Abel inversion", None))
        self.abel_inversion_sel_label.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Algorithm", None))
        self.abel_inversion_sel_combobox.setItemText(0, QCoreApplication.translate("VMI_toolbox_panel", u"Abel Davis", None))
        self.abel_inversion_sel_combobox.setItemText(1, QCoreApplication.translate("VMI_toolbox_panel", u"Basex", None))
        self.abel_inversion_sel_combobox.setItemText(2, QCoreApplication.translate("VMI_toolbox_panel", u"Dasch", None))
        self.abel_inversion_sel_combobox.setItemText(3, QCoreApplication.translate("VMI_toolbox_panel", u"Direct", None))
        self.abel_inversion_sel_combobox.setItemText(4, QCoreApplication.translate("VMI_toolbox_panel", u"Hansenlaw", None))
        self.abel_inversion_sel_combobox.setItemText(5, QCoreApplication.translate("VMI_toolbox_panel", u"Linbasex", None))
        self.abel_inversion_sel_combobox.setItemText(6, QCoreApplication.translate("VMI_toolbox_panel", u"Onion peeling", None))

        self.abel_inversion_sel_label_2.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Legendre polynomial", None))
        self.abel_inversion_sel_label_3.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Symmetrize", None))
        self.checkBox_7.setText("")
        self.abel_inversion_sel_label_4.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Smooth", None))
        self.pushButton.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Try me!", None))
        self.checkBox.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Show output", None))
        self.checkBox_2.setText(QCoreApplication.translate("VMI_toolbox_panel", u"Save output", None))
    # retranslateUi

