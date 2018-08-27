#library imports
import datetime as dt
n1 = dt.datetime.now()
import sys
import requests
import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import *

#custom imports
import latexfact
import api
import utils
import dialogs

#constants
ITEMS_PER_RIJ = 5

#global QtGui Widgets
app = QtGui.QApplication(sys.argv)

soortWindow = QtGui.QWidget()
productWindow = QtGui.QWidget()
customerWindow = QtGui.QWidget()
autoKoopWindow = QtGui.QWidget()
urenWindow = QtGui.QWidget()

orderlijst = QtGui.QGridLayout()
werkLayout = QtGui.QGridLayout()
orderDisplay = QtGui.QLabel()
tabs = QtGui.QTabWidget()

#dataDisplay = QtGui.QLabel()

tablist = []

# global data -Minimize this!
data = {} #factuur data (order, auto, Uren(aantal,omschrijving),klant,soort)
data['Werk']=[]
Cids = {} # key: catId, value: [articles]
catNames = {} #key: catId, value:catName

def main():
	def loadArtikels(silent=True):
		data = utils.readJson('Resources/Artikelen.json')
		if data == {}:
			data = api.getArtikels(silent=silent)
			utils.writeJson('Resources/Artikelen.json',data)
		return data

	app.setWindowIcon(QtGui.QIcon('Resources/icon.png'))
	n2 = dt.datetime.now()
	print("Declaring:"+str((n2-n1).total_seconds()))
	lijst = loadArtikels()
	data['order'] = []
	n3 = dt.datetime.now()
	print("Get artikelen:"+str((n3-n2).total_seconds()))
	Cids.update(defineTabs(lijst))
	n4 = dt.datetime.now()
	print("Define Tabs:"+str((n4-n3).total_seconds()))
	fillTabs(Cids)
	n5 = dt.datetime.now()
	print("Fill Tabs:"+str((n5-n4).total_seconds()))
	soortWindowSetup()
	productWindowSetup()
	customerWindowSetup()
	autoKoopWindowSetup()
	urenWindowSetup()
	n6 = dt.datetime.now()
	print("Windows Setup:"+str((n6-n5).total_seconds()))
	soortWindow.show()
	#productWindow.show()
	#customerWindow.show()
	n7 = dt.datetime.now()
	print("Show Window:"+str((n7-n6).total_seconds()))
	print("Total Time:"+str((n7-n1).total_seconds()))
	sys.exit(app.exec_())

	#debugging tool
	#print(len(app.allWidgets()))

######################################################
#-----------------------Setup-------------------------
######################################################

def setWindowPosition(window):
	pdesk = QtGui.QDesktopWidget()
	rect = pdesk.screenGeometry(pdesk.primaryScreen())
	window.move(rect.left(),rect.top())
	window.resize(rect.width(),rect.height())

def addUren():
	werk = dialogs.urenDialog()
	if werk == None:
		return
	data['Werk'].append(werk)
	rebuildWerkUrenWindow()

def removeUren(werk):
	data['Werk'].remove(werk)
	rebuildWerkUrenWindow()

def editUren(werk):
	werkd = dialogs.urenDialog()
	if werkd == None:
		return
	data['Werk'].remove(werk)
	data['Werk'].append(werkd)
	rebuildWerkUrenWindow()

def rebuildWerkUrenWindow():
	for i in reversed(range(werkLayout.count())):
		notNeeded = werkLayout.takeAt(i).widget().setParent(None)
	rij = 0
	#werk = (floatUren,stringOmschrijving)
	for werk in data['Werk']:
		countlabel = QtGui.QLabel(str(werk[0]))
		countlabel.setFixedSize(25,40)

		omschrijvingLabel = QtGui.QLabel(utils.clean(werk[1]))
		omschrijvingLabel.setWordWrap(True)

		editButton = QtGui.QPushButton("edit")
		editButton.setFixedSize(40,40)
		editButton.clicked.connect(lambda s, w=werk: editUren(w))

		removebutton = QtGui.QPushButton("X")
		removebutton.setFixedSize(40,40)
		removebutton.clicked.connect(lambda s, w=werk: removeUren(w))

		werkLayout.addWidget(countlabel,rij,0)
		werkLayout.addWidget(omschrijvingLabel,rij,1)
		werkLayout.addWidget(editButton,rij,2)
		werkLayout.addWidget(removebutton,rij,3)
		rij+=1

def urenWindowSetup():
	setWindowPosition(urenWindow)
	totalLayout = QtGui.QHBoxLayout()
	leftLayout = QtGui.QVBoxLayout()

	addUrenb = QtGui.QPushButton()
	addUrenb.setFixedHeight(100)
	addUrenb.clicked.connect(addUren)
	addUrenb.setText("Werk toevoegen")

	vorigeView = QtGui.QPushButton()
	vorigeView.setText("<Vorige")
	vorigeView.clicked.connect(soortView)
	vorigeView.setFixedWidth(150)

	volgendeView = QtGui.QPushButton()
	volgendeView.setText("Volgende>")
	volgendeView.clicked.connect(productView)
	volgendeView.setFixedWidth(150)

	groupbox2 = QtGui.QGroupBox()

	scroll2 = QtGui.QScrollArea()
	scroll2.setWidget(groupbox2)
	scroll2.setWidgetResizable(True)

	orderlijst.setAlignment(Qt.AlignTop)
	groupbox2.setLayout(werkLayout)

	totalLayout.addLayout(leftLayout)
	totalLayout.addStretch()
	totalLayout.addStretch()

	leftLayout.addWidget(vorigeView)
	leftLayout.addWidget(scroll2)
	leftLayout.addWidget(addUrenb)
	leftLayout.addWidget(volgendeView)

	werkLayout.setAlignment(Qt.AlignTop)
	urenWindow.setLayout(totalLayout)
	urenWindow.setWindowTitle("MX5-factuur \'Uren toevoegen\'")

def soortWindowSetup():
	def setSoort(s):
		data['soortFactuur'] = s
		if s == utils.SoortFactuur.Inkoop:
			autoKoopView()
		elif s == utils.SoortFactuur.Verkoop:
			productView()
		else:
			urenView()

	setWindowPosition(soortWindow)
	totalLayout = QtGui.QHBoxLayout()
	buttonLayout = QtGui.QVBoxLayout()

	for en in utils.SoortFactuur:
		b1 = QtGui.QPushButton()
		b1.setText(en.name)
		b1.clicked.connect(lambda st, so = en: setSoort(so))
		b1.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.MinimumExpanding)
		buttonLayout.addWidget(b1)
		buttonLayout.addStretch()

	totalLayout.addStretch()
	totalLayout.addLayout(buttonLayout)
	totalLayout.addStretch()

	soortWindow.setWindowTitle("MX5-factuur \'Soort factuur\'")
	soortWindow.setLayout(totalLayout)

def productWindowSetup():
	setWindowPosition(productWindow)

	totalLayout = QtGui.QHBoxLayout()
	leftLayout = QtGui.QVBoxLayout()
	rightlayout = QtGui.QVBoxLayout()

	totalLayout.addLayout(leftLayout,3)
	#totalLayout.addWidget(tabs,3)
	totalLayout.addLayout(rightlayout,1)

	vorigeView = QtGui.QPushButton()
	vorigeView.setText("<Vorige")
	vorigeView.clicked.connect(soortView)
	vorigeView.setFixedWidth(150)

	leftLayout.addWidget(vorigeView,1)
	leftLayout.addWidget(tabs,4)

	productWindow.setWindowTitle("MX5-factuur \'Producten kiezen\'")
	productWindow.setLayout(totalLayout)

	groupbox2 = QtGui.QGroupBox()

	scroll2 = QtGui.QScrollArea()
	scroll2.setWidget(groupbox2)
	scroll2.setWidgetResizable(True)

	orderlijst.setAlignment(Qt.AlignTop)
	groupbox2.setLayout(orderlijst)

	resetorder = QtGui.QPushButton()
	resetorder.setFixedHeight(80)
	resetorder.setText("Leegmaken")
	resetorder.clicked.connect(emptyOrder)

	bevestig = QtGui.QPushButton()
	bevestig.setFixedHeight(200)
	bevestig.setText("Volgende>")
	bevestig.clicked.connect(lambda: customerView())

	actie = QtGui.QAction(productWindow)
	actie.setShortcut("Ctrl+F")
	productWindow.addAction(actie)
	actie.triggered.connect(lambda: searchTab())

	rightlayout.addWidget(resetorder)
	rightlayout.addWidget(scroll2)
	rightlayout.addWidget(bevestig)

	tabs.setFocusPolicy(Qt.NoFocus)

def customerWindowSetup():
	def lastView():
		s = data['soortFactuur']
		if s == utils.SoortFactuur.Inkoop or s == utils.SoortFactuur.Verkoop:
			autoKoopView()
		else:
			productView()

	def makeFactuur(rightLayout):
		customerEdit = rightLayout.itemAt(1)
		data['klant'] = dialogs.getJsonLayout(customerEdit)
		#if data['id'] == '':
		#	data['klant']['id'] = data['klant']['Naam']
		latexfact.startFactuur(data['order'],data['Werk'],data['klant'],data['soortFactuur'],'Test')

	def kiesKlant(layout):
		fileName = QtGui.QFileDialog.getOpenFileName(customerWindow, 'Open File', 'Resources/Klanten')
		klantData = utils.readJson(fileName)
		custEdit = dialogs.controleerJsonLayout(klantData)
		l = layout.takeAt(1)
		for i in reversed(range(l.count())):
			notNeeded = l.takeAt(i).widget().setParent(None)
		layout.insertLayout(1,custEdit)

	setWindowPosition(customerWindow)

	totalLayout = QtGui.QHBoxLayout()

	vorigeView = QtGui.QPushButton()
	vorigeView.setText("<Vorige")
	vorigeView.clicked.connect(lastView)
	vorigeView.setFixedWidth(150)

	orderDisplay.setAlignment(Qt.AlignTop)
	orderDisplay.setWordWrap(True)

	leftLayout = QtGui.QVBoxLayout()
	leftLayout.addWidget(vorigeView,1)
	leftLayout.addWidget(orderDisplay,5)
	rightLayout = QtGui.QVBoxLayout()

	data['klant'] = utils.readJson('Resources/emptyCustomer.json')
	customerEdit = dialogs.controleerJsonLayout(data['klant'])

	factuurMaken = QtGui.QPushButton()

	bestaandeKlantKiezen = QtGui.QPushButton()
	rightLayout.addWidget(bestaandeKlantKiezen,1)
	rightLayout.addLayout(customerEdit,4)
	rightLayout.addWidget(factuurMaken,1)

	bestaandeKlantKiezen.setText("Bestaande Klant Kiezen")
	bestaandeKlantKiezen.clicked.connect(lambda s, edit = rightLayout: kiesKlant(edit))
	bestaandeKlantKiezen.setFixedHeight(100)

	factuurMaken.setText("Factuur maken")
	factuurMaken.clicked.connect(lambda s, edit = rightLayout: makeFactuur(edit)) #latexfact.startFactuur(order))
	factuurMaken.setFixedHeight(200)

	totalLayout.addLayout(leftLayout,1)
	totalLayout.addLayout(rightLayout,5)

	customerWindow.setLayout(totalLayout)
	customerWindow.setWindowTitle("MX5-factuur \'Klant kiezen\'")

def autoKoopWindowSetup():
	setWindowPosition(autoKoopWindow)
	totalLayout = QtGui.QHBoxLayout()

	data['Auto'] = utils.readJson('Resources/emptyAuto.json')
	autoEdit = dialogs.controleerJsonLayout(data['Auto'])

	vorigeView = QtGui.QPushButton()
	vorigeView.setText("<Vorige")
	vorigeView.clicked.connect(soortView)
	vorigeView.setFixedWidth(200)

	klantKiezen = QtGui.QPushButton()
	klantKiezen.setText("Klant kiezen")
	klantKiezen.clicked.connect(lambda s, edit = autoEdit: saveAuto(edit))
	klantKiezen.setFixedHeight(200)

	rightLayout = QtGui.QVBoxLayout()
	rightLayout.addWidget(vorigeView,1)
	rightLayout.addLayout(autoEdit,4)
	rightLayout.addWidget(klantKiezen,1)

	totalLayout.addLayout(rightLayout)

	autoKoopWindow.setLayout(totalLayout)
	autoKoopWindow.setWindowTitle("MX5-factuur \'Auto-informatie\'")


def saveAuto(autoEdit):
	data['Auto'] = dialogs.getJsonLayout(autoEdit)
	customerView()


#########################################################
#----------------------Switch Views----------------------
#########################################################

def soortView():
	autoKoopWindow.hide()
	productWindow.hide()
	soortWindow.show()
	urenWindow.hide()

def urenView():
	autoKoopWindow.hide()
	productWindow.hide()
	soortWindow.hide()
	urenWindow.show()

def customerView():
	autoKoopWindow.hide()
	productWindow.hide()
	urenWindow.hide()
	rebuildOrderDisplay()
	customerWindow.show()

def productView():
	productWindow.show()
	soortWindow.hide()
	customerWindow.hide()
	urenWindow.hide()

def autoKoopView():
	customerWindow.hide()
	soortWindow.hide()
	autoKoopWindow.show()

def rebuildOrderDisplay():
	s = ''
	for o in data['order']:
		try:
			s += str(o['Aantal']) + ' x ' + utils.clean(o['item']['name']) + '\n'
		except:
			s += "\n"
	if data['order'] == []:
		s = 'Geen producten gekozen'
	orderDisplay.setText(s)

#############################################################
#-------------------------Zoeken-----------------------------
#############################################################

def searchTab():
	print(len(app.allWidgets()))

	activeTab = tabs
	while type(activeTab.currentWidget()) is QtGui.QTabWidget:
		activeTab = activeTab.currentWidget()

	activePosition = activeTab.currentIndex()
	activeCatName = activeTab.tabText(activePosition)
	activeScroll = activeTab.currentWidget()
	activeCatId = activeScroll.whatsThis()

	lijst = Cids[str(activeCatId)]

	text, ok = QtGui.QInputDialog.getText(productWindow,"Zoeken","Zoeken in:" + str(activeCatName))
	if not ok:
		return
	text = str(text).lower()

	results = []
	for item in lijst:
		if text in item['name'].lower() or text in item['description'].lower():
			results.append(item)

	newScroll = makeTab(activeCatId)

	b1 = QtGui.QPushButton(newScroll)
	b1.clicked.connect(lambda state, tab = activeTab, i=activePosition,name=activeCatName,catId = activeCatId: previousTab(tab,i,name,catId))
	b1.setFixedSize(100,100)
	b1.setFocusPolicy(Qt.NoFocus)
	b1.setStyleSheet("border: none;")
	b1.setIcon(QtGui.QIcon('Resources/searchback.png'))
	b1.setIconSize(QSize(100,100))

	l1 = QtGui.QLabel('',parent = newScroll)
	l1.setFixedSize(100,100)
	l1.setWordWrap(True)

	makeGrid(results,newScroll,(b1,l1))

	activeTab.insertTab(activePosition,newScroll,'Zoek:'+str(text))
	baseWidget = activeTab.widget(activePosition+1)
	activeTab.removeTab(activePosition+1)
	baseWidget.deleteLater()
	activeTab.setCurrentIndex(activePosition)

def previousTab(tab, pos,name, catId):
	scroll = makeTab(catId)
	makeGrid(Cids[str(catId)],scroll,None)

	sluitZoeken(scroll,tab,pos,catNames[str(catId)])
	print(len(app.allWidgets()))

def sluitZoeken(scrollArea,tab,pos,name):
	zoek = tab.widget(pos)
	tab.removeTab(pos)
	zoek.deleteLater()
	tab.insertTab(pos,scrollArea,name)
	tab.setCurrentIndex(pos)

############################################################
#------------------------Categories/Tabs--------------------
############################################################

def defineTabs(lijst):
	def listCatIds(lijst):
		cids = {}
		for a in lijst:
			for c in a['categories']:
				cids.setdefault(str(c['category_id']),[]).append(a)

		return cids

	cids = listCatIds(lijst)
	categories = api.getCategories()
	for c in categories:
		loopCats(c,cids.keys(),'',tabs,lijst)
	return cids

def loopCats(c,ids,prefix,parentTab,lijst):
	currentTab = QtGui.QTabWidget(parentTab)
	currentTab.setFocusPolicy(Qt.NoFocus)

	containsItems = False
	if str(c['id']) in ids:
		containsItems = True

	childContainsItems = False
	for l in c.get('leafs',[]):
		childContainsItems = loopCats(l,ids,prefix+'-',currentTab,lijst)

	if childContainsItems:
		parentTab.addTab(currentTab,"s: "+ utils.clean(c['title']))
		if containsItems:
			defaultTab = makeTab(c['id'])
			tablist.append((c['id'],defaultTab))
			currentTab.insertTab(0,defaultTab,"d: "+ utils.clean(c['title']))
			catNames[str(c['id'])] = c['title']
	elif containsItems:
		leafTab = makeTab(c['id'])
		tablist.append((c['id'],leafTab))
		parentTab.addTab(leafTab,"l: "+utils.clean(c['title']))
		catNames[str(c['id'])] = c['title']

	return childContainsItems or containsItems

def fillTabs(cids):
	if not os.path.exists('Images/'):
		os.makedirs('Images/')
	for t in tablist:
		makeGrid(cids[str(t[0])],t[1],None)

###############################################################
#----------------------------Single Tab------------------------
###############################################################

def makeTab(cid):
	scroll = QtGui.QScrollArea()
	groupbox = QtGui.QGroupBox(scroll)
	grid = QtGui.QGridLayout(groupbox)

	scroll.setWidget(groupbox)
	scroll.setWidgetResizable(True)

	scroll.setWhatsThis(str(cid))
	return scroll

def makeGrid(lijst,scroll,button):
	grid = scroll.widget().layout()

	buttons = []
	if button is not None:
		buttons.append(button)

	for item in lijst:
		b = makeButton(item)
		l = makeLabel(item)
		buttons.append((b,l))

	l = len(buttons)
	itemsPerKolom = int(l / ITEMS_PER_RIJ) + 1
	for j in range(itemsPerKolom):
		for i in range(ITEMS_PER_RIJ):
			if ITEMS_PER_RIJ * j + i > l - 1:
				return
			grid.addWidget(buttons[ITEMS_PER_RIJ * j + i][0], j, 2 * i)
			grid.addWidget(buttons[ITEMS_PER_RIJ * j + i][1], j, 2 * i + 1)



###############################################################
#------------------------Single Button-------------------------
###############################################################


def makeButton(item):
	def getImageUrl(item):
		iurl = 'Images/' + str(item['id']) + '.jpeg'
		if os.path.isfile(iurl):
			return iurl
		else:
			return 'Resources/nopic.jpg'

	b1 = QtGui.QPushButton()
	b1.clicked.connect(lambda: itemClicked(item))
	b1.setFixedSize(100,100)
	b1.setAutoFillBackground(True)
	b1.setFocusPolicy(Qt.NoFocus)

	foto = getImageUrl(item)
	b1.setIcon(QtGui.QIcon(foto))
	b1.setStyleSheet("border: none;")
	b1.setIconSize(QSize(100,100))
	return b1

def makeLabel(item):
	l1 = QtGui.QLabel(utils.clean(item['name']))
	l1.setFixedSize(100,100)
	l1.setWordWrap(True)
	return l1

################################################################
#-------------------------ORDERLIJST----------------------------
################################################################

def itemClicked(item):
	if item not in list(map(lambda x: x['item'],data['order'])):
		data['order'].append({'Aantal':1,'item':item})
	else:
		for o in data['order']:
			if o['item'] is item:
				o['Aantal'] = o['Aantal']+1
				break

	rebuildOrderLijst()

def removeItem(item):
	item['Aantal']-=1
	if item['Aantal']==0:
		data['order'].remove(item)
	rebuildOrderLijst()

def addItem(item):
	item['Aantal']+=1
	rebuildOrderLijst()

def emptyOrder():
	del data['order'][:]
	rebuildOrderLijst()

def rebuildOrderLijst():
	for i in reversed(range(orderlijst.count())):
		notNeeded = orderlijst.takeAt(i).widget().setParent(None)
	rij=0
	for o in data['order']:
		removebutton = QtGui.QPushButton("-")
		removebutton.setFixedSize(40,40)
		removebutton.clicked.connect(lambda s, orde=o: removeItem(orde))

		countlabel = QtGui.QLabel(str(o["Aantal"]))
		countlabel.setFixedSize(25,40)

		addbutton = QtGui.QPushButton("+")
		addbutton.setFixedSize(40,40)
		addbutton.clicked.connect(lambda s, orde=o: addItem(orde))

		itemlabel = QtGui.QLabel(utils.clean(o['item']['name']))
		itemlabel.setWordWrap(True)

		orderlijst.addWidget(removebutton,rij,0)
		orderlijst.addWidget(countlabel,rij,1)
		orderlijst.addWidget(addbutton,rij,2)
		orderlijst.addWidget(itemlabel,rij,3)

		rij+=1

main()
