import uuid
from eth_account.local import LocalAccount
from flask import request, jsonify
from web3 import Web3, HTTPProvider
from app import app as a,mongo

# web3 = Web3(HTTPProvider(endpoint_uri="https://mainnet.infura.io/KbuOINU0Q1pTnO7j30hw"))
web3 = Web3(HTTPProvider(endpoint_uri="https://rinkeby.infura.io/KbuOINU0Q1pTnO7j30hw"))


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
    mongo.db.wallet.insert(data)
    return data


@a.route('/get_wallet', methods=['POST'])
def get_address():
    params = request.get_json()
    account_uuid = params.get('account')
    data = create_eth_wallet(account_uuid)
    # TODO: check account by uuid

    return jsonify({'address': data['address'], 'uuid': data['uuid']})


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
