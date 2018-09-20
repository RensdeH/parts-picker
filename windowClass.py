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

class Orderlijst(QtGui.QGridLayout):
	def __init__(self,data,parent=None):
		super(Orderlijst,self).__init__(parent)
		self.setAlignment(Qt.AlignTop)
		self.Data = data

	def removeItem(self,item):
		item.Aantal -= 1
		if item.Aantal == 0:
			self.Data.remove(item)
		self.rebuild()

	def addItem(self,item):
		item.Aantal += 1
		self.rebuild()

	def rebuild(self):
		for i in reversed(range(self.count())):
			notNeeded = self.takeAt(i).widget().setParent(None)
		rij=0
		for o in self.Data:
			removebutton = QtGui.QPushButton("-")
			removebutton.setFixedSize(40,40)
			removebutton.clicked.connect(lambda s, orde=o: self.removeItem(orde))

			countlabel = QtGui.QLabel(str(o.Aantal))
			countlabel.setFixedSize(25,40)

			addbutton = QtGui.QPushButton("+")
			addbutton.setFixedSize(40,40)
			addbutton.clicked.connect(lambda s, orde=o: self.addItem(orde))

			itemlabel = QtGui.QLabel(utils.clean(o.Name))
			itemlabel.setWordWrap(True)

			self.addWidget(removebutton,rij,0)
			self.addWidget(countlabel,rij,1)
			self.addWidget(addbutton,rij,2)
			self.addWidget(itemlabel,rij,3)

			rij+=1
