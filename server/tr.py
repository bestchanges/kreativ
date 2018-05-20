# transaction endpoint
from app import mongo

# TODO: when insert use http://api.mongodb.com/python/current/tutorial.html#inserting-a-document
from utils import *
from flask import request, jsonify
from app import app as a


def create_offer():
    json_data = request.get_json()
    seller_from_wallet_uuid = json_data.get('from_wallet_uuid')
    seller_to_wallet_uuid = json_data.get('to_wallet_uuid')
    rate_percent = json_data.get('rate_percent')
    rate_mul = 1 + rate_percent / 100
    data = {
        'seller_account_uuid': '',
        'seller_from_wallet_uuid': '',
        'seller_to_wallet_uuid': '',
        'state': '',
        'currency_from': '',
        'currency_to': '',
        'rate': 44000,
        'rate_index': rate_mul,
        'seller_fee': 0.003,
        'buyer_fee': 0.007,
    }

def start_transaction(buyer_account_uuid, offer_uuid, buyer_from_wallet_uuid, buyer_to_wallet_uuid, payed_amount):
    """
    # https://docs.google.com/document/d/1U878MJwM0I4pQkp-vo_dc4FUeQ5azZP1obEQhiPrmmE/edit#heading=h.roquar5ig1p0
    :param buyer_account_uuid:
    :param offer_uuid:
    :param buyer_from_wallet_uuid:
    :param buyer_to_wallet_uuid:
    :param amount: сумма
    :return:
    """

    offer = mongo.db.offer.find_one({'uuid': offer_uuid})
    if not offer:
        raise Exception("not found offer {}".format(offer_uuid))
    # TODO: check buyer_account owns buyer_*_wallet_uuid

    # TODO: check buyer_from_wallet.currency = offer.seller_to_wallet.currency
    # the same for second pair of wallets

    # check balance for seller_from_wallet (must have + fee amount)
    # check balance for buyer_from_wallet

    # lock offer
    mongo.db.offer.update_one({'uuid': offer['uuid'] }, { '$set': {'state' 'locked'}})

    rate = offer['rate']
    sold_amount = payed_amount / rate
    # create transaction
    data = {
        'offer_uuid': offer_uuid,
        'seller_account_uuid': offer['seller_account_uuid'],
        'buyer_account_uuid': buyer_account_uuid,
        'seller_from_wallet_uuid': offer['seller_from_wallet_uuid'],
        'seller_to_wallet_uuid': offer['seller_to_wallet_uuid'],
        'buyer_to_wallet_uuid': buyer_to_wallet_uuid,
        'buyer_from_wallet_uuid': buyer_from_wallet_uuid,
        'sell_currency': '',
        'buy_currency': '',
        'sold_amount': sold_amount,
        'payed_amount': payed_amount,
        'rate': '',
    }
    # find start transfer of RUB part (by currency)
    # send ETH part reduced by service fee and - network fee
    # send service fee on the wallet - network fee