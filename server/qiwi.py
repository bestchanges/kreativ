def get_qiwi_balance(token, phone):
    api_url = 'https://edge.qiwi.com/funding-sources/v2/persons/' + phone + '/accounts'

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + token}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for c in data['accounts']:
            if c['hasBalance']:
                return c['balance']['amount']
            else:
                print('no balance')
                return None
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None


