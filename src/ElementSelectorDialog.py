# -*- coding: utf-8 -*-

# Copyright 2004-2007 Nanorex, Inc.  See LICENSE file for details. 
# Form implementation generated from reading ui file 'ElementSelectorDialog.ui'
#
# Created: Wed Sep 20 10:12:41 2006
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_ElementSelectorDialog(object):
    def setupUi(self, ElementSelectorDialog):
        ElementSelectorDialog.setObjectName("ElementSelectorDialog")
        ElementSelectorDialog.resize(QtCore.QSize(QtCore.QRect(0,0,214,426).size()).expandedTo(ElementSelectorDialog.minimumSizeHint()))
        ElementSelectorDialog.setMinimumSize(QtCore.QSize(200,150))

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(0),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(1),QtGui.QColor(230,231,230))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(2),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(3),QtGui.QColor(242,243,242))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(4),QtGui.QColor(115,115,115))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(5),QtGui.QColor(153,154,153))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(6),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(7),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(8),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(9),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(10),QtGui.QColor(230,231,230))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(11),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(12),QtGui.QColor(0,0,128))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(13),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(14),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(15),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(16),QtGui.QColor(232,232,232))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(0),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(1),QtGui.QColor(230,231,230))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(2),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(3),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(4),QtGui.QColor(115,115,115))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(5),QtGui.QColor(153,154,153))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(6),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(7),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(8),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(9),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(10),QtGui.QColor(230,231,230))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(11),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(12),QtGui.QColor(0,0,128))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(13),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(14),QtGui.QColor(0,0,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(15),QtGui.QColor(255,0,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(16),QtGui.QColor(232,232,232))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(0),QtGui.QColor(128,128,128))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(1),QtGui.QColor(230,231,230))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(2),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(3),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(4),QtGui.QColor(115,115,115))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(5),QtGui.QColor(153,154,153))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(6),QtGui.QColor(128,128,128))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(7),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(8),QtGui.QColor(128,128,128))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(9),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(10),QtGui.QColor(230,231,230))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(11),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(12),QtGui.QColor(0,0,128))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(13),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(14),QtGui.QColor(0,0,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(15),QtGui.QColor(255,0,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(16),QtGui.QColor(232,232,232))
        ElementSelectorDialog.setPalette(palette)

        self.vboxlayout = QtGui.QVBoxLayout(ElementSelectorDialog)
        self.vboxlayout.setMargin(2)
        self.vboxlayout.setSpacing(2)
        self.vboxlayout.setObjectName("vboxlayout")

        self.elementFrame = QtGui.QFrame(ElementSelectorDialog)
        self.elementFrame.setMinimumSize(QtCore.QSize(200,150))
        self.elementFrame.setFrameShape(QtGui.QFrame.Box)
        self.elementFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.elementFrame.setObjectName("elementFrame")
        self.vboxlayout.addWidget(self.elementFrame)

        self.elementButtonGroup = QtGui.QGroupBox(ElementSelectorDialog)
        self.elementButtonGroup.setMinimumSize(QtCore.QSize(0,126))
        self.elementButtonGroup.setObjectName("elementButtonGroup")

        self.gridlayout = QtGui.QGridLayout(self.elementButtonGroup)
        self.gridlayout.setMargin(2)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.toolButton1 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton1.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton1.setCheckable(True)
        self.toolButton1.setObjectName("toolButton1")
        self.gridlayout.addWidget(self.toolButton1,0,4,1,1)

        self.toolButton2 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton2.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton2.setCheckable(True)
        self.toolButton2.setObjectName("toolButton2")
        self.gridlayout.addWidget(self.toolButton2,0,5,1,1)

        self.toolButton6 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton6.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton6.setCheckable(True)
        self.toolButton6.setObjectName("toolButton6")
        self.gridlayout.addWidget(self.toolButton6,1,1,1,1)

        self.toolButton7 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton7.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton7.setCheckable(True)
        self.toolButton7.setObjectName("toolButton7")
        self.gridlayout.addWidget(self.toolButton7,1,2,1,1)

        self.toolButton8 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton8.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton8.setCheckable(True)
        self.toolButton8.setObjectName("toolButton8")
        self.gridlayout.addWidget(self.toolButton8,1,3,1,1)

        self.toolButton10 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton10.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton10.setCheckable(True)
        self.toolButton10.setObjectName("toolButton10")
        self.gridlayout.addWidget(self.toolButton10,1,5,1,1)

        self.toolButton9 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton9.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton9.setCheckable(True)
        self.toolButton9.setObjectName("toolButton9")
        self.gridlayout.addWidget(self.toolButton9,1,4,1,1)

        self.toolButton13 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton13.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton13.setCheckable(True)
        self.toolButton13.setObjectName("toolButton13")
        self.gridlayout.addWidget(self.toolButton13,2,0,1,1)

        self.toolButton17 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton17.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton17.setCheckable(True)
        self.toolButton17.setObjectName("toolButton17")
        self.gridlayout.addWidget(self.toolButton17,2,4,1,1)

        self.toolButton5 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton5.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton5.setCheckable(True)
        self.toolButton5.setObjectName("toolButton5")
        self.gridlayout.addWidget(self.toolButton5,1,0,1,1)

        self.toolButton10_2 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton10_2.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton10_2.setCheckable(True)
        self.toolButton10_2.setObjectName("toolButton10_2")
        self.gridlayout.addWidget(self.toolButton10_2,2,5,1,1)

        self.toolButton15 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton15.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton15.setCheckable(True)
        self.toolButton15.setObjectName("toolButton15")
        self.gridlayout.addWidget(self.toolButton15,2,2,1,1)

        self.toolButton16 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton16.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton16.setCheckable(True)
        self.toolButton16.setObjectName("toolButton16")
        self.gridlayout.addWidget(self.toolButton16,2,3,1,1)

        self.toolButton14 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton14.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton14.setCheckable(True)
        self.toolButton14.setObjectName("toolButton14")
        self.gridlayout.addWidget(self.toolButton14,2,1,1,1)

        self.toolButton33 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton33.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton33.setCheckable(True)
        self.toolButton33.setObjectName("toolButton33")
        self.gridlayout.addWidget(self.toolButton33,3,2,1,1)

        self.toolButton34 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton34.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton34.setCheckable(True)
        self.toolButton34.setObjectName("toolButton34")
        self.gridlayout.addWidget(self.toolButton34,3,3,1,1)

        self.toolButton35 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton35.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton35.setCheckable(True)
        self.toolButton35.setObjectName("toolButton35")
        self.gridlayout.addWidget(self.toolButton35,3,4,1,1)

        self.toolButton36 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton36.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton36.setCheckable(True)
        self.toolButton36.setObjectName("toolButton36")
        self.gridlayout.addWidget(self.toolButton36,3,5,1,1)

        self.toolButton32 = QtGui.QToolButton(self.elementButtonGroup)
        self.toolButton32.setMinimumSize(QtCore.QSize(30,30))
        self.toolButton32.setCheckable(True)
        self.toolButton32.setObjectName("toolButton32")
        self.gridlayout.addWidget(self.toolButton32,3,1,1,1)
        self.vboxlayout.addWidget(self.elementButtonGroup)

        spacerItem = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.TransmuteButton = QtGui.QPushButton(ElementSelectorDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TransmuteButton.sizePolicy().hasHeightForWidth())
        self.TransmuteButton.setSizePolicy(sizePolicy)
        self.TransmuteButton.setObjectName("TransmuteButton")
        self.hboxlayout.addWidget(self.TransmuteButton)

        spacerItem1 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.transmuteCheckBox = QtGui.QCheckBox(ElementSelectorDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transmuteCheckBox.sizePolicy().hasHeightForWidth())
        self.transmuteCheckBox.setSizePolicy(sizePolicy)
        self.transmuteCheckBox.setObjectName("transmuteCheckBox")
        self.vboxlayout1.addWidget(self.transmuteCheckBox)
        self.vboxlayout.addLayout(self.vboxlayout1)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem2)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem3 = QtGui.QSpacerItem(106,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem3)

        self.closePTableButton = QtGui.QPushButton(ElementSelectorDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePTableButton.sizePolicy().hasHeightForWidth())
        self.closePTableButton.setSizePolicy(sizePolicy)
        self.closePTableButton.setDefault(True)
        self.closePTableButton.setObjectName("closePTableButton")
        self.hboxlayout1.addWidget(self.closePTableButton)

        spacerItem4 = QtGui.QSpacerItem(10,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem4)
        self.vboxlayout.addLayout(self.hboxlayout1)

        spacerItem5 = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem5)

        self.retranslateUi(ElementSelectorDialog)
        QtCore.QObject.connect(self.closePTableButton,QtCore.SIGNAL("clicked()"),ElementSelectorDialog.close)
        QtCore.QMetaObject.connectSlotsByName(ElementSelectorDialog)
        ElementSelectorDialog.setTabOrder(self.TransmuteButton,self.transmuteCheckBox)
        ElementSelectorDialog.setTabOrder(self.transmuteCheckBox,self.closePTableButton)

    def retranslateUi(self, ElementSelectorDialog):
        ElementSelectorDialog.setWindowTitle(QtGui.QApplication.translate("ElementSelectorDialog", "Element Selector", None, QtGui.QApplication.UnicodeUTF8))
        self.elementFrame.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "3D thumbnail view", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton1.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Hydrogen", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton1.setText(QtGui.QApplication.translate("ElementSelectorDialog", "H", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton1.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "H", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton2.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Helium", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton2.setText(QtGui.QApplication.translate("ElementSelectorDialog", "He", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton6.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Carbon", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton6.setText(QtGui.QApplication.translate("ElementSelectorDialog", "C", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton6.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "C", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton7.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Nitrogen", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton7.setText(QtGui.QApplication.translate("ElementSelectorDialog", "N", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton7.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "N", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton8.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Oxygen", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton8.setText(QtGui.QApplication.translate("ElementSelectorDialog", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton8.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton10.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Neon", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton10.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Ne", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton9.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Fluorine", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton9.setText(QtGui.QApplication.translate("ElementSelectorDialog", "F", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton9.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "F", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton13.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Aluminum", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton13.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Al", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton17.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Chlorine", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton17.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Cl", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton5.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Boron", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton5.setText(QtGui.QApplication.translate("ElementSelectorDialog", "B", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton5.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "B", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton10_2.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Argon", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton10_2.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Ar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton15.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Phosphorus", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton15.setText(QtGui.QApplication.translate("ElementSelectorDialog", "P", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton15.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "P", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton16.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Sulfur", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton16.setText(QtGui.QApplication.translate("ElementSelectorDialog", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton16.setShortcut(QtGui.QApplication.translate("ElementSelectorDialog", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton14.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Silicon", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton14.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Si", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton33.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Arsenic", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton33.setText(QtGui.QApplication.translate("ElementSelectorDialog", "As", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton34.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Selenium", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton34.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Se", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton35.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Bromine", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton35.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Br", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton36.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Krypton", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton36.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Kr", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton32.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Germanium", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton32.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Ge", None, QtGui.QApplication.UnicodeUTF8))
        self.TransmuteButton.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Transmute Selected Atoms", None, QtGui.QApplication.UnicodeUTF8))
        self.TransmuteButton.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Transmute", None, QtGui.QApplication.UnicodeUTF8))
        self.transmuteCheckBox.setToolTip(QtGui.QApplication.translate("ElementSelectorDialog", "Check if transmuted atoms should keep all existing bonds,  even if chemistry is wrong", None, QtGui.QApplication.UnicodeUTF8))
        self.transmuteCheckBox.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Force to Keep Bonds", None, QtGui.QApplication.UnicodeUTF8))
        self.closePTableButton.setText(QtGui.QApplication.translate("ElementSelectorDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
