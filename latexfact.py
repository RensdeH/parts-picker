import subprocess
import utils
#klasse om een factuur te maken
#alle input moeten kunnen 
#opmaak is dezelfde
#inputs:
#-Bedrijfs informatie
#-Klant info
#-producten (prijzen, aantallen, btw)
#input kan ook json bestand zijn

def startFactuur(order,klant,soort):
	#kies klant dialog
	#klant = utils.readJson('Resources/emptyCustomer.json')
	bedrijf = standardBedrijfInfo()
	makeFactuur(order,klant,bedrijf,soort)

def makeFactuur(order,klantinfo,bedrijfsinfo,soort):
	workingDir = 'Invoice/'
	filename = klantinfo['id'] + '.tex'
	pdffilename = klantinfo['id'] + '.pdf'
	file = open(workingDir + filename,'w')
	latexCode = makeTex(order, klantinfo, bedrijfsinfo,soort)
	file.write(latexCode)
	file.close()
	runpdflatex(filename,True,workingDir)	
	openfile(pdffilename,workingDir)

def makeTex(order, klantinfo, bedrijfsinfo,soort):
	factuurNummer = getNummer(soort)
	latexCode = ""
	latexCode += makeTopText(klantinfo,bedrijfsinfo,factuurNummer)
	latexCode += makeOrderText(order)
	latexCode += makeBottomText(bedrijfsinfo)
	return latexCode

def getNummer(s):
	return s.name #TODO

def makeOrderText(order):
	orderText = ''
	#sorteer de items in de order op soort (werk of product)
	orderText += '\\feetype{Gebruikte Producten}'
	for o in order:
		#if o is product
		orderText += '\unitrow{'+o['item']['name'][0:30]+'}{'+str(o['Aantal'])+'}{'+o['item']['price']['default']+'}{}\n'
	#for o in order:
		#if o is werk
		###
	orderText += '\subtotal*'
	return orderText



def makeTopText(klant,bedrijf,factuurnummer):
	topText = ''
	topText += '\documentclass{invoice}\n'

	topText += '\def \\tab {\hspace*{3ex}}\n'

	topText += '\\begin{document}\n'

	topText += '\hfil{\Huge\\bf '+bedrijf['Bedrijfsnaam']+'}\hfil\n'
	topText += '\\bigskip\\break % Whitespace\n'
	topText += '\hrule % Horizontal line\n'

	topText += bedrijf['Straat'] + ' \hfill '+bedrijf['Telefoon']+' \\\\\n'
	topText += bedrijf['Plaats']+', '+bedrijf['Postcode']+' \hfill '+bedrijf['Email']+'\n'
	topText += '\\\\ \\\\\n'
	topText += '{\\bf Factuur:} \\\\\n'
	topText += '\\tab '+klant['Naam']+' \\\\\n'
	topText += '\\tab Generic Corporation \\\\ \n'

	topText += '{\\bf Datum:} \\\\\n'
	topText += '\\tab \\today \\\\\n'

	topText += '\\begin{invoiceTable}\n'
	return topText

def makeBottomText(bedrijfsinfo):
	bottomText = ''
	
	bottomText += '\end{invoiceTable}\n'
	bottomText += '\end{document}\n'
	return bottomText

def runpdflatex(fileName,debug,workingDir):
	print(fileName)
	if debug:
		proc = subprocess.Popen(['pdflatex','-interaction','nonstopmode',fileName],cwd=workingDir)
		proc.communicate()
	else:
		proc = subprocess.Popen(['pdflatex','-interaction','batchmode',fileName],cwd=workingDir)
		proc.communicate()

def openfile(filename,workingDir):
	proc = subprocess.Popen(['xdg-open',filename],cwd=workingDir)
	proc.communicate()


#####################################################################3


def standardBedrijfInfo():
	company = utils.readJson('Resources/company.json')
	if company == {}:
		company = {} #TODO
		utils.writeJson('Resources/company.json',utils.makeCompany())
	return company

def klantInfo():
	#invulapplication
	
	return {}

