import { decorate, observable } from 'mobx'

class StoreClass {
  walletUUID = null
  account = null
  wallets = null

  setWalletUUID = (walletUUID) => {
    this.walletUUID = walletUUID
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
})
