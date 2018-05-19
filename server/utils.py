import requests
from web3 import Web3, HTTPProvider
from app import app as a, mongo
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen

web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))


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
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return response.json()


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


def get_rate(from_, to):
    pair_string = "{}/{}".format(from_, to)
    if from_ == 'ETH' and to == 'RUB (QIWI)':
        url1 = 'https://www.bestchange.ru/ethereum-to-qiwi.html'
        url2 = 'https://www.bestchange.ru/qiwi-to-ethereum.html'
    else:
        raise Exception("Unexpected pair {}/{}".format(from_, to))

    direct_rate = get_median_rate(url1, from_)
    reverse_rate = get_median_rate(url2, to)
    our_rate = (direct_rate + reverse_rate) / 2
    our_rate = round(our_rate, 2)
    print(our_rate)
    return our_rate


def create_eth_wallet():
    a = web3.eth.account.create()  # type:LocalAccount
    data = {
        'private_key': web3.toHex(a.privateKey),
        'address': a.address
    }
    return data


def check_account_balance():
    # check account balance
    # balance = web3.eth.getBalance("0x9Ba88a8BB6De98edB63a6066A7c7938Cdc4793E7")
    balance = web3.eth.getBalance(a.address)
    print(balance)


def get_eth_balance(adress):
    # check account balance
    # balance = web3.eth.getBalance("0x9Ba88a8BB6De98edB63a6066A7c7938Cdc4793E7")
    balance = web3.eth.getBalance(a.address)
    return balance


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


def create_account(qiwi_address, ethereum_address):
    acc_uuid = uuid.uuid4()

    data = {
        'ethereum_address': ethereum_address,
        'qiwi_address': qiwi_address,
        'uuid': acc_uuid
    }

    mongo.db.account.insert(data)

    return acc_uuid
