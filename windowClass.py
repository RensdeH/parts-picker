from PyQt4 import QtGui
from PyQt4.QtCore import *
import utils
from enum import Enum
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
		vorigeView.setFocusPolicy(Qt.NoFocus)
		return vorigeView

	def volgendeButton(self):
		volgendeView = QtGui.QPushButton()
		volgendeView.setFixedHeight(100)
		volgendeView.setText("Volgende>")
		volgendeView.clicked.connect(self.nextView)
		volgendeView.setStyleSheet("background-color: yellow");
		volgendeView.setFocusPolicy(Qt.NoFocus)
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

	def previousView(self):
		if self.previous is not None:
			self.changeView(self.previous)

	#Kan handig zijn om te jumpen naar andere windows
	def changeView(self,window):
		window.show()
		self.hide()
		window.show()

class Orderlijst(QtGui.QGridLayout):
	class Features(Enum):
		Add = 1
		Remove = 2
		Delete = 3
		Count = 4
		Name = 5
		Prijs = 6

	def __init__(self,data,parent=None):
		super(Orderlijst,self).__init__(parent)
		self.setAlignment(Qt.AlignTop)
		self.Data = data
		self.features = []

	def addFeature(self,feature):
		if feature == Orderlijst.Features.Add:
			self.features.append(self.makeAddButton)
		if feature == Orderlijst.Features.Remove:
			self.features.append(self.makeRemoveButton)
		if feature == Orderlijst.Features.Delete:
			self.features.append(self.makeDeleteButton)
		if feature == Orderlijst.Features.Count:
			self.features.append(self.makeCountLabel)
		if feature == Orderlijst.Features.Name:
			self.features.append(self.makeNameLabel)
		if feature == Orderlijst.Features.Prijs:
			self.features.append(self.makePrijsLabel)

	def makeAddButton(self,item):
		addButton = QtGui.QPushButton('+')
		addButton.setFixedSize(40,40)
		addButton.clicked.connect(lambda s, orde=item: self.addItem(orde))
		return addButton

	def addItem(self,item):
		item.Aantal += 1
		self.rebuild()

	def makeRemoveButton(self,item):
		removeButton = QtGui.QPushButton("-")
		removeButton.setFixedSize(40,40)
		removeButton.clicked.connect(lambda s, orde=item: self.removeItem(orde))
		return removeButton

	def removeItem(self,item):
		item.Aantal -= 1
		if item.Aantal == 0:
			self.Data.remove(item)
		self.rebuild()

	def makeDeleteButton(self,item):
		deleteButton = QtGui.QPushButton("X")
		deleteButton.setFixedSize(40,40)
		deleteButton.clicked.connect(lambda s, w=item: self.deleteItem(w))
		return deleteButton

	def deleteItem(self,item):
		self.Data.remove(item)
		self.rebuild()

	def makeCountLabel(self,item):
		countLabel = QtGui.QLabel(str(item.Aantal))
		countLabel.setFixedSize(25,40)
		return countLabel

	def makeNameLabel(self,item):
		nameLabel = QtGui.QLabel(utils.clean(item.Name))
		nameLabel.setWordWrap(True)
		return nameLabel

	def makePrijsLabel(self,item):
		prijsLabel = QtGui.QLabel('\xe2\x82\xac'.decode('utf8')+str(item.Prijs))
		prijsLabel.setAlignment(Qt.AlignRight)
		return prijsLabel

	def rebuild(self):
		for i in reversed(range(self.count())):
			notNeeded = self.takeAt(i).widget().setParent(None)
		rij=0
		for o in self.Data:
			colom = 0
			for f in self.features:
				widget = f(o)
				self.addWidget(widget,rij,colom)
				colom +=1
			rij+=1

def productLijst(list):
	lijst = Orderlijst(list)
	lijst.addFeature(Orderlijst.Features.Remove)
	lijst.addFeature(Orderlijst.Features.Count)
	lijst.addFeature(Orderlijst.Features.Add)
	lijst.addFeature(Orderlijst.Features.Name)
	return lijst

def vrijVeldLijst(list):
	lijst = Orderlijst(list)
	lijst.addFeature(Orderlijst.Features.Count)
	lijst.addFeature(Orderlijst.Features.Name)
	lijst.addFeature(Orderlijst.Features.Prijs)
	lijst.addFeature(Orderlijst.Features.Delete)
	return lijst

def werkLijst(list):
	lijst = Orderlijst(list)
	lijst.addFeature(Orderlijst.Features.Count)
	lijst.addFeature(Orderlijst.Features.Name)
	lijst.addFeature(Orderlijst.Features.Delete)
	lijst.addFeature(Orderlijst.Features.Prijs)
	return lijst
