import subprocess
import utils
import datetime as dt
import api
import os
import shutil
import dialogs

#deprecated
def mockfact():
	order = utils.readJson('Resources/mockOrder.json')[0:9]
	comp = []
	for item in order:
		comp.append({'Aantal':2,'item':item})
	klant = utils.readJson('Resources/Klanten/mockCustomer.json')
	soort = utils.SoortFactuur.Reparatie
	omschrijving = 'Mock Factuur'

def startFactuur(data,voorbeeld,raming = False):
	if 'soortFactuur' not in data:
		dialogs.errorDialog()
		return
	if not voorbeeld:
		utils.writeJson('Resources/Klanten/'+data['Klant']['Naam']+'.json',data['Klant'])
	makeFactuur(data,voorbeeld,raming)

def makeFactuur(data,voorbeeld,raming=False):
	factuurNummer = getFactuurNummer(data['soortFactuur'],voorbeeld,raming)
	data['FactuurNummer'] = factuurNummer
	pdfNaam = data['Klant']['Naam'] +' '+ factuurNummer
	data['bedrijf'] = standardBedrijfInfo()
	if raming:
		data['Omschrijving'] = 'Kostenraming'
	else:
		data['Omschrijving'] = 'Factuur'
	workingDir = 'Invoice/'
	filename = pdfNaam + '.tex'
	pdffilename = pdfNaam + '.pdf'

	file = open(workingDir + filename,'w')
	latexCode = makeTex(data,raming)
	file.write(latexCode)
	file.close()
	proc = runpdflatex(filename,True,workingDir)
	proc.wait()
	shutil.move(workingDir + filename,'Facturen/' + filename)
	if voorbeeld:
		shutil.move(workingDir + pdffilename,'Temp/' + pdffilename)
	else:
		shutil.move(workingDir + pdffilename,'Facturen/' + pdffilename)
		shutil.copy('Facturen/' + pdffilename,'/home/chris/Dropbox/B. MX5-Winkel administratie/MX5Winkel' + pdffilename)

	if voorbeeld:
		openfile(pdffilename,'Temp/')
	else:
		openfile(pdffilename,'Facturen/')

def makeTex(data,raming):
	order = data['Artikelen']
	preCustom = data['preCustom']
	custom = data['Custom']
	werk = data['Werk']
	klant = data['Klant']
	bedrijfsinfo = data['bedrijf']
	factuurNummer = data['FactuurNummer']
	omschrijving = data['Omschrijving']
	betaalwijze = "contant of per pin"
	if data['soortFactuur'] == utils.SoortFactuur.Reparatie:
		betaalwijze += " bij afhalen auto"
	if data['soortFactuur'] == utils.SoortFactuur.Verkoop:
		betaalwijze = "via bankoverschrijving voor afhalen auto"
	if data['soortFactuur'] == utils.SoortFactuur.Inkoop:
		betaalwijze = "via bankoverschrijving"
	auto = None
	if 'Auto' in data:
		auto = data['Auto']

	latexCode = ""
	latexCode += makeStartText()
	latexCode += makeTopText(klant,factuurNummer,omschrijving,raming)
	latexCode += makeOrderText(order,werk,auto,preCustom,custom)
	latexCode += makeBottomText(bedrijfsinfo,betaalwijze)
	return latexCode

def getFactuurNummer(soort,voorbeeld,raming):
	S = soort.name[0:1]
	jaar = dt.datetime.now().year
	counter = getCounter('C',voorbeeld)
	if raming:
		return 'Raming-'+str(jaar) +'-'+ S + str(counter)
	else:
		return str(jaar) +'-'+ S + str(counter)

def getCounter(S,voorbeeld):
	counters = utils.readJson('Resources/counters.json')
	c = counters[S] + 1
	if not voorbeeld:
		counters[S] = c
		utils.writeJson('Resources/counters.json',counters)
	return c

def makeStartText():
	return utils.readfile('Invoice/top.txt')

def makeTopText(klant,factuurnummer, omschrijving,raming):
	datumData = dt.date.today()
	datum = datumData.strftime("%d-%m-%Y")
	topText = r"""\begin{tabular}[t]{l@{}}
    	\tab """+klant['Naam']+r""" \\
    	\tab """+klant['Straat']+r"""\\
    	\tab """+klant['Postcode']+r""" """+klant['Plaats']+r"""\\
    	[0.5cm]
    	\tab Telefoon: """+klant['Telefoon']+r"""\\
    	\tab Email: """+klant['email']+r"""\\
		\end{tabular}

	\hfill

	\begin{tabular}[t]{l@{}}
     	"""+omschrijving

	if not raming:
		topText += r"""\\
     	Factuurdatum:\hspace{0.3cm} """+datum+r""" \\
     	Factuurnummer: """+factuurnummer
	else:
		topText += r"""\\
		Datum:\hspace{1.5cm} """+datum

	if klant['Kenteken'] != '':
		topText += r"""\\
		\\
		Kenteken: \hspace{1.1cm} """+klant['Kenteken']
	topText += r"""\\
	 \end{tabular}
	}

	\renewcommand{\arraystretch}{0.9}"""
	return topText

def makeOrderText(order,werk,auto,preCustom,custom):
	btwhoog = 0
	uitbtwhoog = 0
	uitbtwgeen = 0

	orderText = ''
	orderText += r"""

	\begin{invoiceTable}"""

	if order != [] or preCustom != [] or custom != []:
		orderText += r"""\feetype{Producten}"""
	for o in order:
		orderText += '\unitrow{'+o['item']['name']+'}{'+str(o['Aantal'])+'}{'+o['item']['price']['default']+'}{}'
		if float(o['item']['tax']) == 21:
			uitbtwhoog += float(o['item']['price']['default']) * o['Aantal']
		elif float(o['item']['tax']) == 0:
			uitbtwgeen += float(o['item']['price']['default']) * o['Aantal']

	for o in preCustom:
		orderText += '\unitrow{'+o['item']['name']+'}{'+str(o['Aantal'])+'}{'+o['item']['Prijs']+'}{}'
		if float(o['item']['tax']) == 21:
			uitbtwhoog += float(o['item']['Prijs']) * o['Aantal']
		elif float(o['item']['tax']) == 0:
			uitbtwgeen += float(o['item']['Prijs']) * o['Aantal']

	for o in custom:
		orderText += '\unitrow{'+o[1]+'}{'+str(o[0])+'}{'+str(o[2])+'}{}'
		if o[3] == 21:
			uitbtwhoog += float(o[2]) * o[0]
		elif o[3] == 0:
			uitbtwgeen += float(o[2]) * o[0]

	if werk != []:
		orderText += r"""
		\feetype{Gewerkte Uren}"""
		for w in werk:
			orderText += r"""\hourrow{Werkplaatstarief """+w[1]+r"""}{"""+str(w[0])+r"""}{62.5}"""
			uitbtwhoog += float(62.5) * w[0]

	if auto['Model'] != '':
		orderText += r"""
		\feetype{Auto}"""
		autoOmschrijving = getCarDes(auto)
		orderText += r"""\unitrow{"""+getCarDes(auto)+r"""}{"""+str(1)+r"""}{"""+auto['Prijs']+r"""}{}"""
		uitbtwgeen += float(auto['Prijs'])

	btwhoog = (uitbtwhoog/1.21)*0.21
	orderText+=r"""
	\setendtotal{"""+str(uitbtwhoog)+r"""}{"""+str(btwhoog)+r"""}{"""+str(uitbtwgeen)+r"""}{0}\\
	\end{invoiceTable}
	"""
	return orderText

def getCarDes(auto):
	s = ''
	s += str(auto['Model'])+' kenteken '+str(auto['Kenteken'])+r"""\\"""
	s += "Bouwjaar: " + str(auto['Bouwjaar']) +r"""\\"""
	s += "km-stand: " + str(auto['km-stand']) +r"""\\"""
	s += "Meldcode: " + str(auto['Meldcode']) +r"""\\"""
	s += "APK " + str(auto['APK']) +r"""\\"""
	s += auto['extra info']
	return s

def makeBottomText(bedrijf,betaalwijze):
	bottomText = r"""
	\tab \tab Betaalwijze: {\bf """ + betaalwijze + r"""}
	\vspace*{\fill}
	\begin{center}
		\begin{spacing}{1.0}
		"""+bedrijf['Website']+r""" / """+bedrijf['Straat']+r""" / """+bedrijf['Postcode']+r""" """+bedrijf['Plaats']+r""" """+bedrijf['Land']+r""" \\
		KvK """+bedrijf['KvK']+r""" / BTW nr. """+bedrijf['BTW-nr.']+r""" \\
		IBAN """+bedrijf['IBAN']+r""" / Bicnr. """+bedrijf['BIC']+r""" \\
		voor contact: """+bedrijf['Email']+r""" \\
		\end{spacing}
	\end{center}
	\end{document}"""
	return bottomText

def runpdflatex(fileName,debug,workingDir):
	print(fileName)
	if debug:
		proc =  subprocess.Popen(['pdflatex','-interaction','nonstopmode',fileName],cwd=workingDir)
		return proc
	else:
		proc = subprocess.Popen(['pdflatex','-interaction','batchmode',fileName],cwd=workingDir)
		return proc

def openfile(filename,workingDir):
	proc = subprocess.Popen(['xdg-open',filename],cwd=workingDir)
	return proc

#####################################################################3

def standardBedrijfInfo():
	company = utils.readJson('Resources/company.json')
	if company != {}:
		return company
	return utils.writeJson('Resources/company.json',utils.makeCompany())
