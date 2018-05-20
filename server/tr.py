# transaction endpoint
from _decimal import Decimal

from pymongo import MongoClient

# TODO: when insert use http://api.mongodb.com/python/current/tutorial.html#inserting-a-document
from utils import *

TR_GAS_LIMIT = 21000
# set once gas price. In future make it updateable
gas_price = web3.eth.gasPrice

def _send_ethereum_transaction(private_key, to_address, amount_wei, only_estimate=False, ):
    '''
    low level method sending eth
    :param private_key:
    :param to_address:
    :param amount_wei:
    :param only_estimate:
    :return:
    '''
    # http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendTransaction
    global gas_price
    from_account = web3.eth.account.privateKeyToAccount(private_key)  # type:LocalAccount
    print(from_account.address)
    tx_data = dict(
        nonce=web3.eth.getTransactionCount(from_account.address),
        gasPrice=gas_price,
        gas=TR_GAS_LIMIT,
        to=to_address,
        value=amount_wei,
        data=b'',
    )
    print(tx_data)
    tx = from_account.signTransaction(tx_data)
    # http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendRawTransaction
    if not only_estimate:
        tx_id = web3.eth.sendRawTransaction(tx['rawTransaction'])
        return web3.toHex(tx_id)


def send_eth(offer, buyer_eth_wallet, amount):
    # offer = mongo.app.offers.find_one({'uuid': "b3369554-3c57-4023-9171-40e903d98a12"})
    # buyer = mongo.app.account.find_one({'name': 'ALICE'})
    pass

def start_transaction(buyer_account_uuid, offer_uuid, buyer_from_wallet_uuid, buyer_to_wallet_uuid, amount):
    """
    # https://docs.google.com/document/d/1U878MJwM0I4pQkp-vo_dc4FUeQ5azZP1obEQhiPrmmE/edit#heading=h.roquar5ig1p0
    :param buyer_account_uuid:
    :param offer_uuid:
    :param buyer_from_wallet_uuid:
    :param buyer_to_wallet_uuid:
    :param amount: сумма платежа в публях
    :return:
    """

    offer = mongo.db.offer.find_one({'uuid': offer_uuid})
    if not offer:
        raise Exception("not found offer {}".format(offer_uuid))
    if offer['state'] != 'open':
        raise Exception("Offer {} in not open state '{}'".format(offer_uuid, offer['state']))


    # TODO: check buyer_account owns buyer_*_wallet_uuid
    buyer_from_wallet = mongo.db.wallet.find_one({'uuid': buyer_from_wallet_uuid})
    if buyer_from_wallet['account_uuid'] != buyer_account_uuid:
        raise Exception("Security breach! Wallet {} of buyer not belongs to {}".format(buyer_from_wallet, buyer_account_uuid))
    # TODO: check buyer_from_wallet.currency = offer.seller_to_wallet.currency
    # the same for second pair of wallets

    # check balance for seller_from_wallet (must have + fee amount)
    # calculate network fee web3.eth.estimateGas

    # check balance for buyer_from_wallet
    buyer_from_wallet_balance = update_qiwi_balance_for_wallet(buyer_from_wallet)
    if buyer_from_wallet_balance < recieved_amount:
        raise Exception("Not enought balance on wallet {}. required: {}, available: {}".format(buyer_from_wallet['uuid'], buyer_from_wallet_balance, recieved_amount))

    # lock offer
    offer['state'] = 'locked'
    mongo.db.offer.find_one_and_replace({'uuid': offer['uuid'] }, offer)

    rate = offer['rate']
    sent_amount = recieved_amount / rate
    # create transaction
    tr_uuid = str(uuid.uuid4())
    data = {
        'uuid': tr_uuid,
        'offer_uuid': offer_uuid,
        'seller_account_uuid': offer['seller_account_uuid'],
        'buyer_account_uuid': buyer_account_uuid,
        'seller_from_wallet_uuid': offer['seller_from_wallet_uuid'],
        'seller_to_wallet_uuid': offer['seller_to_wallet_uuid'],
        'buyer_to_wallet_uuid': buyer_to_wallet_uuid,
        'buyer_from_wallet_uuid': buyer_from_wallet_uuid,
        'sent_amount': sent_amount,
        'recieved_amount': recieved_amount,
        'rate': rate,
        'tx_id': None,
    }
    mongo.db.transaction.insert(data)
    transaction = mongo.db.transaction.find_one({'uuid': tr_uuid})

    # start transfer of RUB from buyer to seller
    # send ETH part reduced by service fee and - network fee
    buyer_to_wallet = mongo.app.wallet.find_one({'account_uuid': buyer_to_wallet_uuid})
    assert buyer_to_wallet['currency'] == ETH
    seller_from_wallet = mongo.app.wallet.find_one({'uuid': offer["seller_from_wallet_uuid"]})
    assert seller_from_wallet['currency'] == ETH
    assert buyer_to_wallet['address'] != seller_from_wallet['address']

    private_key = web3.toBytes(hexstr=seller_from_wallet['private_key'])
    amount_wei = web3.toWei(sent_amount, 'ether')

    transaction_fee_wei = gas_price * TR_GAS_LIMIT
    amount_wei -= transaction_fee_wei

    tx_id = _send_ethereum_transaction(only_estimate=False, private_key=private_key, to_address=buyer_to_wallet['address'], amount_wei=amount_wei)

    # send service fee on the wallet - network fee

    # unlock offer
    offer['state'] = 'open'
    mongo.db.offer.find_one_and_replace({'uuid': offer['uuid'] }, offer)

