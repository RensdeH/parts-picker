#debugging tool
#print(len(app.allWidgets()))
#library imports
import datetime as dt
n1 = dt.datetime.now()
import sys
import os.path
from PyQt4 import QtGui
from PyQt4.QtCore import *

#custom imports
import latexfact
import api
import utils
import dialogs
import windowClass

tablist = []
webshopLijst = []
customLijst = []
data = {}
Cids = {} # key: catId, value: [articles]
catNames = {} #key: catId, value:catName
data['Artikelen'] = []
data['Custom'] = []
data['Werk'] = []

app = QtGui.QApplication(sys.argv)
tabs = QtGui.QTabWidget()
productWindow = windowClass.Window("Producten kiezen")
customerWindow = windowClass.Window("Klant kiezen")
vrijveldWindow = windowClass.Window("Custom producten")
urenWindow = windowClass.Window("Uren & Auto")
werkLayout = windowClass.werkLijst(data['Werk'])
orderlijst = windowClass.productLijst(data['Artikelen'])
vrijVeldLayout = windowClass.vrijVeldLijst(data['Custom'])

def main():
	windowClass.data = data
	def loadArtikels(silent=True):
		webshopProducts = utils.readJson('Resources/Artikelen.json')
		customProducts = utils.readJson('Resources/Custom/custom.json')
		if webshopProducts == {}:
			webshopProducts = api.getArtikels(silent=silent)
			utils.writeJson('Resources/Artikelen.json',webshopProducts)
		for d in webshopProducts:
			item = utils.makeWebshopItem(1,d)
			if item is not None:
				webshopLijst.append(item)
		for d in customProducts:
			item = utils.makePreCustomItem(1,d)
			if item is not None:
				customLijst.append(item)

	app.setWindowIcon(QtGui.QIcon('Resources/icon.png'))
	n2 = dt.datetime.now()
	print("Declaring:"+str((n2-n1).total_seconds()))
	loadArtikels()
	n3 = dt.datetime.now()
	print("Get artikelen:"+str((n3-n2).total_seconds()))
	Cids.update(defineTabs(webshopLijst))
	n4 = dt.datetime.now()
	print("Define Tabs:"+str((n4-n3).total_seconds()))
	fillTabs(Cids)
	n5 = dt.datetime.now()
	print("Fill Tabs:"+str((n5-n4).total_seconds()))
	productWindowSetup()
	customerWindowSetup()
	vrijveldWindowSetup()
	urenWindowSetup()
	setVolgorde([customerWindow,productWindow,vrijveldWindow,urenWindow])
	n6 = dt.datetime.now()
	print("Windows Setup:"+str((n6-n5).total_seconds()))
	customerWindow.show()
	n7 = dt.datetime.now()
	print("Show Window:"+str((n7-n6).total_seconds()))
	print("Total Time:"+str((n7-n1).total_seconds()))
	sys.exit(app.exec_())

######################################################
#-----------------------Setup-------------------------
######################################################

def addCustomProduct():
	product = dialogs.vrijVeldDialog()
	if product is None:
		return
	data['Custom'].append(product)
	vrijVeldLayout.rebuild()

def addUren():
	werk = dialogs.urenDialog()
	if werk == None:
		return
	data['Werk'].append(werk)
	werkLayout.rebuild()

def emptyOrder():
	del data['Artikelen'][:]
	orderlijst.rebuild()

#--------------------------Setup----------------------

def urenWindowSetup():
	def saveAuto(layout,typeFactuur):
		autoEdit = layout.itemAt(1)
		data['Auto'] = dialogs.getJsonLayout(autoEdit)
		latexfact.startFactuur(data,typeFactuur)

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

	urenButton = QtGui.QPushButton("Werk toevoegen")
	urenButton.setFixedHeight(100)
	urenButton.clicked.connect(addUren)

	scrollGroup = QtGui.QGroupBox()
	scrollGroup.setLayout(werkLayout)
	werkScroll = QtGui.QScrollArea()
	werkScroll.setWidget(scrollGroup)
	werkScroll.setWidgetResizable(True)

	voorbeeldButton = QtGui.QPushButton("Afdrukvoorbeeld Factuur")
	voorbeeldButton.setFixedHeight(100)
	voorbeeldButton.clicked.connect(lambda : saveAuto(rightLayout,utils.TypeFactuur.Afdrukvoorbeeld))

	prijsOpgaveButton = QtGui.QPushButton("Kostenraming")
	prijsOpgaveButton.setFixedHeight(100)
	prijsOpgaveButton.clicked.connect(lambda : saveAuto(rightLayout,utils.TypeFactuur.Kostenraming))

	urenWindow.setOpslaan(lambda : saveAuto(rightLayout,utils.TypeFactuur.Definitief))
	urenWindow.volgendeView.setText("Definitieve Factuur")

	leftLayout.addWidget(urenWindow.vorigeView,1)
	leftLayout.addWidget(werkScroll,4)
	leftLayout.addWidget(urenButton,1)

	rightLayout.addWidget(bestaandeAutoKiezen,1)
	rightLayout.addLayout(autoEdit,4)
	rightLayout.addWidget(voorbeeldButton,1)
	rightLayout.addWidget(prijsOpgaveButton,1)
	rightLayout.addWidget(urenWindow.volgendeView,1)

	urenWindow.totalLayout.insertLayout(1,leftLayout)
	urenWindow.totalLayout.insertLayout(2,rightLayout)

def productWindowSetup():
	leftLayout = QtGui.QVBoxLayout()
	rightlayout = QtGui.QVBoxLayout()

	tabs.setFocusPolicy(Qt.NoFocus)

	groupbox2 = QtGui.QGroupBox()
	scroll2 = QtGui.QScrollArea()
	scroll2.setWidget(groupbox2)
	scroll2.setWidgetResizable(True)
	groupbox2.setLayout(orderlijst)

	resetorder = QtGui.QPushButton("Leegmaken")
	resetorder.setFixedHeight(80)
	resetorder.clicked.connect(emptyOrder)

	actie = QtGui.QAction(productWindow)
	actie.setShortcut("Ctrl+F")
	productWindow.addAction(actie)
	actie.triggered.connect(lambda: searchTab())

	leftLayout.addWidget(productWindow.vorigeView)
	leftLayout.addWidget(tabs,4)
	rightlayout.addWidget(resetorder)
	rightlayout.addWidget(scroll2)
	rightlayout.addWidget(productWindow.volgendeView)

	productWindow.totalLayout.addLayout(leftLayout,3)
	productWindow.totalLayout.addLayout(rightlayout,1)

def vrijveldWindowSetup():
	leftLayout = QtGui.QVBoxLayout()
	rightLayout = QtGui.QVBoxLayout()

	scroll = QtGui.QScrollArea()
	groupbox = QtGui.QGroupBox(scroll)
	grid = ProductGrid(customLijst,vrijVeldLayout,data['Custom'],3)
	groupbox.setLayout(grid)
	scroll.setWidget(groupbox)
	scroll.setWidgetResizable(True)

	scrollGroup = QtGui.QGroupBox()
	scrollGroup.setLayout(vrijVeldLayout)
	werkScroll = QtGui.QScrollArea()
	werkScroll.setWidget(scrollGroup)
	werkScroll.setWidgetResizable(True)

	addVrij = QtGui.QPushButton("Product toevoegen")
	addVrij.setFixedHeight(100)
	addVrij.clicked.connect(addCustomProduct)

	leftLayout.addWidget(vrijveldWindow.vorigeView,1)
	leftLayout.addWidget(scroll)
	rightLayout.addWidget(werkScroll,5)
	rightLayout.addWidget(addVrij,1)
	rightLayout.addWidget(vrijveldWindow.volgendeView,1)

	vrijveldWindow.totalLayout.addLayout(leftLayout,1)
	vrijveldWindow.totalLayout.addLayout(rightLayout,1)

def customerWindowSetup():
	def saveCustomer(rightLayout):
		customerEdit = rightLayout.itemAt(1)
		data['Klant'] = dialogs.getJsonLayout(customerEdit)

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
		b1.clicked.connect(lambda s, so = en : data.update({'soortFactuur': so}))
		buttonLayout.addWidget(b1)
		buttons.append(b1)
	buttons[0].click()

	rightLayout.addWidget(bestaandeKlantKiezen)
	rightLayout.addLayout(customerEdit)
	rightLayout.addStretch()
	rightLayout.addLayout(buttonLayout)
	rightLayout.addWidget(customerWindow.volgendeView)

	customerWindow.setOpslaan(lambda : saveCustomer(rightLayout))
	customerWindow.totalLayout.addStretch()
	customerWindow.totalLayout.addLayout(rightLayout)
	customerWindow.totalLayout.addStretch()

def setVolgorde(volgorde):
	volgorde[0].setNextView(volgorde[1])
	for x in range(1,len(volgorde)-1):
		volgorde[x].setPreviousView(volgorde[x-1])
		volgorde[x].setNextView(volgorde[x+1])
	volgorde[-1].setPreviousView(volgorde[-2])

#############################################################
#-------------------------Zoeken-----------------------------
#############################################################

def searchTab():
	activeTab = tabs
	while type(activeTab.currentWidget()) is QtGui.QTabWidget:
		activeTab = activeTab.currentWidget()

	activeData = {}
	activeData['Position'] = activeTab.currentIndex()
	activeData['CatName'] = activeTab.tabText(activeData['Position'])
	activeData['Scroll'] = activeTab.currentWidget()
	activeData['CatId'] = activeData['Scroll'].whatsThis()
	activeData['Tab'] = activeTab
	activeData['Color'] = activeTab.tabBar().tabTextColor(activeData['Position'])

	zoekJob = dialogs.zoekDialog()
	if zoekJob is None:
		return
	text = str(zoekJob[0]).lower()
	zoekAlles = zoekJob[1]

	if zoekJob[1]:
		zoekLijst = webshopLijst
	else:
		zoekLijst = Cids[str(activeData['CatId'])]

	results = []

	def inItemDescription(product, text):
		descr = product.Item.get('description')
		if descr == None:
			return False
		else:
			return text in descr.lower()

	for product in zoekLijst:
		if text in product.Item['name'].lower() or inItemDescription(product, text):
			results.append(product)

	newScroll = makeTab(activeData['CatId'])

	b1 = QtGui.QPushButton(newScroll)
	b1.clicked.connect(lambda state, tabData = activeData: previousTab(tabData))
	b1.setFixedSize(100,100)
	b1.setFocusPolicy(Qt.NoFocus)
	b1.setStyleSheet("border: none;")
	b1.setIcon(QtGui.QIcon('Resources/searchback.png'))
	b1.setIconSize(QSize(100,100))

	l1 = QtGui.QLabel('',parent = newScroll)
	l1.setFixedSize(100,100)
	l1.setWordWrap(True)

	grid = ProductGrid(results,orderlijst,data['Artikelen'],5,searchButton = (b1,l1))
	newScroll.widget().setLayout(grid)

	index = activeTab.insertTab(activeData['Position'],newScroll,'Zoek:'+str(text))
	if not zoekJob[1]:
		activeTab.tabBar().setTabTextColor(index,activeData['Color'])
	baseWidget = activeTab.widget(activeData['Position']+1)
	activeTab.removeTab(activeData['Position']+1)
	baseWidget.deleteLater()
	activeTab.setCurrentIndex(activeData['Position'])

def previousTab(tabData):
	scroll = makeTab(tabData['CatId'])
	grid = ProductGrid(Cids[str(tabData['CatId'])],orderlijst,data['Artikelen'],5)
	scroll.widget().setLayout(grid)

	sluitZoeken(scroll,tabData['Tab'],tabData['Position'],catNames[str(tabData['CatId'])],tabData['Color'])

def sluitZoeken(scrollArea,tab,pos,name,color):
	zoek = tab.widget(pos)
	tab.removeTab(pos)
	zoek.deleteLater()
	tab.insertTab(pos,scrollArea,name)
	tab.tabBar().setTabTextColor(pos,color)
	tab.setCurrentIndex(pos)

############################################################
#------------------------Categories/Tabs--------------------
############################################################

def defineTabs(lijst):
	def listCatIds(lijst):
		cids = {}
		for a in lijst:
			for c in a.Item['categories']:
				if str(c['category_id']) == '5118110':
					continue
				if str(c['category_id']) == '5118120':
					continue

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
		grid = ProductGrid(cids[str(t[0])],orderlijst,data['Artikelen'],5)
		t[1].widget().setLayout(grid)
	colorTabs(tabs,QtGui.QColor(0,0,0),0)

def colorTabs(tabWid,color,depth):
	for x in range(tabWid.count()):
		binaryTab = "00000"+"{0:b}".format(x+1)
		newRed = int(binaryTab[-1])*128
		newGreen = int(binaryTab[-2])*128
		newBlue = int(binaryTab[-3])*128
		newColor = QtGui.QColor(newRed,newGreen,newBlue)
		if depth == 2:
			tabWid.tabBar().setTabTextColor(x,color)
		else:
			tabWid.tabBar().setTabTextColor(x,newColor)
		if type(tabWid.widget(x)) is QtGui.QTabWidget:
			colorTabs(tabWid.widget(x),newColor,depth+1)

###############################################################
#----------------------------Single Tab------------------------
###############################################################

def makeTab(cid):
	scroll = QtGui.QScrollArea()
	groupbox = QtGui.QGroupBox(scroll)

	scroll.setWidget(groupbox)
	scroll.setWidgetResizable(True)
	scroll.setWhatsThis(str(cid))
	return scroll

class ProductGrid(QtGui.QGridLayout):
	def __init__(self,products,display,orderLijst,itemsPerRij,searchButton=None,parent=None):
		super(ProductGrid,self).__init__(parent)
		self.products = products
		self.display = display
		self.orderLijst = orderLijst

		self.buttons = []
		if searchButton is not None:
			self.buttons.append(searchButton)
		for product in products:
			b = self.makeButton(product)
			l = self.makeLabel(product)
			self.buttons.append((b,l))

		length = len(self.buttons)
		itemsPerKolom = int(length / itemsPerRij) + 1
		for j in range(itemsPerKolom):
			for i in range(itemsPerRij):
				if itemsPerRij * j + i > length - 1:
					return
				self.addWidget(self.buttons[itemsPerRij * j + i][0], j, 2 * i)
				self.addWidget(self.buttons[itemsPerRij * j + i][1], j, 2 * i + 1)

	def makeLabel(self,product):
		l1 = QtGui.QLabel(utils.clean(product.Name))
		l1.setFixedSize(100,100)
		l1.setWordWrap(True)
		return l1

	def makeButton(self,product):
		b1 = QtGui.QPushButton()
		b1.clicked.connect(lambda: self.addOrderProduct(product))
		b1.setFixedSize(100,100)
		b1.setAutoFillBackground(True)
		b1.setFocusPolicy(Qt.NoFocus)

		foto = 'Images/' + str(product.Item['id']) + '.jpeg'
		if not os.path.isfile(foto):
			foto = 'Resources/nopic.jpg'
		b1.setIcon(QtGui.QIcon(foto))
		b1.setStyleSheet("border: none;")
		b1.setIconSize(QSize(100,100))
		return b1

	def addOrderProduct(self,product):
		if product.Item is None:
			self.orderLijst.append(product)
		else:
			if product.Item not in list(map(lambda x: x.Item,self.orderLijst)):
				self.orderLijst.append(product)
			else:
				for o in self.orderLijst:
					if o.Item is product.Item:
						o.Aantal = o.Aantal + 1
						break
		self.display.rebuild()

main()
