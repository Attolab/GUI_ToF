# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CustomDataTreeWidget.ui'
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
    QPushButton, QSizePolicy, QTreeView, QVBoxLayout,
    QWidget)

class Ui_CustomDataTreeWidget(object):
    def setupUi(self, CustomDataTreeWidget):
        if not CustomDataTreeWidget.objectName():
            CustomDataTreeWidget.setObjectName(u"CustomDataTreeWidget")
        CustomDataTreeWidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CustomDataTreeWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(CustomDataTreeWidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setDefaultDropAction(Qt.MoveAction)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.treeView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_pushButton = QPushButton(CustomDataTreeWidget)
        self.add_pushButton.setObjectName(u"add_pushButton")

        self.horizontalLayout.addWidget(self.add_pushButton)

        self.save_pushButton = QPushButton(CustomDataTreeWidget)
        self.save_pushButton.setObjectName(u"save_pushButton")

        self.horizontalLayout.addWidget(self.save_pushButton)

        self.copy_pushButton = QPushButton(CustomDataTreeWidget)
        self.copy_pushButton.setObjectName(u"copy_pushButton")

        self.horizontalLayout.addWidget(self.copy_pushButton)

        self.delete_pushButton = QPushButton(CustomDataTreeWidget)
        self.delete_pushButton.setObjectName(u"delete_pushButton")

        self.horizontalLayout.addWidget(self.delete_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(CustomDataTreeWidget)

        QMetaObject.connectSlotsByName(CustomDataTreeWidget)
    # setupUi

    def retranslateUi(self, CustomDataTreeWidget):
        CustomDataTreeWidget.setWindowTitle(QCoreApplication.translate("CustomDataTreeWidget", u"Form", None))
        self.add_pushButton.setText(QCoreApplication.translate("CustomDataTreeWidget", u"Add", None))
        self.save_pushButton.setText(QCoreApplication.translate("CustomDataTreeWidget", u"Save", None))
        self.copy_pushButton.setText(QCoreApplication.translate("CustomDataTreeWidget", u"Copy", None))
        self.delete_pushButton.setText(QCoreApplication.translate("CustomDataTreeWidget", u"Delete", None))
    # retranslateUi

