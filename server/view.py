import json
import time
from uuid import UUID

from bson import ObjectId

from utils import *
from flask import request, jsonify, session
from app import app as a


def default_encode(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, UUID):
        return str(o)


json_encoder = json.JSONEncoder(indent=4, default=default_encode)


@a.route('/create_offer', methods=['POST'], endpoint='create_offer')
def create_offer():
    json_data = request.get_json()
    seller_account_uuid = json_data.get('seller_account_uuid', '')

    seller_from_wallet_uuid = json_data.get('seller_from_wallet_uuid', '')


    data = {
        'uuid': uuid.uuid4(),
        'seller_account_uuid': seller_account_uuid,
        'seller_from_wallet_uuid': seller_from_wallet_uuid,
        'seller_to_wallet_uuid': '',
        'state': 'open',
        'locked': False,
        'rate': get_rate(ETH, RUB_QIWI),
        'rate_index': '',
        'seller_fee': '',
        'buyer_fee': ''
        }

    mongo.db.offers.insert(data)

    return jsonify({'code': 'OK',
                    'message': 'created'})


@a.route('/list_accounts', methods=['POST', 'GET'])
def list_accounts1():
    return json_encoder.encode(list_accounts())


@a.route('/auth', methods=['POST', 'GET'])
def auth_account():
    account_uuid = request.args.get('account_uuid')
    account = get_account(account_uuid)
    session['account_uuid'] = account_uuid
    return json_encoder.encode(account)


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

    json_data = request.get_json()
    qiwi_token = json_data.get('token', '')
    qiwi_address = json_data.get('qiwi_address', '')
    ethereum_address = json_data.get('ethereum_address', '')

    acc_uuid = create_account("account", qiwi_address, ethereum_address, qiwi_token)
    data_eth = []
    data_qiwi = []

    return jsonify({'uuid': acc_uuid,
                    'wallets': {ETH: data_eth,
                                RUB_QIWI: data_qiwi}})


@a.route('/get_rates', methods=['GET'], endpoint='get_rates')
def get_rates():
    eth_qw = get_rate(ETH, RUB_QIWI)
    return jsonify({'qw_eth': 1 / eth_qw,
            'eth_qw': eth_qw})


@a.route('/sample_accounts', methods=['GET'])
def sample_accounts():
    r = create_sample_accounts()
    return jsonify(r)



@a.route('/get_wallet', methods=['POST'])
def get_address():
    params = request.get_json()
    account_uuid = params.get('account')
    data = create_eth_wallet(account_uuid)
    # TODO: check account by uuid

    return jsonify({'address': data['address'], 'uuid': data['uuid']})


