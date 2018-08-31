from Crypto.Cipher import AES
import base64
import utils

EncodedPartnerToken = 'pOwEMHkILj263JJxU150TaY4WLSrZrOg/5461micp0UnbDsyCOORiXGMmJSWRuAvPf/M75sLIsfzhJaCTsCUeg=='
EncodedMerchantToken = 'dSiUYs/Kj0EehSSIjxsyf1TrwKoFJHVLC+NIF1KCf0MhuVGGryW9YtuI7vxTyX4FesbguyDe/KllkbQ0IYlrcA=='
EncodedFromMail = 'WCFemY/IjrBxC8z2QybSmIpT/hpJcLtvNZyMsTADxl4='
EncodedToMail = 'KPCxI6QmV0baUkuQtX9HICjwsSOkJldG2lJLkLV/RyDBXYGC+/5UJai7Tn2/hQM0ZFMW9Me6x5AzkssoXfWWpg=='
EncodedGoogleAPI = 'KPCxI6QmV0baUkuQtX9HIFh0QM5YjEVyk5CvFQjnnFjz8l2whqRYS4rs53Zqw3omNQOurWBJFpr3Ts5vpzt+dg=='
EncodedCheck = 'KPCxI6QmV0baUkuQtX9HICjwsSOkJldG2lJLkLV/RyAo8LEjpCZXRtpSS5C1f0cgzw9nbTcmxhRFVkCnILyKhg=='

passdict = utils.readJson('../password.json')
if passdict == {}:
	password = raw_input("Password:")
else:
	password = passdict['password']
#Used once for generating encoded key paste above
def makeKey(p,Key):
	msg = Key.rjust(64)
	cipher = AES.new(key=p.rjust(32))
	enc = cipher.encrypt(msg)
	#print(enc)
	#print(cypher.decrypt(enc))
	encoded = base64.b64encode(enc)
	return encoded

def getDecoded(encoded):
	cipher = AES.new(key=password.rjust(32))
	decoded = cipher.decrypt(base64.b64decode(encoded))
	return decoded

def getPartnerToken():
	return getDecoded(EncodedPartnerToken)

def getMerchantToken():
	return getDecoded(EncodedMerchantToken)

def getFromMail():
	return getDecoded(EncodedFromMail)

def getToMail():
	return getDecoded(EncodedToMail).strip()

def getGoogleAPI():
	return getDecoded(EncodedGoogleAPI).strip()

def getCheck():
	return getDecoded(EncodedCheck).strip()

def checkPassword(attempt):
		cipher = AES.new(key=attempt.rjust(32))
		decoded = cipher.decrypt(base64.b64decode(EncodedCheck))
		if decoded.strip() == 'CodeCracked!':
			return True
		else:
			return False
