import json
import time
from decimal import Decimal
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
    return str(o)


json_encoder = json.JSONEncoder(indent=4, default=default_encode)

@a.route('/list_offers', methods=['GET'], endpoint='get_offer_list')
def list_offers():
    offers = []
    for result in mongo.db.offers.find({'state': 'open'}):
        wallet = mongo.db.wallet.find_one({'uuid': result['seller_from_wallet_uuid']})
        if not wallet:
            raise Exception("Not found wallet")
        wallet=update_balance_for_wallet(wallet)
        offers.append({'offer': result, 'wallet': wallet})
    return json_encoder.encode(offers)


@a.route('/create_offer', methods=['POST'], endpoint='create_offer')
def create_offer():
    json_data = request.get_json()
    seller_account_uuid = json_data.get('seller_account_uuid', '')
    if seller_account_uuid == '':
        raise Exception("Not found seller_account_uuid")
    seller_from_wallet_uuid = json_data.get('seller_from_wallet_uuid', '')
    if seller_from_wallet_uuid == '':
        raise Exception("Not found seller_from_wallet_uuid")
    seller_to_wallet_uuid = json_data.get('seller_to_wallet_uuid', '')
    if seller_to_wallet_uuid == '':
        raise Exception("Not found seller_to_wallet_uuid")

    offer_uuid = str(uuid.uuid4())
    data = {
        'uuid': offer_uuid,
        'seller_account_uuid': seller_account_uuid,
        'seller_from_wallet_uuid': seller_from_wallet_uuid,
        'seller_to_wallet_uuid': seller_to_wallet_uuid,
        'state': 'open',
        'rate': get_rate(ETH, RUB_QIWI),
        'rate_index': 1,
        'seller_fee': 0,
        'buyer_fee': 0
        }

    mongo.db.offers.insert(data)
    offer = mongo.db.offers.find_one({'uuid': offer_uuid})
    return json_encoder.encode(offer)


@a.route('/list_accounts', methods=['POST', 'GET'])
def list_accounts1():
    return json_encoder.encode(list_accounts())


@a.route('/auth', methods=['POST', 'GET'])
def auth_account():
    account_uuid = request.args.get('account_uuid')
    account = get_account(account_uuid)
    session['account_uuid'] = account_uuid
    return json_encoder.encode(account)


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


@a.route('/wallet_balance', methods=['GET'])
def wallet_balance():
    wallet_uuid = request.args.get('wallet_uuid')
    wallet = mongo.db.wallet.find_one({'uuid': wallet_uuid})
    wallet = update_balance_for_wallet(wallet)
    return jsonify(wallet['balance'])


@a.route('/create_transaction', methods=['GET', 'POST'])
def create_transaction1():
    try:
        json_data = request.get_json()

        if json_data:
            data = json_data
        else:
            data = request.args
        offer_uuid = data.get('offer_uuid')
        buyer_account_uuid = data.get('account_uuid')
        buyer_from_wallet_uuid = data.get('from_wallet_uuid')
        buyer_to_wallet_uuid = data.get('to_wallet_uuid')
        amount = float(data.get('amount'))

        transaction = create_transaction(buyer_account_uuid, offer_uuid, buyer_from_wallet_uuid, buyer_to_wallet_uuid, amount)
        return json_encoder.encode(transaction)
    except Exception as e:
        return json_encoder.encode({'error': True, 'message': str(e)})

@a.route('/execute_transaction', methods=['GET', 'POST'])
def execute_transaction1():
    try:
        json_data = request.get_json()
        if json_data:
            data = json_data
        else:
            data = request.args
        transaction_uuid = data.get('transaction_uuid')

        return json_encoder.encode(execute_transaction(transaction_uuid))
    except Exception as e:
        raise e
        return json_encoder.encode({'error': True, 'message': str(e)})
