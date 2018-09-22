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



class Test():
	def __init__(self,data):
		self.Data = data
	def rebuild(self):
		print(self.Data)

def foo():
	list = ['ok']
	les = ['2ok']
	t = Test(list)
	t2 = Test(les)
	list.append('hi')
	les.append('2vfd')
	t.rebuild()
	t2.rebuild()
foo()
