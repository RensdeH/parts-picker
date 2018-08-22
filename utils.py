############################################################
#-------------------------Utils-----------------------------
############################################################
import os.path
import json
from enum import Enum
class SoortFactuur(Enum):
	Inkoop = 1
	Verkoop = 2
	Reparatie = 3
	Artikelen = 4

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
	data = json.load(read)
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

#Templates voor soorten facturen
#emptyCustomer
#emptyAuto
#reparatieCustomer
#ArtikelenCustomer
#InkoopAuto
#VerkoopAuto

def makeMockOrder(data):
	writeJson('Resources/mockOrder.json',data)

def makeMockCustomer():
	data = {}
	data['Naam'] = 'Vladimir Poetin'
	data['email'] = 'vlad@poetin.rus'
	data['Telefoon'] = '06-12345678'
	data['Straat'] = 'Sikkelstraat 5'
	data['Postcode'] = '1999AB'
	data['Plaats'] = 'Moskou'
	data['Kenteken'] = '12-RUS-9'
	data['km-stand'] = '45682'
	writeJson('Resources/Klanten/mockCustomer.json',data)

def makeCompany():
	data = {}
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
	return data

def makeEmptyCustomer():
	data = {}
	data['Naam'] = ''
	data['email'] = ''
	data['Telefoon'] = ''
	data['Straat'] = ''
	data['Postcode'] = ''
	data['Plaats'] = ''
	data['Kenteken'] = ''
	data['km-stand'] = ''
	writeJson('Resources/emptyCustomer.json',data)

def makeEmptyAuto():
	data = {}
	data['Kenteken'] = ''
	data['Model'] = ''
	data['Bouwjaar'] = ''
	data['km-stand'] = ''
	data['Meldcode'] = ''
	data['APK'] = ''
	data['extra info'] = ''
	writeJson('Resources/emptyAuto.json',data)

def makeCounters():
	data = {}
	data['R'] = 300
	data['V'] = 200
	data['I'] = 300
	data['A'] = 100
	data['year'] = 2018
	writeJson('Resources/counters.json',data)

#controlJsonApp('Resources/emptyCustomer.json')

#writeJson('Resources/company.json',makeCompany())
