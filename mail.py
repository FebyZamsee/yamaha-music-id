#1secmail.com
import requests as r,json
url="https://www.1secmail.com/api/v1/"
def create():
	req = r.get(url+'?action=genRandomMailbox&count=1')
	if req.status_code:
		res = req.json()[0]
		return res
	else: create()

def msg(mail):
	base = mail.split('@')
	mailname = base[0]
	maildomain = base[1]
	req = r.get(url+f'?action=getMessages&login={mailname}&domain={maildomain}')
	if req.status_code:
		res = req.json()
		if (len(res) >= 1):
			msgid = res[0]['id']
			req = r.get(url+f'?action=readMessage&login={mailname}&domain={maildomain}&id={msgid}')
			if req.status_code:
				return req.text
			else: msg(mail)
	else: msg(mail)
