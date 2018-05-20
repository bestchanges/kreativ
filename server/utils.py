import requests
from web3 import Web3, HTTPProvider
from app import mongo
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen

web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))

RUB_QIWI = 'RUB (QIWI)'
ETH = 'ETH'

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


our_rate = 4200045

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
    return int(our_rate * 100)






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

