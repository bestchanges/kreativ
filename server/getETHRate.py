from bs4 import BeautifulSoup
from urllib.request import urlopen

from flask import jsonify

from app import app as a


@a.route('/get_rates', methods=['GET'], endpoint='get_rates')
def get_rates():
    qw_eth = get_rate('https://www.bestchange.ru/qiwi-to-ethereum.html')
    eth_qw = get_rate('https://www.bestchange.ru/ethereum-to-qiwi.html')
    return jsonify({'qw_eth': qw_eth,
                    'eth_qw': eth_qw})



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
