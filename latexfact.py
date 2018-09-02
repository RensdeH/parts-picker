import subprocess
import utils
import datetime as dt
import api
import os
import shutil

#deprecated
def mockfact():
	order = utils.readJson('Resources/mockOrder.json')[0:9]
	comp = []
	for item in order:
		comp.append({'Aantal':2,'item':item})
	klant = utils.readJson('Resources/Klanten/mockCustomer.json')
	soort = utils.SoortFactuur.Reparatie
	omschrijving = 'Mock Factuur'

def factuurFromData(data):
	startFactuur(data)

def startFactuur(data):
	data['bedrijf'] = standardBedrijfInfo()
	makeFactuur(data)

def makeFactuur(data):
	factuurNummer = getFactuurNummer(data['soortFactuur'])
	data['FactuurNummer'] = factuurNummer
	workingDir = 'Invoice/'
	filename = factuurNummer + '.tex'
	pdffilename = factuurNummer + '.pdf'

	file = open(workingDir + filename,'w')
	latexCode = makeTex(data)
	file.write(latexCode)
	file.close()
	proc = runpdflatex(filename,True,workingDir)
	proc.wait()
	shutil.move(workingDir + filename,'Facturen/' + filename)
	shutil.move(workingDir + pdffilename,'Facturen/' + pdffilename)

	openfile(pdffilename,'Facturen/')

def makeTex(data):
	order = data['order']
	werk = None
	if 'Werk' in data:
		werk = data['Werk']
	klant = data['klant']
	bedrijfsinfo = data['bedrijf']
	factuurNummer = data['FactuurNummer']
	omschrijving = data['Omschrijving']
	auto = None
	if 'Auto' in data:
		auto = data['Auto']

	latexCode = ""
	latexCode += makeStartText()
	latexCode += makeTopText(klant,factuurNummer,omschrijving)
	latexCode += makeOrderText(order,werk,auto)
	latexCode += makeBottomText(bedrijfsinfo)
	return latexCode

def getFactuurNummer(soort):
	S = soort.name[0:1] #TODO
	jaar = dt.datetime.now().year
	counter = getCounter(S)
	return str(jaar) +'-'+ S + str(counter)

def getCounter(S):
	counters = utils.readJson('Resources/counters.json')
	c = counters[S] + 1
	counters[S] = c
	utils.writeJson('Resources/counters.json',counters)
	return c

def makeStartText():
	return utils.readfile('Invoice/top.txt')

def makeTopText(klant,factuurnummer, omschrijving):
	datum = str(dt.date.today())
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
     	"""+omschrijving+r"""\\
     	Kenteken: \hspace{0.9cm} """+klant['Kenteken']+r"""\\
     	Factuurdatum:\hspace{0.3cm} """+datum+r""" \\
     	Factuurnummer: """+factuurnummer+r"""\\
	 \end{tabular}
	}

	\renewcommand{\arraystretch}{0.9}"""
	return topText

def makeOrderText(order,werk,auto):
	btwhoog = 0
	uitbtwhoog = 0
	uitbtwgeen = 0

	orderText = ''
	orderText += r"""

	\begin{invoiceTable}
	\feetype{Producten}"""
	for o in order:
		orderText += '\unitrow{'+o['item']['name'][0:30]+'}{'+str(o['Aantal'])+'}{'+o['item']['price']['default']+'}{}'
		if float(o['item']['tax']) == 21:
			uitbtwhoog += float(o['item']['price']['default']) * o['Aantal']
		elif float(o['item']['tax']) == 0:
			uitbtwgeen += float(o['item']['price']['default']) * o['Aantal']

	if werk != None:
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
	s += str(auto['Model'])+' '
	s += "Bouwjaar:" + str(auto['Bouwjaar']) + '\n'
	s += auto['extra info']
	return s

def makeBottomText(bedrijf):
	bottomText = r"""
	\tab \tab Betaalwijze: {\bf contant of pinbetaling bij afhalen auto}
	\vspace*{\fill}
	\begin{center}
		\begin{spacing}{0.5}
		voor contact: """+bedrijf['Email']+r""" \\
		"""+bedrijf['Website']+r""" / """+bedrijf['Straat']+r""" / """+bedrijf['Postcode']+r""" """+bedrijf['Plaats']+r""" """+bedrijf['Land']+r""" \\
		KvK """+bedrijf['KvK']+r""" / BTW nr. """+bedrijf['BTW-nr.']+r""" \\
		IBAN """+bedrijf['IBAN']+r""" / Bicnr. """+bedrijf['BIC']+r"""
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