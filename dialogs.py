import os.path
import json
import sys
import utils
import windowClass

from collections import OrderedDict

from PyQt4 import QtGui
from PyQt4.QtCore import *

class baseDialog(QtGui.QDialog):
	def __init__(self,parent=None):
		super(baseDialog,self).__init__(parent)
		self.totalLayout = QtGui.QFormLayout()
		windowClass.setWindowPosition(self,resize = False, ax = 300, ay = 300)
		self.setFixedSize(600,350)
		self.returnList = []
		self.setLayout(self.totalLayout)
		self.applyButton = self.apply_button()

	def apply_button(self):
		apply_button = QtGui.QPushButton('GA', self)
		apply_button.clicked.connect(lambda : self.validate(self.returnList))
		return apply_button

	def return_strings(self):
		lijst = []
		for x in self.returnList:
			lijst.append(x())
		return lijst

	def getData(self):
		self.deleteLater()
		if self.exec_() == 0:
			return None
		return self.return_strings()

	def validate(self,list):
		self.done(1)

class UrenDialog(baseDialog):
	def __init__(self, parent=None):
		super(UrenDialog,self).__init__(parent)

		self.edit_first = QtGui.QDoubleSpinBox()
		local = QLocale.c()
		self.edit_first.setLocale(local)
		self.edit_first.setSingleStep(float(0.25))
		self.edit_first.setMinimum(0)
		self.edit_first.setDecimals(2)
		self.edit_first.setFixedWidth(100)

		self.totalLayout.addRow(QtGui.QLabel('Uren'),self.edit_first)

		self.edit_second = QtGui.QLineEdit()
		self.totalLayout.addRow(QtGui.QLabel('Omschrijving'),self.edit_second)
		self.totalLayout.addRow(self.applyButton)

		self.returnList.append(self.edit_first.value)
		self.returnList.append(self.edit_second.text)

	@staticmethod
	def get_data():
		return UrenDialog().getData()

class VrijVeldDialog(baseDialog):
	def __init__(self, parent=None):
		def setTax(tax):
			self.tax = tax
		super(VrijVeldDialog,self).__init__(parent)

		self.edit_first = QtGui.QDoubleSpinBox(parent = self)
		local = QLocale.c()
		self.edit_first.setLocale(local)
		self.edit_first.setSingleStep(float(1))
		self.edit_first.setMinimum(1)
		self.edit_first.setDecimals(1)
		self.edit_first.setValue(1)
		self.edit_first.setFixedWidth(100)

		self.totalLayout.addRow(QtGui.QLabel('Aantal'),self.edit_first)

		self.edit_second = QtGui.QLineEdit(parent = self)

		self.totalLayout.addRow(QtGui.QLabel('Naam'),self.edit_second)

		self.editPrijs = QtGui.QDoubleSpinBox(parent = self)
		local = QLocale.c()
		self.editPrijs.setLocale(local)
		self.editPrijs.setSingleStep(float(1))
		self.editPrijs.setMinimum(0)
		self.editPrijs.setMaximum(100000)
		self.editPrijs.setDecimals(2)
		self.editPrijs.setFixedWidth(100)

		self.totalLayout.addRow(QtGui.QLabel('Prijs per stuk'),self.editPrijs)

		self.tax = 0
		self.tax0 = QtGui.QRadioButton('BTW margeregeling',parent=self)
		self.tax21 = QtGui.QRadioButton('BTW 21%',parent=self)
		self.tax0.clicked.connect(lambda s : setTax(0))
		self.tax21.clicked.connect(lambda s : setTax(21))

		self.tax0.toggle()

		self.totalLayout.addRow(self.tax0,self.tax21)
		self.totalLayout.addRow(self.applyButton)

		self.returnList.append(self.edit_first.value)
		self.returnList.append(self.edit_second.text)
		self.returnList.append(self.editPrijs.value)
		self.returnList.append(self.getTax)

	def getTax(self):
		return self.tax

	@staticmethod
	def get_data():
		return VrijVeldDialog().getData()

class SearchDialog(baseDialog):
	def __init__(self, parent=None):
		def validate(z):
			if z != '':
				self.done(1)
		super(SearchDialog,self).__init__(parent)

		self.zoekNaar = QtGui.QLabel('Zoeken naar:',parent=self)
		self.editZoekNaar = QtGui.QLineEdit(parent=self)
		self.editZoekNaar.setFocus()
		self.zoekAlles = QtGui.QCheckBox('Zoeken in alle categorieen',parent=self)
		self.zoekAlles.click()

		self.totalLayout.addRow(self.zoekNaar,self.editZoekNaar)
		self.totalLayout.addRow(self.zoekAlles,self.applyButton)

		self.returnList.append(self.editZoekNaar.text)
		self.returnList.append(self.zoekAlles.isChecked)

	@staticmethod
	def get_data():
		return SearchDialog().getData()

def urenDialog():
	return UrenDialog.get_data()  # window is value from edit field

def vrijVeldDialog():
	return VrijVeldDialog.get_data()

def zoekDialog():
	return SearchDialog.get_data()

def errorDialog():
	QtGui.QMessageBox.warning(None,"Geen soort gekozen",'Je hebt geen soort factuur (I,A,R,V) gekozen')

def controleerJsonLayout(data):
	layout = QtGui.QFormLayout()
	for line in data.keys():
		label = QtGui.QLabel(line)
		value = QtGui.QLineEdit(data[line])
		layout.addRow(label,value)
	return layout

def getJsonLayout(formLayout):
	data = OrderedDict()
	aantalRows = formLayout.rowCount()
	for x in range(aantalRows):
		rowLabel = formLayout.itemAt(x,QtGui.QFormLayout.LabelRole)
		rowField = formLayout.itemAt(x,QtGui.QFormLayout.FieldRole)
		data[str(rowLabel.widget().text())] = str(rowField.widget().text())
	return data
