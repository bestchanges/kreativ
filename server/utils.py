import requests
from web3 import Web3, HTTPProvider
from app import app as a,mongo
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen

from cache import Cache

web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))


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


def create_wallet(account_uuid, currency, balance, privateKey, api_token):
    data = {
        'uuid': uuid.uuid4(),
        'private_key': privateKey,
        'account_uuid': account_uuid,
        'currency': currency,
        'balance': balance,
        'api_token': api_token
    }
    mongo.db.wallet.insert(data)
    return data

cached_rates = Cache(max_size=100)

def get_median_rate(url):
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    mydivs = soup.findAll('div', {"class": "fs"})

    for i in [1, 2, 3, 4]:
        print(float(mydivs[i].text.replace(' ', '').replace('RUBQIWI', '')))

    print('\n')
    print('\n')
    print('\n')

    s = 0;

    for i in [2, 3]:
        s += float(mydivs[i].text.replace(' ', '').replace('RUBQIWI', ''))
    s /= 2
    return s

def get_rate(from_, to):
    pair_string = "{}/{}".format(from_, to)
    if cached_rates.get(pair_string):
        return cached_rates.get(pair_string)
    if from_ == 'ETH' and to == 'RUB (QIWI)':
        url1 = 'https://www.bestchange.ru/ethereum-to-qiwi.html'
        url2 = 'https://www.bestchange.ru/qiwi-to-ethereum.html'
    else:
        raise Exception("Unexpected pair {}/{}".format(from_, to))

    direct_rate = get_median_rate(url1)
    reverse_rate = get_median_rate(url2)
    our_rate = (direct_rate + reverse_rate) / 2
    our_rate = round(our_rate, 2)
    cached_rates[pair_string] = our_rate
    return our_rate



def create_eth_wallet(account_uuid):
    a = web3.eth.account.create() # type:LocalAccount
    # account private key
    # print(a.address)
    # account address
    # print(a.privateKey)
    data = {
        'uuid': uuid.uuid4(),
        'private_key': web3.toHex(a.privateKey),
        'address': a.address,
        'account_uuid': account_uuid
    }
    create_wallet()
    mongo.db.wallet.insert(data)
    return data


def check_account_balance():
    # check account balance
    #balance = web3.eth.getBalance("0x9Ba88a8BB6De98edB63a6066A7c7938Cdc4793E7")
    balance = web3.eth.getBalance(a.address)
    print(balance)


def send_tr():
    # send transaction
    # http://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.sendTransaction
    private_key = 0x0#................
    from_account = web3.eth.account.privateKeyToAccount(private_key) # type:LocalAccount
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
