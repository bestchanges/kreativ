import requests
from web3 import Web3, HTTPProvider
from app import mongo
import uuid
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))

RUB_QIWI = 'RUB (QIWI)'
ETH = 'ETH'

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


def create_transaction(buyer_account_uuid, offer_uuid, buyer_from_wallet_uuid, buyer_to_wallet_uuid, pay_amount):
    """
    # https://docs.google.com/document/d/1U878MJwM0I4pQkp-vo_dc4FUeQ5azZP1obEQhiPrmmE/edit#heading=h.roquar5ig1p0
    :param buyer_account_uuid:
    :param offer_uuid:
    :param buyer_from_wallet_uuid:
    :param buyer_to_wallet_uuid:
    :param pay_amount: сумма платежа в RUB
    :return:
    """

    # TODO: check if offer is open

    offer = mongo.db.offers.find_one({'uuid': offer_uuid})
    if not offer:
        raise Exception("not found offer {}".format(offer_uuid))
    if offer['state'] != 'open':
        raise Exception("Offer {} in not open state '{}'".format(offer_uuid, offer['state']))

    # TODO: check buyer_account owns buyer_*_wallet_uuid
    buyer_from_wallet = mongo.db.wallet.find_one({'uuid': buyer_from_wallet_uuid})
    if buyer_from_wallet['account_uuid'] != buyer_account_uuid:
        raise Exception(
            "Security breach! Wallet {} of buyer not belongs to {}".format(buyer_from_wallet, buyer_account_uuid))
    # TODO: check buyer_from_wallet.currency = offer.seller_to_wallet.currency
    # the same for second pair of wallets

    # check balance for seller_from_wallet (must have + service fee amount)

    # check balance for buyer_from_wallet
    buyer_from_wallet = update_qiwi_balance_for_wallet(buyer_from_wallet)
    if buyer_from_wallet['balance'] < pay_amount:
        raise Exception(
            "Not enought balance on wallet {}. required: {}, available: {}".format(buyer_from_wallet['uuid'],
                                                                                   buyer_from_wallet['balance'],
                                                                                   pay_amount))


    rate = offer['rate']
    pay_amount = round(pay_amount, 2)
    # calculate network fee web3.eth.estimateGas
    transaction_fee_amount = gas_price * TR_GAS_LIMIT
    ether_amount = pay_amount / rate
    ether_amount_wei = web3.toWei(ether_amount, 'ether')
    print("Selling {} ETH for rate {} = {}".format(ether_amount, pay_amount, rate))

    seller_to_wallet_amount = pay_amount
    buyer_from_wallet_amount = pay_amount
    seller_from_wallet_amount = ether_amount_wei
    buyer_to_wallet_amount = ether_amount_wei - transaction_fee_amount

    if buyer_to_wallet_amount < 0:
        raise Exception("Cannot do. After fees ({}) ETH amount {} is less 0 ({}) . ".format(transaction_fee_amount, seller_from_wallet_amount, buyer_to_wallet_amount))


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

        'seller_from_wallet_amount': seller_from_wallet_amount,
        'seller_to_wallet_amount': seller_to_wallet_amount,
        'buyer_to_wallet_amount': buyer_to_wallet_amount,
        'buyer_from_wallet_amount': buyer_from_wallet_amount,

        'transaction_fee_amount': transaction_fee_amount,

        'state': 'created',
        'rate': rate,
        'tx_id': None,
    }
    print(data)
    # lock offer
    offer['state'] = 'locked'
    mongo.db.offer.find_one_and_replace({'uuid': offer['uuid']}, offer)

    mongo.db.transaction.insert(data)
    transaction = mongo.db.transaction.find_one({'uuid': tr_uuid})
    return transaction


def execute_transaction(transaction_uuid):

    transaction = mongo.db.transaction.find_one({'uuid': transaction_uuid})
    if transaction['state'] not in ['created', 'executing']:
        return transaction

    # TODO: start transfer of RUB from buyer to seller
    buyer_qiwi_wallet = mongo.db.wallet.find_one({'uuid': transaction['buyer_from_wallet_uuid']})
    seller_qiwi_wallet = mongo.db.wallet.find_one({'uuid': transaction['seller_to_wallet_uuid']})
    try:
        qiwi_tx_id = send_money_qiwi(buyer_qiwi_wallet['api_token'], seller_qiwi_wallet['address'], transaction['buyer_from_wallet_amount'])
        transaction['qiwi_tx_id'] = qiwi_tx_id
    except Exception as e:
        print(str(e))
        pass
    transaction['state'] = 'partly_executed'
    mongo.db.transaction.find_one_and_replace({'uuid': transaction['uuid']}, transaction)

    buyer_to_wallet = mongo.db.wallet.find_one({'uuid': transaction['buyer_to_wallet_uuid']})
    seller_from_wallet = mongo.db.wallet.find_one({'uuid': transaction["seller_from_wallet_uuid"]})

    private_key = web3.toBytes(hexstr=seller_from_wallet['private_key'])
    amount_wei = transaction['buyer_to_wallet_amount']

    tx_id = _send_ethereum_transaction(only_estimate=False, private_key=private_key, to_address=buyer_to_wallet['address'], amount_wei=amount_wei)

    transaction['tx_id'] = tx_id
    transaction['state'] = 'finished'

    mongo.db.transaction.find_one_and_replace({'uuid': transaction['uuid'] }, transaction)

    # send service fee on the wallet - network fee

    # unlock offer
    offer = mongo.db.offers.find_one({'uuid': transaction['offer_uuid']})
    offer['state'] = 'open'
    mongo.db.offers.find_one_and_replace({'uuid': offer['uuid'] }, offer)

    return transaction

def get_account(account_uuid):
    account = mongo.db.account.find_one({'uuid': account_uuid})
    if not account:
        raise Exception("Not found account {}".format(account_uuid))
    del account["_id"]
    account['wallets'] = {ETH: [], RUB_QIWI: []}
    for wallet in mongo.db.wallet.find({'currency': ETH, 'account_uuid': account['uuid']}):
        del wallet['_id']
        wallet['private_key'] = ''
        wallet['api_token'] = ''
        account['wallets'][ETH].append(wallet)
    for wallet in mongo.db.wallet.find({'currency': RUB_QIWI, 'account_uuid': account['uuid']}):
        del wallet['_id']
        wallet['private_key'] = ''
        wallet['api_token'] = ''
        account['wallets'][RUB_QIWI].append(wallet)
    return account


def list_accounts():
    result = mongo.db.account.find()
    accounts = []
    for account in result:
        accounts.append(get_account(account['uuid']))
    return accounts


def update_balance_for_wallet(wallet):
    if wallet['currency'] == ETH:
        return update_eth_balance_for_wallet(wallet)
    elif wallet['currency'] == RUB_QIWI:
        return update_qiwi_balance_for_wallet(wallet)
    raise Exception("shall not be here")


def update_qiwi_balance_for_wallet(wallet):
    if wallet['currency'] != RUB_QIWI:
        raise Exception("Not QIWI")
    balance = get_qiwi_balance(wallet['api_token'], wallet['address'])
    wallet['balance'] = balance
    mongo.db.wallet.find_one_and_replace({'uuid': wallet['uuid']}, wallet)
    return wallet


def get_qiwi_balance(qiwi_token, phone):
    # json_data = request.get_json()
    # qiwi_token = json_data.get('token', '')
    # phone = json_data.get('phone', '')
    api_url = 'https://edge.qiwi.com/funding-sources/v2/persons/' + phone + '/accounts'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + qiwi_token}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for c in data['accounts']:
            return c['balance']['amount']
    print(response.json())
    raise Exception("Error getting balance")


def create_wallet(account_uuid, currency, balance, privateKey, api_token, address):
    data = {
        'uuid': str(uuid.uuid4()),
        'private_key': privateKey,
        'account_uuid': account_uuid,
        'currency': currency,
        'balance': balance,
        'api_token': api_token,
        'address': address
    }
    mongo.db.wallet.insert(data)
    return data


def get_median_rate(url, currency):
    tail = 'RUBQIWI'
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    if currency == 'ETH':
        mydivs_tmp = soup.findAll('td', {"class": 'bi'})
        mydivs = []
        i = 0
        for div in mydivs_tmp:
            div_str = str(div)
            if 'RUB QIWI' in div_str:
                mydivs.append(div_str[15:26])
                i += 1
                if i > 3:
                    break

    else:
        mydivs_tmp = soup.findAll('div', {"class": 'fs'})
        mydivs = []
        i = 0
        for div in mydivs_tmp:
            mydivs.append(str(div.text))

    for i in [0, 1, 2, 3]:
        print(float(mydivs[i].replace(' ', '').replace(tail, '')))


    s = 0;

    for i in [1, 2]:
        s += float(mydivs[i].replace(' ', '').replace(tail, ''))
    s /= 2
    print(s, '\n')
    return s


our_rate = 42000

def get_rate(from_, to):

    global our_rate
    if our_rate is not None:
        return our_rate

    if from_ == ETH and to == RUB_QIWI:
        url1 = 'https://www.bestchange.ru/ethereum-to-qiwi.html'
        url2 = 'https://www.bestchange.ru/qiwi-to-ethereum.html'
    else:
        raise Exception("Unexpected pair {}/{}".format(from_, to))

    direct_rate = get_median_rate(url1, from_)
    reverse_rate = get_median_rate(url2, to)
    our_rate = (direct_rate + reverse_rate) / 2
    return our_rate






def create_eth_wallet():
    a = web3.eth.account.create()  # type:LocalAccount
    data = {
        'private_key': web3.toHex(a.privateKey),
        'address': a.address
    }
    return data


def update_eth_balance_for_wallet(wallet):
    if wallet['currency'] != ETH:
        raise Exception("Not ETH")
    balance = get_eth_balance(wallet['address'])
    wallet['balance'] = balance
    mongo.db.wallet.find_one_and_replace({'uuid': wallet['uuid']}, wallet)
    return wallet


def get_eth_balance(address):
    # check account balance
    balance = web3.eth.getBalance(address)
    # balance = web3.eth.getBalance(a.address)
    balance = balance / 10**18
    return balance



# gas price
# http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.estimateGas

def create_account(name, qiwi_address, ethereum_address = None, qiwi_token = None, ethereum_private_key = None):
    acc_uuid = str(uuid.uuid4())

    data = {
        'ethereum_address': ethereum_address,
        'qiwi_address': qiwi_address,
        'uuid': acc_uuid,
        'name': name,
    }

    mongo.db.account.insert(data)

    # TODO: do not request balance here. Do it somethere later by separate request wallet_balance
    if qiwi_token:
        balance = get_qiwi_balance(qiwi_token, qiwi_address)
    else:
        balance = 0

    data_qiwi = create_wallet(acc_uuid, RUB_QIWI, balance, '', qiwi_token, qiwi_address)

    if not ethereum_address:
        data_eth = create_eth_wallet()
        ethereum_private_key = data_eth['private_key']
        ethereum_address = data_eth['address']
        balance = 0 # for sure. We just created it
    else:
        balance = get_eth_balance(ethereum_address)
    # ДОПИЛИТЬ - ПРЛУЧИТЬ БАЛАНС КРИПТЫ
    # balance = get_eth_balance(eth_close_address)
    data_eth = create_wallet(acc_uuid, ETH, balance, ethereum_private_key, '', ethereum_address)
    return acc_uuid


def create_sample_accounts():
    # bob sell ETH
    # alice buy ETH
    create_account(
        "ALICE",
        qiwi_address="79636853224",
        qiwi_token="7820a390d136f825461739c26ae7324b",
        ethereum_address="0x6afCFCEc1e595cd4D43e4c1D69e4590DC1944B29",
    )
    create_account(
        "BOB",
        qiwi_address="79118341146",
        qiwi_token="",
    )


def send_money_qiwi(token, phone, amount):
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

    if response.status_code != 200:
        raise Exception("Not send")



