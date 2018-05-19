import time
import requests
from flask import request, jsonify
import uuid

from app import mongo, app as a


@a.route('/getbalanceqiwi', methods=['POST'], endpoint='get_balance')
def get_balance():
    json_data = request.get_json()
    qiwi_token = json_data.get('token', '')
    phone = json_data.get('phone', '')
    api_url = 'https://edge.qiwi.com/funding-sources/v2/persons/' + phone + '/accounts'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + qiwi_token}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for c in data['accounts']:
            return c['balance']['amount']
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return response.json()


@a.route('/sendmoneyqiwi', methods=['POST'], endpoint='send_money')
def send_money(token, phone, amount):
    api_url = 'https://edge.qiwi.com/sinap/api/v2/terms/99/payments'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + token}

    id = round(time.time() * 100000)
    print(id)
    data = {'id': str(id),
            'sum': {
                'amount': amount,
                'currency': '643'},
            'paymentMethod': {
                'type': 'Account',
                'accountId': '643'},
            'comment': 'test',
            'fields': {
                'account': phone}}

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        print('ok')
    else:
        print(response.json())


@a.route('/createaccountqiwi', methods=['POST'], endpoint='create_account')
def create_account():
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



