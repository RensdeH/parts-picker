import subprocess
import utils
import datetime as dt
import os
import shutil
from codecs import open

def startFactuur(data,typeFactuur):
	if typeFactuur != utils.TypeFactuur.Afdrukvoorbeeld:
		utils.writeJson('Resources/Klanten/'+data['Klant']['Naam']+'.json',data['Klant'])
	makeFactuur(data,typeFactuur)

def makeFactuur(data,typeFactuur):
	factuurNummer = getFactuurNummer(data['soortFactuur'],typeFactuur)
	data['FactuurNummer'] = factuurNummer
	pdfNaam = data['Klant']['Naam'] +' '+ factuurNummer + ' ' + data['Klant']['Kenteken']
	data['bedrijf'] = standardBedrijfInfo()
	if typeFactuur == utils.TypeFactuur.Kostenraming:
		data['Omschrijving'] = 'Kostenraming'
	elif typeFactuur == utils.TypeFactuur.Definitief:
		if data['soortFactuur'] == utils.SoortFactuur.Inkoop:
			data['Omschrijving'] = 'Inkoop-Factuur'
		else:
			data['Omschrijving'] = 'Factuur'
	else:
		data['Omschrijving'] = 'Afdrukvoorbeeld'
	workingDir = 'Invoice/'
	filename = pdfNaam + '.tex'
	pdffilename = pdfNaam + '.pdf'

	file = open(workingDir + filename,'w',encoding='utf8')
	latexCode = makeTex(data,typeFactuur)
	file.write(latexCode)
	file.close()
	proc = runpdflatex(filename,workingDir)
	proc.wait()

	if typeFactuur == utils.TypeFactuur.Afdrukvoorbeeld:
		shutil.move(workingDir + filename,'Facturen/Temp/' + filename)
		shutil.move(workingDir + pdffilename,'Facturen/Temp/' + pdffilename)
		openfile(pdffilename,'Facturen/Temp/')
	else:
		shutil.move(workingDir + pdffilename,'Facturen/' + pdffilename)
		print("moved file to " + 'Facturen/' + pdffilename)
		try:
			shutil.copy('Facturen/' + pdffilename,'/home/chris/Dropbox/B. MX5-Winkel administratie/MX5Winkel Facturen/' + pdffilename)
			print("Copied file to Dropbox")
		except:
			print('Dropbox directory not found!')
		openfile(pdffilename,'Facturen/')

def makeTex(data,typeFactuur):
	order = data['Artikelen']
	custom = data['Custom']
	werk = data['Werk']
	klant = data['Klant']
	bedrijfsinfo = data['bedrijf']
	factuurNummer = data['FactuurNummer']
	omschrijving = data['Omschrijving']
	betaalwijze = "per pin"
	if data['soortFactuur'] == utils.SoortFactuur.Reparatie:
		betaalwijze += " bij afhalen auto\\\\\\tab\\tab\\tab\\tab\\tab\\hspace{0.2cm}"
	betaalwijze += " of vooraf overmaken."
	if data['soortFactuur'] == utils.SoortFactuur.Verkoop:
		betaalwijze = "via bankoverschrijving voor afhalen auto"
	if data['soortFactuur'] == utils.SoortFactuur.Inkoop:
		betaalwijze = "via bankoverschrijving"
	auto = None
	if 'Auto' in data:
		auto = data['Auto']

	latexCode = ""
	latexCode += makeStartText()
	latexCode += makeTopText(klant,factuurNummer,omschrijving,typeFactuur)
	latexCode += makeOrderText(order,werk,auto,custom,data)
	latexCode += makeBottomText(bedrijfsinfo,betaalwijze)
	return latexCode

def getFactuurNummer(soort,typeFactuur):
	S = soort.name[0:1]
	jaar = dt.datetime.now().year
	counter = getCounter('C',typeFactuur)
	if typeFactuur == utils.TypeFactuur.Kostenraming:
		return 'Raming' + str(jaar) +'-'+ 'K' + str(counter)
	return str(jaar) +'-'+ S + str(counter)

def getCounter(S,typeFactuur):
	counters = utils.readJson('Resources/counters.json')
	c = counters.setdefault(S,100) + 1
	if typeFactuur != utils.TypeFactuur.Afdrukvoorbeeld:
		counters[S] = c
		utils.writeJson('Resources/counters.json',counters)
	return c

def makeStartText():
	return utils.readfile('Invoice/top.txt')

def makeTopText(klant,factuurnummer, omschrijving,typeFactuur):
	datumData = dt.date.today()
	datum = datumData.strftime("%d-%m-%Y")
	topText = r"""\begin{tabular}[t]{l@{}}
    	\tab """+utils.replaceSpecialChars(klant['Naam'])+r""" \\
    	\tab """+utils.replaceSpecialChars(klant['Straat'])+r"""\\
    	\tab """+klant['Postcode']+r""" """+utils.replaceSpecialChars(klant['Plaats'])+r"""\\
    	[0.5cm]
    	\tab Telefoon: """+utils.replaceSpecialChars(klant['Telefoon'])+r"""\\
    	\tab Email: """+utils.replaceSpecialChars(klant['email'])
	if klant["BTW"] != '':
		topText+=r"""\\
		\tab BTW nr: """+utils.replaceSpecialChars(klant['BTW'])

	topText+=r"""\\
	\end{tabular}

	\hfill

	\begin{tabular}[t]{l@{}}
     	"""+utils.replaceSpecialChars(omschrijving)

	if typeFactuur == utils.TypeFactuur.Kostenraming:
		topText += r"""\\
		Datum:\hspace{1.5cm} """+utils.replaceSpecialChars(datum)
	else:
		topText += r"""\\
		Factuurdatum:\hspace{0.3cm} """+utils.replaceSpecialChars(datum)+r""" \\
		Factuurnummer: """+utils.replaceSpecialChars(factuurnummer)

	if klant['Kenteken'] != '':
		topText += r"""\\
		\\
		KM-stand: \hspace{1.1cm} """+utils.replaceSpecialChars(klant['km-stand'])

	if klant['Kenteken'] != '':
		topText += r"""\\
		\\
		Kenteken: \hspace{1.1cm} """+utils.replaceSpecialChars(klant['Kenteken'])

	topText += r"""\\
	 \end{tabular}
	}

	\renewcommand{\arraystretch}{0.9}"""
	return topText

def makeOrderText(order,werk,auto,custom, data):
	btwhoog = 0
	uitbtwhoog = 0
	uitbtwgeen = 0

	orderText = r"""\begin{invoiceTable}"""

	if order != [] or custom != []:
		orderText += r"""\feetype{Producten}"""

	for o in order + custom:
		orderText += o.strLatex()
		if o.Tax == 21:
			uitbtwhoog += o.totaalPrijs()
		elif o.Tax == 0:
			uitbtwgeen += o.totaalPrijs()

	if werk != []:
		orderText += r"""\feetype{Gewerkte Uren}"""

	for o in werk:
		orderText += o.strLatex()
		if o.Tax == 21:
			uitbtwhoog += o.totaalPrijs()
		elif o.Tax == 0:
			uitbtwgeen += o.totaalPrijs()

	if auto['Model'] != '':
		if data['soortFactuur'] == utils.SoortFactuur.Inkoop:
			feetype = 'Inkoop Auto'
		else:
			feetype = 'Auto'
		orderText += r"""
		\feetype{"""+utils.replaceSpecialChars(feetype)+'}'
		autoOmschrijving = getCarDes(auto)
		orderText += r"""\unitrow{"""+getCarDes(auto)+'}{'+str(1)+'}{'+utils.replaceSpecialChars(auto['Prijs'])+'}{}'
		uitbtwgeen += float(auto['Prijs'])

	btwhoog = (uitbtwhoog/1.21)*0.21
	orderText+=r"""
	\setendtotal{"""+str(uitbtwhoog)+'}{'+str(btwhoog)+'}{'+str(uitbtwgeen)+r"""}{0}\\
	\end{invoiceTable}
	"""
	return orderText

def getCarDes(auto):
	s = ''
	s += "Model: " + utils.replaceSpecialChars(str(auto['Model'])) + r"""\\"""
	s += "Kenteken: " + utils.replaceSpecialChars(str(auto['Kenteken'])) +r"""\\"""
	s += "Bouwjaar: " + utils.replaceSpecialChars(str(auto['Bouwjaar'])) +r"""\\"""
	s += "Km-stand: " + utils.replaceSpecialChars(str(auto['km-stand'])) +r"""\\"""
	s += "Meldcode: " + utils.replaceSpecialChars(str(auto['Meldcode'])) +r"""\\"""
	if str(auto['APK']) != '':
		s += "APK: " + utils.replaceSpecialChars(str(auto['APK'])) +r"""\\"""
	s += utils.replaceSpecialChars(auto['extra info'])
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

def runpdflatex(fileName,workingDir):
	print(fileName)
	debug = False
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
