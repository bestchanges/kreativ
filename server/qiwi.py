import time
import requests
from flask import request, jsonify
from utils import create_wallet, get_rate
from app import mongo, app as a


#@a.route('/getbalanceqiwi', methods=['POST'], endpoint='get_balance')
def get_balance(qiwi_token, phone):
    #json_data = request.get_json()
    #qiwi_token = json_data.get('token', '')
    #phone = json_data.get('phone', '')
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


@a.route('/createaccountqiwi', methods=['POST'], endpoint='create_account_qiwi')
def create_account_qiwi():
    json_data = request.get_json()
    qiwi_token = json_data.get('token', '')
    phone = json_data.get('phone', '')
    balance = get_balance(qiwi_token, phone)
    if not isinstance(balance, float):
        return balance
    data = create_wallet(phone, 'RUR QIWI', balance, '', qiwi_token)
    return jsonify({'result': "OK",
                    'uuid': data['account_uuid']})


@a.route('/get_rates', methods=['GET'], endpoint='get_rates')
def get_rates():
    qw_eth = get_rate('https://www.bestchange.ru/qiwi-to-ethereum.html')
    eth_qw = get_rate('https://www.bestchange.ru/ethereum-to-qiwi.html')
    return {'qw_eth': qw_eth,
            'eth_qw': eth_qw}

