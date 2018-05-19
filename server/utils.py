from web3 import Web3, HTTPProvider
from app import app as a,mongo
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen

web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))


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



def get_rate(url):
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
    s = round(s, 4)
    return s
