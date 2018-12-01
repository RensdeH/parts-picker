import api
import csv

def main():
	lijst = api.getArtikels()
	aantal =0
	for l in lijst:
		if 'sku' in l:
			if l['sku'].lower().startswith('gvmx'):
				if 'tax' in l:
					if float(l['tax']) != 0:
						aantal += 1
						print(l['sku'])
	print(aantal)

def main2():
	lijst = api.getOrders()
	with open('address.csv','w') as csvfile:
		writer = csv.writer(csvfile)
		for l in lijst:
			writer.writerow(prettyprint(l))

def prettyprint(order):
	customer = order['debtor']['name'].encode('utf-8')
	address = order['debtor']['address']['invoice']
	country = address['country'].encode('utf-8')
	zipcode = address['zipcode'].upper().replace(' ',"").encode('utf-8')
	street = address['street'].encode('utf-8')
	number = address['number'].encode('utf-8')
	city = address['city'].encode('utf-8')
	country = address['country'].encode('utf-8')
	return [customer,street+' '+number+'\n'+zipcode+' '+city,country]

main2()
