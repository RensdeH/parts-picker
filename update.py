import api
import encrypt
import utils
import requests
import StringIO
from PIL import Image

#iets voor install.py?
def makeJsonFiles():
	utils.makeEmptyAuto()
	utils.makeEmptyCustomer()
	utils.makeEmptyCompany()
	utils.makeMockCustomer()
	utils.makeCounters()

	data = api.getArtikels(aantal = 10,silent=True)
	data2 = data[0:10]
	utils.makeMockOrder(data2)

#makeJsonFiles()

def downloadImage(item):
	size = 100,100
	iurl = 'Images/' + str(item['id']) + '.jpeg'
	if 'images' in item:
		url = item['images'][0]['urls']['full']
	else:
		return
	img_data = requests.get(url).content
	tempBuff = StringIO.StringIO()
	tempBuff.write(img_data)
	tempBuff.seek(0)
	foto = Image.open(tempBuff)
	foto.thumbnail(size,Image.ANTIALIAS)
	foto.save(iurl,"JPEG")
	return iurl

def main():
	data = api.getArtikels()
	utils.writeJson('Resources/Artikelen.json',data)
	for item in data:
		downloadImage(item)

def install():
	#install tex packages & python-qt4
	#dialog voor password
	while true:
		dialogData = raw_input("Wachtwoord:")
		if encrypt.checkPassword:
			utils.writeJson('../password.json',dialogData)
			break
		print("Wachtwoord Incorrect")

	makeJsonFiles()
	main()

#main()
