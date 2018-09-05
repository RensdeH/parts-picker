import os.path
import json
import sys
import utils

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

		setWindowPosition(self,resize = False, ax = 300, ay = 300)
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
		def checker(u,o,p):
			if str(u) == '0,0':
				return
			if str(o) == '':
				return
			self.done(1)
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

		apply_button = QtGui.QPushButton('Toevoegen', self)
		apply_button.clicked.connect(lambda : checker(self.edit_first.text(),self.edit_second.text(),self.editPrijs.text()))

		grid.addWidget(apply_button, 4, 3)
		self.setLayout(grid)

		setWindowPosition(self,resize = False, ax = 300, ay = 300)
		self.setFixedSize(600,350)

	def return_strings(self):
		#   Return list of values. It need map with str (self.lineedit.text() will return QString)
		return [self.edit_first.value(), self.edit_second.text(),self.editPrijs.text()]

	@staticmethod
	def get_data(parent=None):
		dialog = VrijWidget(parent)
		if dialog.exec_() == 0:
			return None
		return dialog.return_strings()

def urenDialog():
	return Widget().get_data()  # window is value from edit field

def vrijVeldDialog():
	return VrijWidget().get_data()

def errorDialog():
	QtGui.QMessageBox.warning(None,"Geen soort gekozen",'Je hebt geen soort factuur (I,A,R,V) gekozen')

def setWindowPosition(window,resize = True,ax=0,ay=0):
	pdesk = QtGui.QDesktopWidget()
	rect = pdesk.screenGeometry(pdesk.primaryScreen())
	window.move(rect.left()+ax,rect.top()+ay)
	if resize:
		window.resize(rect.width(),rect.height())

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
