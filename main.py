import requests as r
from fake_useragent import UserAgent
import raname
import traceback as tbb

from urllib.parse import urlencode
import hashlib
import re
import time
import json
from datetime import datetime as date
import random


def create():
    req = r.get("https://www.1secmail.com/api/v1/" +
                '?action=genRandomMailbox&count=1')
    if req.status_code:
        res = req.json()[0]
        return res
    else:
        create()


def msg(mail):
    base = mail.split('@')
    mailname = base[0]
    maildomain = base[1]
    req = r.get("https://www.1secmail.com/api/v1/" +
                f'?action=getMessages&login={mailname}&domain={maildomain}')
    if req.status_code:
        res = req.json()
        if (len(res) >= 1):
            msgid = res[0]['id']
            req = r.get("https://www.1secmail.com/api/v1/" +
                        f'?action=readMessage&login={mailname}&domain={maildomain}&id={msgid}')
            if req.status_code:
                return req.text
            else:
                msg(mail)
    else:
        msg(mail)


def gw(t1, t2, s):
    try:
        t1_escaped = re.escape(t1)
        t2_escaped = re.escape(t2)
        regexPattern = f"{t1_escaped}(.+?){t2_escaped}"
        str_found = re.search(regexPattern, s, re.DOTALL).group(1).strip()
        return str_found
    except AttributeError:
        return ''


def getsernum():
    with open('serials.txt', 'r', encoding="utf-8") as f:
        serials = f.readlines()
    serial = f"{''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(4)]).upper()}{random.randint(00000,999999)}"
    if not serial in serials:
        with open('serials.txt', 'a') as f:
            f.write(f"{serial}\n")
        return serial
    else:
        getsernum()

def productID(loginData):
    serverApiCode = '%2s&JD6twAf'
    shaObj = hashlib.sha256()
    shaObj.update((loginData['UID'] + serverApiCode).encode('utf-8'))
    authToken = shaObj.hexdigest()
    dataSugest = {
        "authToken": authToken,
        "UID": loginData["UID"],
        "UIDSignature": loginData["UIDSignature"],
        "signatureTimestamp": loginData["signatureTimestamp"],
        "data": {
            "ProductName": str(random.choice(['ra','ad','qe','po','w','ro','r','b','gu'])),
            "DistinctName": True
        }
    }
    url = "https://id.yamaha.com/id/api/sfdcAPProductSuggestCampaign.json"
    head = {
        'authority': 'id.yamaha.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https//id.yamaha.com',
        'pragma': 'no-cache',
        'referer': 'https//id.yamaha.com/',
        'sec-ch-ua': '"(Not(A:Brand";v="99", "Chromium";v="115", "Google Chrome";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(UserAgent().random),
        'x-requested-with': 'XMLHttpRequest'
    }
    req = r.post(url, headers=head, json=dataSugest)
    # input(req.json())
    return req.json()

def payloadProduct(loginData):
    today = f"{random.randint(2016,2023)}-{random.randint(1,12)}-{random.randint(1,28)}"
    products = productID(loginData)['responseBody']['ProductInfo']
    product = random.choice(products)
    productId = product['ProductId']
    productName = product['DisplayName']
    serialNumber = getsernum()
    print(f"[/] ProductName: {productName}")
    print(f"[/] ProductID: {productId}")
    print(f"[/] SerialNumber: {serialNumber}")
    gigyaIdentifier = 'YMID'
    serverApiCode = '%2s&JD6twAf'
    shaObj = hashlib.sha256()
    shaObj.update((loginData['UID'] + serverApiCode).encode('utf-8'))
    authToken = shaObj.hexdigest()
    postdata = {
        "authToken": authToken,
        "UID": loginData["UID"],
        "UIDSignature": loginData["UIDSignature"],
        "signatureTimestamp": loginData["signatureTimestamp"],
        "data": {
            "ProductId": productId,
            "SerialNumber": serialNumber,
            "PurchaseDate": today,
            "ProductUse": 0,
            "PurchaseType": 0,
            "LastName": loginData["profile"]["lastName"],
            "GigyaIdentifier": gigyaIdentifier,
            "GigyaUId": loginData["UID"],
            "Email": loginData["profile"]["email"],
            "FlowKeyCode": None,
            "TomplayCode": None,
            "RegistrationUrl": "https://id.yamaha.com/"
        }
    }

    return json.dumps(postdata)


def login(email: str,
          password: str):
    url = "https://socialize-us.yamaha.com/accounts.login"
    data = {
        "loginID": email,
        "password": password,
        "sessionExpiration": "2592000",
        "targetEnv": "jssdk",
        "include": "profile,data,emails,subscriptions,preferences,",
        "includeUserInfo": True,
        "loginMode": "standard",
        "lang": "id",
        "APIKey": "3_hK1zVlmR82Jgi_rYYTTvxhL5YBEh8ugjfIhhadc4fTZS4T4Efn7kUuacAKCRt-T7",
        "source": "showScreenSet",
        "sdk": "js_canary",
        "authMode": "cookie",
        "pageURL": "https//id.yamaha.com/id/news_events/2021/20210701_RegistrasiAlatMusikYamaha.html",
        "sdkBuild": "15535",
        "format": "json",
    }

    head = {
        'authority': 'socialize-us.yamaha.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https//id.yamaha.com',
        'pragma': 'no-cache',
        'referer': 'https//id.yamaha.com/',
        'sec-ch-ua': '"(Not(A:Brand";v="99", "Chromium";v="115", "Google Chrome";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(UserAgent().random)
    }

    req = r.post(url, headers=head, data=data)
    return req.json(), req.cookies


def regisProduct(loginData, kuki):
    print(f'[.] Add Product')
    data = json.loads(payloadProduct(loginData))
    url = "https://id.yamaha.com/id/api/sfdcAPProductRegistration.json"
    head = {
        'authority': 'id.yamaha.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https//id.yamaha.com',
        'pragma': 'no-cache',
        'referer': 'https//id.yamaha.com/',
        'sec-ch-ua': '"(Not(A:Brand";v="99", "Chromium";v="115", "Google Chrome";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(UserAgent().random),
        'x-requested-with': 'XMLHttpRequest'
    }
    req = r.post(url, headers=head, json=data)
    return req.json()


def addProduk(imel, pw):
    atemps = 0
    print(f'[.] Login')
    addedprod = 0
    loginData, loginCookies = login(imel, pw)
    # result = ''
    while addedprod < addprod:
        # with open('akun.txt', 'r') as f:
        #     akuns = f.read()
        atemps += 1
        regProd = regisProduct(loginData, loginCookies)
        if regProd['errorMessage'] == 'SFDC error':
            print(f"[!] Add Product Error : {regProd['errorMessage']}")
        else:
            addedprod += 1
            print(f'[{addedprod}] Add Product Success')
            prodID = regProd['responseBody']['AssetInfo']['ProductId']
            seriNum = regProd['responseBody']['AssetInfo']['SerialNumber']
            assID = regProd['responseBody']['AssetInfo']['AssetId']
            variation = regProd['responseBody']['AssetInfo']['Variation']
            buyDate = regProd['responseBody']['AssetInfo']['PurchaseDate']
            # if not f"{imel}|{pw}" in akuns:
            #     result += f"{imel}|{pw}|{prodID}|{seriNum}|{assID}|{variation}|{buyDate}|{atemps} Percobaan"
            # else:
            #     result += f"|{prodID}|{seriNum}|{assID}|{variation}|{buyDate}|{atemps} Percobaan"
    else:
        with open('akun.txt', 'a') as f:
            f.write(f"\n{imel} {pw}")

def regToken():
    url = 'https://socialize-us.yamaha.com/accounts.initRegistration'
    api_key = '3_hK1zVlmR82Jgi_rYYTTvxhL5YBEh8ugjfIhhadc4fTZS4T4Efn7kUuacAKCRt-T7'
    head = {
        'authority': 'socialize-us.yamaha.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://id.yamaha.com',
        'pragma': 'no-cache',
        'referer': 'https://id.yamaha.com/',
        'sec-ch-ua': '"(Not(A:Brand";v="99", "Chromium";v="115", "Google Chrome";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Linux',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(UserAgent().random)
    }
    params = {
        'APIKey': api_key,
        'source': 'showScreenSet',
        'sdk': 'js_latest',
        'authMode': 'cookie',
        'sdkBuild': '15535',
        'format': 'json'
    }
    req = r.get(url, headers=head, params=params)
    return req.json()['regToken']


def regisAkun(imel):
    url = 'https://socialize-us.yamaha.com/accounts.register'
    head = {
        'authority': 'socialize-us.yamaha.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://id.yamaha.com',
        'pragma': 'no-cache',
        'referer': 'https://id.yamaha.com/',
        'sec-ch-ua': '"(Not(A:Brand";v="99", "Chromium";v="115", "Google Chrome";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(UserAgent().random)
    }
    while len((nama := str(raname.getname()).split(' '))) < 2:
        continue
    else:
        fname = nama[0]
        lname = nama[1]
    print(f'[.] Nama : {nama[0]} {nama[1]}')
    payload = {
        'email': imel,
        'password': pw,
        'regToken': regToken(),
        'regSource': 'https://id.yamaha.com/id/products/musical_instruments/guitars_basses/index.html',
        'profile': {
            "country": "Indonesia",
            "firstName": fname,
            "lastName": lname,
            "birthMonth": str(random.randint(1, 12)),
            "birthDay": str(random.randint(1, 28)),
            "birthYear": str(random.randint(1987, 2003))
        },
        'preferences': {
            "terms": {"country": {"isConsentGranted": 'true'}},
            "privacy": {"country": {"isConsentGranted": 'true'}},
            "countryAgeConsent": {"isConsentGranted": 'true'}
        },
        'displayedPreferences': {
            "terms.country": {"docVersion": 'null', "docDate": "2019-03-26T00:00:00Z"},
            "privacy.country": {"docVersion": 'null', "docDate": "2021-07-29T00:00:00Z"},
            "countryAgeConsent": {"docVersion": 'null', "docDate": "2022-02-28T00:00:00Z"}
        },
        'data': '{"gender":"Female"}',
        'lang': 'id',
        'finalizeRegistration': True,
        'targetEnv': 'jssdk',
        'sessionExpiration': '2592000',
        'include': 'profile,data,emails,loginIDs,subscriptions,preferences,',
        'includeUserInfo': True,
        'subscriptions': {
                "newsletter2": {"email": {"isSubscribed": 'true'}},
            "newsletter1": {"email": {"isSubscribed": 'true'}}
        },
        'APIKey': '3_hK1zVlmR82Jgi_rYYTTvxhL5YBEh8ugjfIhhadc4fTZS4T4Efn7kUuacAKCRt-T7',
        'source': 'showScreenSet',
        'sdk': 'js_latest',
        'pageURL': 'https://id.yamaha.com/id/products/musical_instruments/',
        'sdkBuild': '15535',
        'format': 'json'
    }

    data = f"email={payload['email']}&password={payload['password']}&regToken={payload['regToken']}&regSource={payload['regSource']}&profile={payload['profile']}&preferences={payload['preferences']}&displayedPreferences={payload['displayedPreferences']}&data={payload['data']}&lang={payload['lang']}&finalizeRegistration={payload['finalizeRegistration']}&targetEnv={payload['targetEnv']}&sessionExpiration={payload['sessionExpiration']}&include={payload['include']}&includeUserInfo={payload['includeUserInfo']}&subscriptions={payload['subscriptions']}&APIKey={payload['APIKey']}&source={payload['source']}&sdk={payload['sdk']}&pageURL={payload['pageURL']}&sdkBuild={payload['sdkBuild']}&format={payload['format']}"

    print(f'[.] Mendaftar')
    req = r.post(url, headers=head, data=data)
    # print(req.json())

    print(f'[.] Cek Email')
    ts = time.time()
    while (round(time.time() - ts) < 10):
        pesan = msg(imel)
        if pesan != None:
            break
    else:
        print('[!] Email Tidak Kunjung Masuk')
        return False
    linkVerif = gw('<!--[if mso]>\\n<a href=\\"',
                   '\\">\\n ', pesan).replace('\\', '').strip()
    print(f'[.] Link Verifikasi Email : {linkVerif}')
    verifEmail = r.get(linkVerif, headers={
                       'user-agent': str(UserAgent().random)})
    if 'Alamat email Anda berhasil diverifikasi.' in verifEmail.text:
        print('[-] Sukses Verif Email')
        return True
    else:
        with open('verifemail.html', 'w') as f:
            f.write(verifEmail.text)
        exit()


addprod = 2



while True:
    print('+--------------------------------------------+')
    try:
        while len((pw := str(raname.getname()).replace(' ', '') + str(random.randint(100, 9999)))) < 10:
            continue
        else:
            imel = str(raname.getname()).replace(' ', '') + str(random.randint(10, 999)) + \
                '@' + \
                str(random.choice(
                    ['icznn', 'laafd', 'ezztt', 'vjuum'])) + '.com'
            print(f'[.] Email : {imel}')
            print(f'[-] Password : {pw}')
            if regisAkun(imel):
                addProduk(imel, pw)
    except:
        continue
        # exit(tbb.format_exc())
