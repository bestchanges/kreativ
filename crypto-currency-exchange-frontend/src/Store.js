import { decorate, observable, transaction } from 'mobx'

class StoreClass {
  walletUUID = null
  account = null
  wallets = null
  offer = null
  transaction_uuid = null

  setWalletUUID = (walletUUID) => {
    this.walletUUID = walletUUID
  }

  setCurrentOffer = (offer) => {
    this.offer = offer
  }

  clearOffer = () => {
    this.offer = null
  }

  setTransactionUUID  = (uuid) => {
    this.transaction_uuid = uuid
  }

  setAccount = (account) => {
    this.account = account
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
