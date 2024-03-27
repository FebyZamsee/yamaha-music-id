import hashlib
import json
from flask import *
app = Flask(__name__)

@app.route('/payload', methods=['GET','POST'])
def payloadProduct():
    loginData = request.json
    gigyaIdentifier = 'YMID'
    serverApiUrl = 'https://id.yamaha.com/id'
    serverApiCode = '%2s&JD6twAf'
    apiurl = serverApiUrl + '/api/sfdcAPProductRegistrationList.json'
    shaObj = hashlib.sha256()
    shaObj.update((loginData['UID'] + serverApiCode).encode('utf-8'))
    authToken = shaObj.hexdigest()
    postdata = {
        "authToken": authToken,
        "UID": loginData['UID'],
        "UIDSignature": loginData['UIDSignature'],
        "signatureTimestamp": loginData['signatureTimestamp'],
        "data": {
            "ProductId": "id_1457730",
            "SerialNumber": "IJN140499",
            "PurchaseDate": "2023-11-17",
            "ProductUse": 0,
            "PurchaseType": 0,
            "LastName": loginData['profile']['lastName'],
            "GigyaIdentifier": gigyaIdentifier,
            "GigyaUId": loginData['UID'],
            "Email": loginData['profile']['email'],
            "FlowKeyCode": None,
            "TomplayCode": None,
            "RegistrationUrl": "https://id.yamaha.com/"
        }
    }
    return jsonify(postdata)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7890)