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
import windowClass
#constants
ITEMS_PER_RIJ = 5

#global QtGui Widgets
app = QtGui.QApplication(sys.argv)
productWindow = windowClass.Window("Producten kiezen")
customerWindow = windowClass.Window("Klant kiezen")
vrijveldWindow = windowClass.Window("Custom producten")
urenWindow = windowClass.Window("Uren & Auto")

orderlijst = QtGui.QGridLayout()
werkLayout = QtGui.QGridLayout()
vrijVeldLayout = QtGui.QGridLayout()
orderDisplay = QtGui.QLabel()
tabs = QtGui.QTabWidget()
tablist = []

# global data -Minimize this!
data = {} #factuur data (order, auto, Uren(aantal,omschrijving),klant,soort)
#data['Artikelen']
#data['Werk']
#data['Klant']
#data['Auto']
#data['Custom']
#data['preCustom']
#data['omschrijving']
#data['SoortFactuur']

Cids = {} # key: catId, value: [articles]
catNames = {} #key: catId, value:catName

def main():
	windowClass.data = data
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
	data['Artikelen'] = []
	data['Werk'] = []
	data['Custom'] = []
	data['preCustom'] = []
	n3 = dt.datetime.now()
	print("Get artikelen:"+str((n3-n2).total_seconds()))
	Cids.update(defineTabs(lijst))
	n4 = dt.datetime.now()
	print("Define Tabs:"+str((n4-n3).total_seconds()))
	fillTabs(Cids)
	n5 = dt.datetime.now()
	print("Fill Tabs:"+str((n5-n4).total_seconds()))
	productWindowSetup()
	customerWindowSetup()
	vrijveldWindowSetup()
	urenWindowSetup()
	n6 = dt.datetime.now()
	print("Windows Setup:"+str((n6-n5).total_seconds()))
	customerWindow.show()
	n7 = dt.datetime.now()
	print("Show Window:"+str((n7-n6).total_seconds()))
	print("Total Time:"+str((n7-n1).total_seconds()))
	sys.exit(app.exec_())
	#debugging tool
	#print(len(app.allWidgets()))

######################################################
#-----------------------Setup-------------------------
######################################################

#-------------------Werklijst Display-----------------

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
	if data['Werk'] == []:
		geenWerk = QtGui.QLabel('Geen werkuren toegevoegd')
		werkLayout.addWidget(geenWerk)

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

#--------------------------Setup----------------------

def urenWindowSetup():
	def saveAuto(layout,voorbeeld):
		autoEdit = layout.itemAt(1)
		data['Auto'] = dialogs.getJsonLayout(autoEdit)
		latexfact.startFactuur(data,voorbeeld)

	def kiesAuto(layout):
		fileName = QtGui.QFileDialog.getOpenFileName(customerWindow, 'Open File', 'Resources/Autos')
		if fileName == '':
			return
		autoData = utils.readJson(fileName)
		carEdit = dialogs.controleerJsonLayout(autoData)
		l = layout.takeAt(1)
		for i in reversed(range(l.count())):
			notNeeded = l.takeAt(i).widget().setParent(None)
		layout.insertLayout(1,carEdit)

	leftLayout = QtGui.QVBoxLayout()
	rightLayout = QtGui.QVBoxLayout()

	emptyAuto = utils.readJson('Resources/emptyAuto.json')
	autoEdit = dialogs.controleerJsonLayout(emptyAuto)

	bestaandeAutoKiezen = QtGui.QPushButton("Bestaande Auto Kiezen")
	bestaandeAutoKiezen.clicked.connect(lambda s, edit = rightLayout: kiesAuto(edit))
	bestaandeAutoKiezen.setFixedHeight(100)

	addUrenb = QtGui.QPushButton("Werk toevoegen")
	addUrenb.setFixedHeight(100)
	addUrenb.clicked.connect(addUren)

	rebuildWerkUrenWindow()

	scrollGroup = QtGui.QGroupBox()
	scrollGroup.setLayout(werkLayout)
	werkScroll = QtGui.QScrollArea()
	werkScroll.setWidget(scrollGroup)
	werkScroll.setWidgetResizable(True)

	leftLayout.addWidget(urenWindow.vorigeView,1)
	leftLayout.addWidget(werkScroll,4)
	leftLayout.addWidget(addUrenb,1)

	voorbeeldButton = QtGui.QPushButton("Afdrukvoorbeeld")
	voorbeeldButton.setFixedHeight(100)
	voorbeeldButton.setText("Afdrukvoorbeeld")
	voorbeeldButton.clicked.connect(lambda : saveAuto(rightLayout,True))

	rightLayout.addWidget(bestaandeAutoKiezen,1)
	rightLayout.addLayout(autoEdit,4)
	rightLayout.addWidget(voorbeeldButton,1)
	rightLayout.addWidget(urenWindow.volgendeView,1)

	urenWindow.totalLayout.insertLayout(1,leftLayout)
	urenWindow.totalLayout.insertLayout(2,rightLayout)

	urenWindow.setNextView(None,opslaan = lambda : saveAuto(rightLayout,False))
	urenWindow.volgendeView.setText("Definitieve Factuur")
	urenWindow.setPreviousView(vrijveldWindow)

	werkLayout.setAlignment(Qt.AlignTop)

def productWindowSetup():
	leftLayout = QtGui.QVBoxLayout()
	rightlayout = QtGui.QVBoxLayout()

	leftLayout.addWidget(productWindow.vorigeView)
	leftLayout.addWidget(tabs,4)

	groupbox2 = QtGui.QGroupBox()
	scroll2 = QtGui.QScrollArea()
	scroll2.setWidget(groupbox2)
	scroll2.setWidgetResizable(True)

	orderlijst.setAlignment(Qt.AlignTop)
	groupbox2.setLayout(orderlijst)

	resetorder = QtGui.QPushButton("Leegmaken")
	resetorder.setFixedHeight(80)
	resetorder.clicked.connect(emptyOrder)

	actie = QtGui.QAction(productWindow)
	actie.setShortcut("Ctrl+F")
	productWindow.addAction(actie)
	actie.triggered.connect(lambda: searchTab())

	rightlayout.addWidget(resetorder)
	rightlayout.addWidget(scroll2)
	rightlayout.addWidget(productWindow.volgendeView)

	tabs.setFocusPolicy(Qt.NoFocus)

	productWindow.setNextView(vrijveldWindow)
	productWindow.setPreviousView(customerWindow)
	productWindow.totalLayout.addLayout(leftLayout,3)
	productWindow.totalLayout.addLayout(rightlayout,1)

def addVrijVeld():
	product = dialogs.vrijVeldDialog()
	if product == None:
		return
	data['Custom'].append(product)
	rebuildVrijVeldWindow()

def addCustomProduct(product):
	if product not in list(map(lambda x: x['item'],data['preCustom'])):
		data['preCustom'].append({'Aantal':1,'item':product})
	else:
		for o in data['preCustom']:
			if o['item'] is product:
				o['Aantal'] = o['Aantal']+1
				break
	rebuildVrijVeldWindow()

def removePreCustom(product):
	data['preCustom'].remove(product)
	rebuildVrijVeldWindow()


def removeVrijVeld(product):
	data['Custom'].remove(product)
	rebuildVrijVeldWindow()

def rebuildVrijVeldWindow():
	for i in reversed(range(vrijVeldLayout.count())):
		notNeeded = vrijVeldLayout.takeAt(i).widget().setParent(None)
	rij = 0
	#werk = (floatUren,stringOmschrijving)
	if data['Custom'] == [] and data['preCustom'] == []:
		geenCustom = QtGui.QLabel('Geen Extra Producten toegevoegd')
		vrijVeldLayout.addWidget(geenCustom)

	for product in data['Custom']:
		countlabel = QtGui.QLabel(str(product[0]))
		countlabel.setFixedSize(25,40)

		omschrijvingLabel = QtGui.QLabel(utils.clean(product[1]))
		omschrijvingLabel.setWordWrap(True)

		prijsLabel = QtGui.QLabel('\xe2\x82\xac'.decode('utf8')+str(product[2]))
		prijsLabel.setAlignment(Qt.AlignRight)
		removebutton = QtGui.QPushButton("X")
		removebutton.setFixedSize(40,40)
		removebutton.clicked.connect(lambda s, w=product: removeVrijVeld(w))

		vrijVeldLayout.addWidget(countlabel,rij,0)
		vrijVeldLayout.addWidget(omschrijvingLabel,rij,1)
		vrijVeldLayout.addWidget(prijsLabel,rij,2)
		vrijVeldLayout.addWidget(removebutton,rij,3)
		rij+=1
	for product in data['preCustom']:
		countlabel = QtGui.QLabel(str(product['Aantal']))
		countlabel.setFixedSize(25,40)

		omschrijvingLabel = QtGui.QLabel(utils.clean(product['item']['name']))
		omschrijvingLabel.setWordWrap(True)

		prijsLabel = QtGui.QLabel('\xe2\x82\xac'.decode('utf8')+str(product['item']['Prijs']))
		prijsLabel.setAlignment(Qt.AlignRight)
		removebutton = QtGui.QPushButton("X")
		removebutton.setFixedSize(40,40)
		removebutton.clicked.connect(lambda s, w=product: removePreCustom(w))

		vrijVeldLayout.addWidget(countlabel,rij,0)
		vrijVeldLayout.addWidget(omschrijvingLabel,rij,1)
		vrijVeldLayout.addWidget(prijsLabel,rij,2)
		vrijVeldLayout.addWidget(removebutton,rij,3)
		rij+=1

def vrijveldWindowSetup():
	leftLayout = QtGui.QVBoxLayout()
	rightLayout = QtGui.QVBoxLayout()

	leftLayout.addWidget(vrijveldWindow.vorigeView,1)

	customProducts = utils.readJson('Resources/Custom/custom.json')

	scroll = QtGui.QScrollArea()
	groupbox = QtGui.QGroupBox(scroll)
	grid = QtGui.QGridLayout(groupbox)

	scroll.setWidget(groupbox)
	scroll.setWidgetResizable(True)

	makeGrid2(customProducts,scroll,None)
	leftLayout.addWidget(scroll)

	addVrij = QtGui.QPushButton("Product toevoegen")
	addVrij.setFixedHeight(100)
	addVrij.clicked.connect(addVrijVeld)

	scrollGroup = QtGui.QGroupBox()
	scrollGroup.setLayout(vrijVeldLayout)
	werkScroll = QtGui.QScrollArea()
	werkScroll.setWidget(scrollGroup)
	werkScroll.setWidgetResizable(True)

	rebuildVrijVeldWindow()

	rightLayout.addWidget(werkScroll,5)
	rightLayout.addWidget(addVrij,1)
	rightLayout.addWidget(vrijveldWindow.volgendeView,1)

	vrijVeldLayout.setAlignment(Qt.AlignTop)
	vrijveldWindow.setNextView(urenWindow)
	vrijveldWindow.setPreviousView(productWindow)

	vrijveldWindow.totalLayout.addLayout(leftLayout,1)
	vrijveldWindow.totalLayout.addLayout(rightLayout,1)

def customerWindowSetup():
	def setSoort(s):
		data['soortFactuur'] = s

	def makeFactuur(rightLayout,omsLine):
		customerEdit = rightLayout.itemAt(1)
		data['Klant'] = dialogs.getJsonLayout(customerEdit)
		data['Omschrijving'] = str(omsLine.text())
		#latexfact.startFactuur(data)

	def kiesKlant(layout):
		fileName = QtGui.QFileDialog.getOpenFileName(customerWindow, 'Open File', 'Resources/Klanten')
		if fileName == '':
			return
		klantData = utils.readJson(fileName)
		custEdit = dialogs.controleerJsonLayout(klantData)
		l = layout.takeAt(1)
		for i in reversed(range(l.count())):
			notNeeded = l.takeAt(i).widget().setParent(None)
		layout.insertLayout(1,custEdit)

	def rebuildOrderDisplay():
		s = ''
		for o in data['Artikelen']:
			try:
				s += str(o['Aantal']) + ' x ' + utils.clean(o['item']['name']) + '\n'
			except:
				s += "\n"
		if data['Artikelen'] == []:
			s = 'Geen producten gekozen'
		orderDisplay.setText(s)

	def predictSoort(buttons):
		buttons[1].toggle()
		if data['Auto']['Prijs']<0:
			buttons[0].toggle()
			return
		if data['Auto']['Model'] is not '':
			buttons[1].toggle()
			return
		if data['Werk'] is not []:
			buttons[2].toggle()
			return
		buttons[3].toggle()

	leftLayout = QtGui.QVBoxLayout()
	rightLayout = QtGui.QVBoxLayout()

	emptyKlant = utils.readJson('Resources/emptyCustomer.json')
	customerEdit = dialogs.controleerJsonLayout(emptyKlant)

	bestaandeKlantKiezen = QtGui.QPushButton("Bestaande Klant Kiezen")
	bestaandeKlantKiezen.clicked.connect(lambda s, edit = rightLayout: kiesKlant(edit))
	bestaandeKlantKiezen.setFixedHeight(100)

	buttonLayout = QtGui.QHBoxLayout()
	soortLabel = QtGui.QLabel("Soort Factuur:")
	buttonLayout.addWidget(soortLabel)
	buttonLayout.setAlignment(Qt.AlignLeft)

	buttons = []
	for en in utils.SoortFactuur:
		b1 = QtGui.QRadioButton(en.name)
		b1.clicked.connect(lambda s, so = en : setSoort(so))
		buttonLayout.addWidget(b1)
		buttons.append(b1)
	#predictSoort(buttons)

	omsLayout = QtGui.QHBoxLayout()
	omsLabel = QtGui.QLabel("Omschrijving")
	omsLine = QtGui.QLineEdit()
	omsLayout.addWidget(omsLabel)
	omsLayout.addWidget(omsLine)

	orderDisplay.setAlignment(Qt.AlignTop)
	orderDisplay.setWordWrap(True)

	#leftLayout.addWidget(customerWindow.vorigeView,1)
	leftLayout.addWidget(orderDisplay,5)

	rightLayout.addWidget(bestaandeKlantKiezen)
	rightLayout.addLayout(customerEdit)
	rightLayout.addLayout(buttonLayout)
	rightLayout.addLayout(omsLayout)
	rightLayout.addWidget(customerWindow.volgendeView)

	customerWindow.setNextView(productWindow,opslaan = lambda : makeFactuur(rightLayout,omsLine))
	customerWindow.setPreviousView(customerWindow)

	customerWindow.setRebuild(rebuildOrderDisplay)

	customerWindow.totalLayout.addLayout(leftLayout,1)
	customerWindow.totalLayout.addLayout(rightLayout,5)

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

def makeGrid2(lijst,scroll,button):
	grid = scroll.widget().layout()

	buttons = []
	if button is not None:
		buttons.append(button)

	for item in lijst:
		b = makeButton2(item)
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

def makeButton2(item):
	def getImageUrl(item):
		iurl = 'Images/' + str(item['id']) + '.jpeg'
		if os.path.isfile(iurl):
			return iurl
		else:
			return 'Resources/nopic.jpg'

	b1 = QtGui.QPushButton()
	b1.clicked.connect(lambda: addCustomProduct(item))
	b1.setFixedSize(100,100)
	b1.setAutoFillBackground(True)
	b1.setFocusPolicy(Qt.NoFocus)

	foto = getImageUrl(item)
	b1.setIcon(QtGui.QIcon(foto))
	b1.setStyleSheet("border: none;")
	b1.setIconSize(QSize(100,100))
	return b1


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
	if item not in list(map(lambda x: x['item'],data['Artikelen'])):
		data['Artikelen'].append({'Aantal':1,'item':item})
	else:
		for o in data['Artikelen']:
			if o['item'] is item:
				o['Aantal'] = o['Aantal']+1
				break

	rebuildOrderLijst()

def removeItem(item):
	item['Aantal']-=1
	if item['Aantal']==0:
		data['Artikelen'].remove(item)
	rebuildOrderLijst()

def addItem(item):
	item['Aantal']+=1
	rebuildOrderLijst()

def emptyOrder():
	del data['Artikelen'][:]
	rebuildOrderLijst()

def rebuildOrderLijst():
	for i in reversed(range(orderlijst.count())):
		notNeeded = orderlijst.takeAt(i).widget().setParent(None)
	rij=0
	for o in data['Artikelen']:
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
