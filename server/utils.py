import requests
from flask_pymongo import MongoClient
from web3 import Web3, HTTPProvider
from app import mongo
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen

web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))

RUB_QIWI = 'RUB (QIWI)'
ETH = 'ETH'

#mongo = MongoClient()

def list_accounts():
    result = mongo.db.account.find()
    accounts = []
    for account in result:
        accounts.add(account)
    return accounts


# @a.route('/getbalanceqiwi', methods=['POST'], endpoint='get_balance')
def get_balance(qiwi_token, phone):
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
    else:
        # response['message']
        raise Exception("Error getting balance")


def create_wallet(account_uuid, currency, balance, privateKey, api_token, address):
    data = {
        'uuid': uuid.uuid4(),
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


our_rate = None

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
    our_rate = int(our_rate *100)
    return our_rate






def create_eth_wallet():
    a = web3.eth.account.create()  # type:LocalAccount
    data = {
        'private_key': web3.toHex(a.privateKey),
        'address': a.address
    }
    return data


def check_account_balance(address):
    # check account balance
    balance = web3.eth.getBalance(address)
    # balance = web3.eth.getBalance(a.address)
    print(balance)


def get_eth_balance(adress):
    return check_account_balance(adress)


def send_tr():
    # send transaction
    # http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendTransaction
    private_key = 0x0  # ................
    from_account = web3.eth.account.privateKeyToAccount(private_key)  # type:LocalAccount
    print(from_account.address)
    tx_data = dict(
        nonce=web3.eth.getTransactionCount(from_account.address),
        gasPrice=web3.eth.gasPrice,
        gas=21000,
        to="0xec3B133a9A3097f6513f27eaD93B849453eb7C74",
        value=12346,
        data=b'',
    )
    print(tx_data)
    tx = from_account.signTransaction(tx_data)
    # http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendRawTransaction
    tx_id = web3.eth.sendRawTransaction(tx['rawTransaction'])
    print(web3.toHex(tx_id))


# gas price
# http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.estimateGas

def create_account(name, qiwi_address, ethereum_address = None, qiwi_token = None, ethereum_private_key = None):
    acc_uuid = uuid.uuid4()

    data = {
        'ethereum_address': ethereum_address,
        'qiwi_address': qiwi_address,
        'uuid': acc_uuid,
        'name': name,
    }

    mongo.db.account.insert(data)

    balance = get_balance(qiwi_token, qiwi_address)
    if not isinstance(balance, float):
        return balance

    data_qiwi = create_wallet(acc_uuid, RUB_QIWI, balance, '', qiwi_token, qiwi_address)

    data_eth = create_eth_wallet()
    eth_close_address = data_eth['private_key']
    # ДОПИЛИТЬ - ПРЛУЧИТЬ БАЛАНС КРИПТЫ
    # balance = get_eth_balance(eth_close_address)
    data_eth = create_wallet(acc_uuid, ETH, balance, eth_close_address, '', ethereum_address)


    return acc_uuid


def create_sample_accounts():
    # bob sell ETH
    # alice buy ETH
    create_account(
        "ALICE",
        qiwi_address="",
        qiwi_token="cfa7547d48913cee745395c2a7f0de4d",
        ethereum_address="0x6afCFCEc1e595cd4D43e4c1D69e4590DC1944B29",
    )
    create_account("BOB", )

