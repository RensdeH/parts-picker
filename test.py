#import api

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
