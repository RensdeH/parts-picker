import os.path
import json
import sys
import utils
import windowClass

from collections import OrderedDict

from PyQt4 import QtGui
from PyQt4.QtCore import *

class Widget(QtGui.QDialog):
	def __init__(self, parent=None):
		def checker(u,o):
			if str(u) == '0,0':
				return
			if str(o) == '':
				return
			self.done(1)
		super(Widget,self).__init__(parent)

		grid = QtGui.QGridLayout()
		grid.setSpacing(3)

		self.edit_first = QtGui.QDoubleSpinBox()
		self.edit_first.setSingleStep(float(0.25))
		self.edit_first.setMinimum(0)
		self.edit_first.setDecimals(2)
		self.edit_first.setFixedWidth(100)

		grid.addWidget(QtGui.QLabel('Uren'), 1, 0)
		grid.addWidget(self.edit_first, 1, 1)

		self.edit_second = QtGui.QLineEdit()
		grid.addWidget(QtGui.QLabel('Omschrijving'), 2, 0)
		grid.addWidget(self.edit_second, 2, 1)

		apply_button = QtGui.QPushButton('Toevoegen', self)
		apply_button.clicked.connect(lambda : checker(self.edit_first.text(),self.edit_second.text()))

		grid.addWidget(apply_button, 4, 3)
		self.setLayout(grid)

		windowClass.setWindowPosition(self,resize = False, ax = 300, ay = 300)
		self.setFixedSize(600,350)

	def return_strings(self):
		#   Return list of values. It need map with str (self.lineedit.text() will return QString)
		return [self.edit_first.value(), self.edit_second.text()]

	@staticmethod
	def get_data(parent=None):
		dialog = Widget(parent)
		if dialog.exec_() == 0:
			return None
		return dialog.return_strings()

class VrijWidget(QtGui.QDialog):
	def __init__(self, parent=None):
		def checker(u,o):
			if str(u) == '0,0':
				return
			if str(o) == '':
				return
			self.done(1)

		def setTax(tax):
			self.tax = tax
		super(VrijWidget,self).__init__(parent)

		grid = QtGui.QGridLayout()
		grid.setSpacing(3)

		self.edit_first = QtGui.QDoubleSpinBox()
		self.edit_first.setSingleStep(float(1))
		self.edit_first.setMinimum(1)
		self.edit_first.setDecimals(0)
		self.edit_first.setValue(1)
		self.edit_first.setFixedWidth(100)

		grid.addWidget(QtGui.QLabel('Aantal'), 1, 0)
		grid.addWidget(self.edit_first, 1, 1)

		self.edit_second = QtGui.QLineEdit()
		grid.addWidget(QtGui.QLabel('Naam'), 2, 0)
		grid.addWidget(self.edit_second, 2, 1)

		self.editPrijs = QtGui.QDoubleSpinBox()
		self.editPrijs.setSingleStep(float(1))
		self.editPrijs.setMinimum(0)
		self.editPrijs.setMaximum(1000)
		self.editPrijs.setDecimals(2)
		self.editPrijs.setFixedWidth(100)

		grid.addWidget(QtGui.QLabel('Prijs per stuk'), 3, 0)
		grid.addWidget(self.editPrijs, 3, 1)
		self.tax = 0
		self.tax0 = QtGui.QRadioButton('BTW margeregeling')
		self.tax21 = QtGui.QRadioButton('BTW 21%')
		self.tax0.clicked.connect(lambda s : setTax(0))
		self.tax21.clicked.connect(lambda s : setTax(21))

		self.tax0.toggle()

		grid.addWidget(self.tax0,4,0)
		grid.addWidget(self.tax21,4,1)

		apply_button = QtGui.QPushButton('Toevoegen', self)
		apply_button.clicked.connect(lambda : checker(self.edit_first.text(),self.edit_second.text()))

		grid.addWidget(apply_button, 5, 3)
		self.setLayout(grid)

		windowClass.setWindowPosition(self,resize = False, ax = 300, ay = 300)
		self.setFixedSize(600,350)

	def return_strings(self):
		#   Return list of values. It need map with str (self.lineedit.text() will return QString)
		print(self.tax)
		return [self.edit_first.value(), self.edit_second.text(),float(self.editPrijs.value()),self.tax]

	@staticmethod
	def get_data(parent=None):
		dialog = VrijWidget(parent)
		if dialog.exec_() == 0:
			return None
		return dialog.return_strings()

class SearchDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		def checker(z):
			if z!='':
				self.done(1)
			return
		super(SearchDialog,self).__init__(parent)

		totalLayout = QtGui.QVBoxLayout()
		topLayout = QtGui.QVBoxLayout()
		bottomLayout = QtGui.QVBoxLayout()

		self.zoekNaar = QtGui.QLabel('Zoeken naar:')
		self.editZoekNaar = QtGui.QLineEdit()
		topLayout.addWidget(self.zoekNaar)
		topLayout.addWidget(self.editZoekNaar)

		self.zoekAlles = QtGui.QCheckBox('Zoeken in alle categorieen')
		zoeken = QtGui.QPushButton('Zoeken', self)
		zoeken.clicked.connect(lambda : checker(self.zoekNaar.text()))
		bottomLayout.addWidget(self.zoekAlles)
		bottomLayout.addWidget(zoeken)
		totalLayout.addLayout(topLayout)
		totalLayout.addLayout(bottomLayout)
		self.setLayout(totalLayout)

		windowClass.setWindowPosition(self,resize = False, ax = 300, ay = 300)
		self.setFixedSize(600,350)

	def return_strings(self):
		#   Return list of values. It need map with str (self.lineedit.text() will return QString)
		return [self.editZoekNaar.text(), self.zoekAlles.isChecked()]

	@staticmethod
	def get_data(parent=None):
		dialog = SearchDialog(parent)
		if dialog.exec_() == 0:
			return None
		return dialog.return_strings()

def urenDialog():
	return Widget().get_data()  # window is value from edit field

def vrijVeldDialog():
	return VrijWidget().get_data()

def zoekDialog():
	return SearchDialog().get_data()

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

def controlJsonDialog(filename):
	data = utils.readJson(filename)
	if not data:
		return

	dialog = QtGui.QDialog()
	layout = controleerJsonLayout(data)
	layout.setParent(dialog)
	#add button to layout to confirm and save
	dialog.exec_()

def controlJsonApp(filename):
	app = QtGui.QApplication(sys.argv)
	w = QtGui.QWidget()
	w.show()
	controlJsonDialog(filename)
	sys.exit(app.exec_())
