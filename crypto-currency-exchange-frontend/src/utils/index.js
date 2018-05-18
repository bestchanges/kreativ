import { currencies } from '../settings'

export const formatMoney = (amount, currency, type) => {
  if (!type) {
    return (amount / 100).toString()
  }

  return 'Error :)'
}

export const plusMinus = radius => (Math.random() * (radius * 2) | 0) - radius