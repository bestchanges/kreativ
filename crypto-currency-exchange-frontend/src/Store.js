import { decorate, observable, transaction } from 'mobx'

const tryJSON = (str) => {
  try {
    return JSON.parse(str)
  } catch(error) {
    return null
  }
}

class StoreClass {
  walletUUID = tryJSON(localStorage.getItem('walletUUID'))
  account = tryJSON(localStorage.getItem('account'))
  wallets = null
  offer = tryJSON(localStorage.getItem('offer'))
  transaction_uuid = tryJSON(localStorage.getItem('transaction_uuid'))

  setWalletUUID = (walletUUID) => {
    this.walletUUID = walletUUID
    localStorage.setItem('walletUUID', JSON.stringify(walletUUID))
  }

  setCurrentOffer = (offer) => {
    this.offer = offer
    localStorage.setItem('offer', JSON.stringify(offer))
  }

  clearOffer = () => {
    this.offer = null
  }

  setTransactionUUID  = (uuid) => {
    this.transaction_uuid = uuid
    localStorage.setItem('transaction_uuid', JSON.stringify(uuid))
  }

  setAccount = (account) => {
    this.account = account
    localStorage.setItem('account', JSON.stringify(account))
  }

  clearAccount = () => {
    this.account = null
    this.wallets = null
  }
}

export const Store = decorate(StoreClass, {
  walletUUID: observable,
  account: observable,
  wallets: observable,
  offer: observable,
  transaction_uuid: observable,
})
