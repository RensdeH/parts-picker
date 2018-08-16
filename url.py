import encrypt

def tokensUrl():
	return '&partner_token='+encrypt.getPartnerToken()+'&token='+encrypt.getMerchantToken()

def formatUrl(format):
	return '&format='+format

def languageUrl(language):
	return 'language='+language

###################################################
def getCategories(version=1,taal='nl_NL',limit=100,format='json'):
	return "https://api.mijnwebwinkel.nl/v"+str(version)+"/categories?"+languageUrl(taal)+"&limit="+str(limit)+formatUrl(format)+"&as_tree=true&max_depth=5"+tokensUrl()

def getArticles(version=1,taal='nl_Nl',limit=100,offset=0,format='json'):
	return 'https://api.mijnwebwinkel.nl/v'+str(version)+'/articles?'+languageUrl(taal)+formatUrl(format)+'&limit='+str(limit)+'&offset='+str(offset)+tokensUrl()

def postArticle(version=1,taal='nl_Nl',format='json'):
	return 'https://api.mijnwebwinkel.nl/v'+str(version)+'/articles?'+languageUrl(taal)+formatUrl(format)+tokensUrl()


def deleteArticle(id,use_url_id=False, version=1,taal='nl_Nl',format='json'):
	if use_url_id:
		uui='true'
	else:
		uui='false'
	return 'https://api.mijnwebwinkel.nl/v'+str(version)+'/articles/'+str(id)+'?'+languageUrl(taal)+'&use_url_id='+uui+tokensUrl()

def getArticle(id,use_url_id=False, version=1,taal='nl_Nl',format='json'):
	if use_url_id:
		uui = 'true'
	else:
		uui = 'false'
	return 'https://api.mijnwebwinkel.nl/v'+str(version)+'/articles/'+str(id)+'?'+languageUrl(taal)+formatUrl(format)+'&use_url_id='+uui+tokensUrl()

def patchArticle(id,use_url_id=False, version=1,taal='nl_Nl',format='json'):
	if use_url_id:
		uui = 'true'
	else:
		uui = 'false'
	return 'https://api.mijnwebwinkel.nl/v'+str(version)+'/articles/'+str(id)+'?'+languageUrl(taal)+formatUrl(format)+'&use_url_id='+uui+tokensUrl()

def getArticleCount(version=1,taal='nl_Nl',format='json'):
	return 'https://api.mijnwebwinkel.nl/v'+str(version)+'/articles/count?'+languageUrl(taal)+formatUrl(format)+tokensUrl()

