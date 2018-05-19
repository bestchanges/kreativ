import requests
from flask import request, jsonify, app
import uuid
from app import mongo, app as a


def get_qiwi_balance(token, phone):
    api_url = 'https://edge.qiwi.com/funding-sources/v2/persons/' + phone + '/accounts'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + token}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for c in data['accounts']:
            if c['hasBalance']:
                return c['balance']['amount']
            else:
                print('no balance')
                return None
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

@a.route('/createaccountqiwi', methods=['POST'])
def createaccountqiwi():
    json_data = request.get_json()
    qiwi_token = json_data.get('token', '')
    phone = json_data.get('phone', '')
    wallet = json_data.get('wallet', '')
    acc_uuid = uuid.uuid4()
    data = {
        'token': qiwi_token,
        'phone': phone,
        'balance_phone': 0,
        'balance_wallet': 0,
        'wallet': wallet,
        'uuid': acc_uuid
    }
    account = mongo.db.account.insert(data)
    return jsonify({'result': "OK",
                    'uuid': acc_uuid})


@a.route('/sendqiwimoney', methods=['POST'])
def send_money(token, phone):
    api_url = 'https://edge.qiwi.com/sinap/api/v2/terms/99/payments'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + token}
    body = {
        "id": "11111111111111",
        "sum": {
            "amount": 10,
            "currency": "643"
        },
        "paymentMethod": {
            "type": "Account",
            "accountId": "643"
        },
        "comment": "test",
        "fields": {
            "account": phone
        }
    }

    response = requests.get(api_url, headers=headers, body=body)



tkn = '7820a390d136f825461739c26ae7324b'

phn = '79636853224'

print(get_qiwi_balance(tkn, phn))