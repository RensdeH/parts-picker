import os.path
import json
import sys
import utils
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
        self.edit_first.setSingleStep(float(0.5))
        self.edit_first.setMinimum(0)
        self.edit_first.setDecimals(1)
        self.edit_first.setFixedWidth(100)

        grid.addWidget(QtGui.QLabel('Uren'), 1, 0)
        grid.addWidget(self.edit_first, 1, 1)

        #   add layout for second widget
        self.edit_second = QtGui.QLineEdit()
        grid.addWidget(QtGui.QLabel('Omschrijving'), 2, 0)
        grid.addWidget(self.edit_second, 2, 1)

        apply_button = QtGui.QPushButton('Toevoegen', self)
        apply_button.clicked.connect(lambda : checker(self.edit_first.text(),self.edit_second.text()))

        grid.addWidget(apply_button, 4, 3)
        self.setLayout(grid)
        self.setGeometry(300, 300, 600, 300)

    def return_strings(self):
        #   Return list of values. It need map with str (self.lineedit.text() will return QString)
        return [self.edit_first.value(), self.edit_second.text()]

    @staticmethod
    def get_data(parent=None):
        dialog = Widget(parent)
        if dialog.exec_() == 0:
			return None
        return dialog.return_strings()

def urenDialog():
    return Widget().get_data()  # window is value from edit field

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
