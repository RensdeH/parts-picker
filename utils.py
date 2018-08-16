############################################################
#-------------------------Utils-----------------------------
############################################################
import os.path
import json

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

#Templates voor soorten facturen
#emptyCustomer
#emptyAuto
#reparatieCustomer
#ArtikelenCustomer
#InkoopAuto
#VerkoopAuto


def makeCompany():
	data = {}
	data['Bedrijfsnaam'] = "MX5-Winkel"
	data['Straat'] = "Energieweg 9-11"
	data['Plaats'] = 'Meerkerk'
	data['Postcode'] = '4231DJ'
	data['Email'] = ''
	data['Rekeningnummer'] = "NLXXRABOXXXXXXXX"
	data['Telefoon'] = '0183-123456'
	return data

def makeEmptyCustomer():
	data = {}
	data['id'] = ''
	data['Naam'] = ''
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

#controlJsonApp('Resources/emptyCustomer.json')

#writeJson('Resources/company.json',makeCompany())
