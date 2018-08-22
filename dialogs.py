import os.path
import json
import sys
import utils
from PyQt4 import QtGui
from PyQt4.QtCore import *

def controleerJsonLayout(data):
	layout = QtGui.QFormLayout()
	for line in data.keys():
		label = QtGui.QLabel(line)
		value = QtGui.QLineEdit(data[line])
		layout.addRow(label,value)
	return layout

def getJsonLayout(formLayout):
	data={}
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
