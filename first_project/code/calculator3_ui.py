# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calculator3.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPlainTextEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 800)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 371, 451))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.button_0 = QPushButton(self.widget)
        self.button_0.setObjectName(u"button_0")

        self.gridLayout.addWidget(self.button_0, 5, 0, 1, 1)

        self.button_3 = QPushButton(self.widget)
        self.button_3.setObjectName(u"button_3")

        self.gridLayout.addWidget(self.button_3, 4, 2, 1, 1)

        self.button_2 = QPushButton(self.widget)
        self.button_2.setObjectName(u"button_2")

        self.gridLayout.addWidget(self.button_2, 4, 1, 1, 1)

        self.button_minus = QPushButton(self.widget)
        self.button_minus.setObjectName(u"button_minus")

        self.gridLayout.addWidget(self.button_minus, 4, 3, 1, 1)

        self.button_coma = QPushButton(self.widget)
        self.button_coma.setObjectName(u"button_coma")

        self.gridLayout.addWidget(self.button_coma, 5, 1, 1, 1)

        self.button_9 = QPushButton(self.widget)
        self.button_9.setObjectName(u"button_9")

        self.gridLayout.addWidget(self.button_9, 2, 2, 1, 1)

        self.button_6 = QPushButton(self.widget)
        self.button_6.setObjectName(u"button_6")

        self.gridLayout.addWidget(self.button_6, 3, 2, 1, 1)

        self.button_clr = QPushButton(self.widget)
        self.button_clr.setObjectName(u"button_clr")

        self.gridLayout.addWidget(self.button_clr, 1, 2, 1, 2)

        self.button_8 = QPushButton(self.widget)
        self.button_8.setObjectName(u"button_8")

        self.gridLayout.addWidget(self.button_8, 2, 1, 1, 1)

        self.button_1 = QPushButton(self.widget)
        self.button_1.setObjectName(u"button_1")

        self.gridLayout.addWidget(self.button_1, 4, 0, 1, 1)

        self.button_back = QPushButton(self.widget)
        self.button_back.setObjectName(u"button_back")

        self.gridLayout.addWidget(self.button_back, 1, 0, 1, 2)

        self.buttonequal = QPushButton(self.widget)
        self.buttonequal.setObjectName(u"buttonequal")

        self.gridLayout.addWidget(self.buttonequal, 5, 2, 1, 1)

        self.button_div = QPushButton(self.widget)
        self.button_div.setObjectName(u"button_div")

        self.gridLayout.addWidget(self.button_div, 2, 3, 1, 1)

        self.plainTextEdit = QPlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 4)

        self.button_7 = QPushButton(self.widget)
        self.button_7.setObjectName(u"button_7")
        self.button_7.setEnabled(True)

        self.gridLayout.addWidget(self.button_7, 2, 0, 1, 1)

        self.button_mno = QPushButton(self.widget)
        self.button_mno.setObjectName(u"button_mno")

        self.gridLayout.addWidget(self.button_mno, 3, 3, 1, 1)

        self.button_plus = QPushButton(self.widget)
        self.button_plus.setObjectName(u"button_plus")

        self.gridLayout.addWidget(self.button_plus, 5, 3, 1, 1)

        self.button_4 = QPushButton(self.widget)
        self.button_4.setObjectName(u"button_4")

        self.gridLayout.addWidget(self.button_4, 3, 0, 1, 1)

        self.button_5 = QPushButton(self.widget)
        self.button_5.setObjectName(u"button_5")

        self.gridLayout.addWidget(self.button_5, 3, 1, 1, 1)

        self.change_stylesheet = QPushButton(self.widget)
        self.change_stylesheet.setObjectName(u"change_stylesheet")

        self.gridLayout.addWidget(self.change_stylesheet, 6, 0, 1, 2)

        self.change_clock = QPushButton(self.widget)
        self.change_clock.setObjectName(u"change_clock")

        self.gridLayout.addWidget(self.change_clock, 6, 2, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_0.setText(QCoreApplication.translate("Form", u"0", None))
        self.button_3.setText(QCoreApplication.translate("Form", u"3", None))
        self.button_2.setText(QCoreApplication.translate("Form", u"2", None))
        self.button_minus.setText(QCoreApplication.translate("Form", u"-", None))
        self.button_coma.setText(QCoreApplication.translate("Form", u",", None))
        self.button_9.setText(QCoreApplication.translate("Form", u"9", None))
        self.button_6.setText(QCoreApplication.translate("Form", u"6", None))
        self.button_clr.setText(QCoreApplication.translate("Form", u"clear", None))
        self.button_8.setText(QCoreApplication.translate("Form", u"8", None))
        self.button_1.setText(QCoreApplication.translate("Form", u"1", None))
        self.button_back.setText(QCoreApplication.translate("Form", u"back", None))
        self.buttonequal.setText(QCoreApplication.translate("Form", u"=", None))
        self.button_div.setText(QCoreApplication.translate("Form", u"/", None))
        self.button_7.setText(QCoreApplication.translate("Form", u"7", None))
        self.button_mno.setText(QCoreApplication.translate("Form", u"*", None))
        self.button_plus.setText(QCoreApplication.translate("Form", u"+", None))
        self.button_4.setText(QCoreApplication.translate("Form", u"4", None))
        self.button_5.setText(QCoreApplication.translate("Form", u"5", None))
        self.change_stylesheet.setText(QCoreApplication.translate("Form", u"Change stylesheet", None))
        self.change_clock.setText(QCoreApplication.translate("Form", u"Change clock", None))
    # retranslateUi

