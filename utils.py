############################################################
#-------------------------Utils-----------------------------
############################################################
import os.path
import json
from collections import OrderedDict
from enum import Enum
#custom imports not allowed

class SoortFactuur(Enum):
	Reparatie = 1
	Inkoop = 2
	Verkoop = 3
	Artikelen = 4

class TypeFactuur(Enum):
	Definitief = 1
	Afdrukvoorbeeld = 2
	Kostenraming = 3

class OrderItem(object):
	def __init__(self, aantal, name, prijs, tax):
		self.Aantal = aantal
		self.Name = name
		self.Prijs = prijs
		self.Tax = tax
		self.Item = None

	def strLatex(self):
		return '\unitrow{' + self.Name + '}{' + str(self.Aantal) + '}{' + str(self.Prijs) + '}{}'

	def totaalPrijs(self):
		return self.Aantal * self.Prijs

class PreCustomItem(OrderItem):
	def __init__(self,aantal,item):
		super(PreCustomItem,self).__init__(aantal,item['Naam'],item['Prijs'],item['tax'])
		self.Item = item

class WebshopItem(OrderItem):
	def __init__(self,aantal,item):
		super(WebshopItem,self).__init__(aantal,item['name'],float(item['price']['default']),float(item['tax']))
		self.Item = item

def clean(name):
	name = name.replace("Mazda","")
	name = name.replace("MX5","")
	name = name.replace("MX-5","")
	return name

def readJson(filename):
	if not os.path.isfile(filename):
		print("Not found:" + filename)
		return {}
	read = open(filename,'r')
	data = json.load(read, object_pairs_hook=OrderedDict)
	read.close()
	return data

def writeJson(filename,data):
	write = open(filename,'w')
	json.dump(data,write)
	write.close()

def readfile(filename):
	read = open(filename,'r')
	s = read.read()
	read.close()
	return s

def printData(data):
	for key in ['Custom','preCustom']:
		if key in data:
			print(data[key])
	print('---------')

#Templates voor soorten facturen
#emptyCustomer
#emptyAuto
#reparatieCustomer
#ArtikelenCustomer
#InkoopAuto
#VerkoopAuto

def makeMockOrder(data):
	writeJson('Resources/mockOrder.json',data)
	return data

def makeMockCustomer():
	data = OrderedDict()
	data['Naam'] = 'Vladimir Poetin'
	data['email'] = 'vlad@poetin.rus'
	data['Telefoon'] = '06-12345678'
	data['Straat'] = 'Sikkelstraat 5'
	data['Postcode'] = '1999AB'
	data['Plaats'] = 'Moskou'
	data['Kenteken'] = '12-RUS-9'
	data['km-stand'] = '45682'
	writeJson('Resources/Klanten/mockCustomer.json',data)
	return data

def makeMockAuto():
	data = OrderedDict()
	data['Kenteken'] = '12-ABS-09'
	data['Model'] = 'NC'
	data['Bouwjaar'] = '2010'
	data['km-stand'] = '123456'
	data['Meldcode'] = '59'
	data['APK'] = ''
	data['extra info'] = 'Roest onder de kap'
	data['Prijs'] = '2300'
	writeJson('Resources/Autos/mockAuto.json',data)
	return data

def makeCompany():
	data = OrderedDict()
	data['Straat'] = 'Energieweg 9-11'
	data['Plaats'] = 'Meerkerk'
	data['Land'] = 'Nederland'
	data['Postcode'] = '4231DJ'
	data['Email'] = 'info@mx5-winkel.nl'
	data['Website'] = 'MX5Winkel.nl'
	data['KvK'] = '66326141'
	data['BTW-nr.'] = 'NL856495621B01'
	data['IBAN'] = 'NL63RABO0108245489'
	data['BIC'] = 'RABONL2U'
	#Niet nodig voor bottom.txt
	data['Telefoon'] = ''
	data['Bedrijfsnaam'] = ""
	return data

def makeEmptyCompany():
	data = OrderedDict()
	data['Straat'] = ""
	data['Plaats'] = ''
	data['Land'] = ''
	data['Postcode'] = ''
	data['Email'] = ''
	data['Website'] = ''
	data['KvK'] = ''
	data['BTW-nr.'] = ''
	data['IBAN'] = ''
	data['BIC'] = ''
	#Niet nodig voor bottom.txt
	data['Telefoon'] = ''
	data['Bedrijfsnaam'] = ""
	writeJson('Resources/company.json',makeCompany())
	return data

def makeEmptyCustomer():
	data = OrderedDict()
	data['Naam'] = ''
	data['email'] = ''
	data['Telefoon'] = ''
	data['Straat'] = ''
	data['Postcode'] = ''
	data['Plaats'] = ''
	data['Kenteken'] = ''
	data['km-stand'] = ''
	writeJson('Resources/emptyCustomer.json',data)
	return data

def makeEmptyAuto():
	data = OrderedDict()
	data['Kenteken'] = ''
	data['Model'] = ''
	data['Bouwjaar'] = ''
	data['km-stand'] = ''
	data['Meldcode'] = ''
	data['APK'] = ''
	data['extra info'] = ''
	data['Prijs'] = ''
	writeJson('Resources/emptyAuto.json',data)
	return data

def makeCustomProducts():
	data = []
	olieNAB = {}
	olieNAB['Prijs'] = '17.35'
	olieNAB['Aantal'] = '3.8'
	olieNAB['Naam'] = '3.8L Motorolie 10W40'
	olieNAB['id'] = 'olienab'
	olieNAB['name'] = '3.8L Motorolie 10W40'
	olieNAB['tax'] = 21
	data.append(olieNAB)
	olieNC = {}
	olieNC['Prijs'] = '17.70'
	olieNC['Aantal'] = '4.45'
	olieNC['Naam'] = '4.45L Motorolie 15W30'
	olieNC['id'] = 'olienc'
	olieNC['name'] = '4.45L Motorolie 15W30'
	olieNC['tax'] = 21
	data.append(olieNC)
	APK = {}
	APK['Prijs'] = '75'
	APK['Aantal'] = '1'
	APK['Naam'] = 'APK'
	APK['id'] = 'apk'
	APK['name'] = 'APK'
	APK['tax'] = 21
	data.append(APK)
	leenAuto = {}
	leenAuto['Prijs'] = '12.50'
	leenAuto['Aantal'] = '1'
	leenAuto['Naam'] = 'Leenauto'
	leenAuto['id'] = 'leenauto'
	leenAuto['name'] = 'Leenauto'
	leenAuto['tax'] = 0
	data.append(leenAuto)
	writeJson('Resources/Custom/custom.json',data)

def makeCounters():
	#TODO check if file is correct
	#if not os.path.isfile('Resources/counters.json'):
	#	return
	data = {}
	data['C'] = 100
	data['R'] = 300
	data['V'] = 200
	data['I'] = 300
	data['A'] = 100
	data['year'] = 2018
	writeJson('Resources/counters.json',data)
	return data
