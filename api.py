import requests
import json
from time import sleep
import url

def getStoreDetails():
	Url = url.getStoreDetails()
	resp = requests.get(Url)
	checkStatus(resp)
	return json.loads(resp.text)

def getOrders(aantal=0,silent=False):
	if aantal == 0:
		aantal = getOrderCount()
	print(aantal)
	lijst = []
	for offset in range(0,aantal,100):
		if not silent:
			print('Order Offset:'+str(offset))
		Url = url.getOrders(offset=offset)
		resp = requests.get(Url)
		checkStatus(resp,time=0)
		lijst.extend(json.loads(resp.text))
	return lijst

def getCategories():
	Url = url.getCategories()
	resp = requests.get(Url)
	checkStatus(resp,time=0)
	return json.loads(resp.text)

def getOrderCount():
	Url = url.getOrderCount()
	resp = requests.get(Url)
	checkStatus(resp,time=0)
	return json.loads(resp.text)['count']

def getArtikelCount():
	Url = url.getArticleCount()
	resp = requests.get(Url)
	checkStatus(resp,time=0)
	return json.loads(resp.text)['count']

def getArtikels(aantal=0,silent=False):
	if aantal == 0:
		aantal = getArtikelCount()
	lijst = []
	for offset in range(0,aantal,100):
		if not silent:
			print('Offset:'+str(offset))
		Url = url.getArticles(offset=offset)
		resp = requests.get(Url)
		checkStatus(resp,time=0)
		lijst.extend(json.loads(resp.text))
	return lijst

def getArtikel(id,use_url_id=False):
	Url = url.getArticle(id,use_url_id)
	resp = requests.get(Url)
	checkStatus(resp)
	return json.loads(resp.text)

def deleteArtkel(id,use_url_id=False):
	Url = url.deleteArticle(id,use_url_id)
	resp = requests.delete(Url)
	checkStatus(resp)
	return json.loads(resp.text)

def postArtikel(data):
	Url = url.postArticle()
	resp =requests.post(url=Url,data=data)
	checkStatus(resp)
	return json.loads(resp.text)

def patchArtikel(id,data,use_url_id=False,taal='nl_NL'):
	Url = url.patchArticle(id,use_url_id=use_url_id,taal=taal)
	resp =requests.patch(url=Url,data=data)
	checkStatus(resp)
	return json.loads(resp.text)

def getUrlId(id):
	try:
		resp = getArtikel(id)['categories'][0]['article_url_id']
	except:
		resp = id
	return resp

def checkStatus(resp,time=0.65):
	if resp.status_code!=200:
		print(resp.text)
	sleep(time)

