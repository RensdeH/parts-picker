from PyQt4 import QtGui
from PyQt4.QtCore import *

import utils
#pointer naar factuur.data voor debuggen
data = None

def setWindowPosition(window,resize = True,ax=0,ay=0):
	pdesk = QtGui.QDesktopWidget()
	rect = pdesk.screenGeometry(pdesk.primaryScreen())
	window.move(rect.left()+ax,rect.top()+ay)
	if resize:
		window.resize(rect.width(),rect.height())

class Window(QtGui.QWidget):
	def __init__(self,Titel, parent=None):
		super(Window,self).__init__(parent)
		setWindowPosition(self)
		self.volgendeView = self.volgendeButton()
		self.vorigeView = self.vorigeButton()
		self.totalLayout = QtGui.QHBoxLayout()
		self.previous = None
		self.next = None
		self.rebuild = None
		self.opslaan = None
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

	def setOpslaan(self,opslaan):
		self.opslaan = opslaan

	def setPreviousView(self,window):
		self.previous = window

	def setNextView(self,window):
		self.next = window

	def nextView(self):
		if self.opslaan != None:
			self.opslaan()
		if self.next is not None:
			self.changeView(self.next)
		utils.printData(data)

	def previousView(self):
		if self.previous is not None:
			self.changeView(self.previous)
		utils.printData(data)

	#Kan handig zijn om te jumpen naar andere windows
	def changeView(self,window):
		window.show()
		self.hide()
		window.show()
