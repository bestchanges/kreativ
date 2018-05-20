const server = window.endpointOrigin

const getJSON = res => res.json()

async function request(url, options) {
  const result = await fetch(`${server}${url}`, options)
    .then(getJSON)
    .catch(console.error)

  return result
}

function get(url, options) {
  return request(url, {
    method: 'GET',
    ...options,
  })
}

function post(url, options) {
  return request(url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
    },
    ...options,
  })
}

export const fetchRates = (options) =>
  get('/get_rates', options)

export const createQiwiAccount = (options) =>
  post('/createaccountqiwi', options)

export const getWallet = (options) =>
  get('/get_wallet', options)

export const getAccounts = (options) =>
  get('/list_accounts', options)

export const getAuth = (uuid) =>
  get(`/auth?account_uuid=${uuid}`)

export const createOffer = (options) =>
  post('/create_offer', options)

//   POST /getbalanceqiwi
// {
//   'token': token,
//   'phone': phone}

// {
//   'code': 'QWPRC-220', 
//   'message': 'Недостаточно средств '}