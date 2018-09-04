import dialogs
from PyQt4 import QtGui
from PyQt4.QtCore import *

import utils
data = None

class Window(QtGui.QWidget):

	def __init__(self,Titel, parent=None):
		super(Window,self).__init__(parent)
		dialogs.setWindowPosition(self) #TODO evt. naar hier halen
		self.volgendeView = self.volgendeButton()
		self.vorigeView = self.vorigeButton()
		self.totalLayout = QtGui.QHBoxLayout()
		self.previous = None
		self.next = None
		self.rebuild = None

		self.totalLayout.setAlignment(Qt.AlignTop)
		self.setWindowTitle("MX5-factuur \'"+Titel+"'\'")
		self.setLayout(self.totalLayout)

	def vorigeButton(self):
		vorigeView = QtGui.QPushButton()
		vorigeView.setText("<Vorige")
		vorigeView.clicked.connect(self.previousView)
		vorigeView.setFixedHeight(100)
		vorigeView.setStyleSheet("background-color: yellow");
		return vorigeView

	def volgendeButton(self):
		volgendeView = QtGui.QPushButton()
		volgendeView.setFixedHeight(100)
		volgendeView.setText("Volgende>")
		volgendeView.clicked.connect(self.nextView)
		volgendeView.setStyleSheet("background-color: yellow");
		return volgendeView

	def show(self):
		super(Window,self).show()
		if self.rebuild != None:
			self.rebuild()

	def setRebuild(self,rebuild):
		self.rebuild = rebuild

	def setPreviousView(self,window):
		self.previous = window

	def setNextView(self,window,opslaan= None):
		self.opslaan = opslaan
		self.next = window

	def nextView(self):
		if self.opslaan != None:
			self.opslaan()
		self.changeView(self.next)
		utils.printData(data)

	def previousView(self):
		self.changeView(self.previous)
		utils.printData(data)

	#Kan handig zijn om te jumpen naar andere windows
	def changeView(self,window):
		self.hide()
		window.show()
