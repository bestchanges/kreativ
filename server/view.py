import time
from utils import *
from flask import request, jsonify
from app import app as a


@a.route('/sendmoneyqiwi', methods=['POST'], endpoint='send_money_qiwi')
def send_money_qiwi():
    json_data = request.get_json()
    token = json_data.get('token', '')
    phone = json_data.get('phone', '')
    amount = json_data.get('amount', '')
    api_url = 'https://edge.qiwi.com/sinap/api/v2/terms/99/payments'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + token}

    id = round(time.time() * 100000)
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
        return jsonify({'code': 200,
                        'message': id})
    else:
        return response.text


@a.route('/createaccount', methods=['POST'], endpoint='create_accounts')
def create_accounts():

    #создание аккаунтов



    json_data = request.get_json()
    qiwi_token = json_data.get('token', '')
    phone = json_data.get('phone', '')
    wallet = json_data.get('wallet', '')

    balance = get_balance(qiwi_token, phone)
    if not isinstance(balance, float):
        return balance

    data_qiwi = create_wallet(phone, 'RUR QIWI', balance, '', qiwi_token, phone)

    data_eth = create_eth_wallet()

    data_eth = create_wallet(wallet, 'ETH', '', data_eth['private_key'], '', data_eth['address'])

    return jsonify({'result': "OK",
                    'uuid': data['account_uuid']})


@a.route('/get_rates', methods=['GET'], endpoint='get_rates')
def get_rates():
    qw_eth = get_rate('https://www.bestchange.ru/qiwi-to-ethereum.html')
    eth_qw = get_rate('https://www.bestchange.ru/ethereum-to-qiwi.html')
    return {'qw_eth': qw_eth,
            'eth_qw': eth_qw}



@a.route('/get_wallet', methods=['POST'])
def get_address():
    params = request.get_json()
    account_uuid = params.get('account')
    data = create_eth_wallet(account_uuid)
    # TODO: check account by uuid

    return jsonify({'address': data['address'], 'uuid': data['uuid']})


