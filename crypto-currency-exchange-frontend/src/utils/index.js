import { currencies } from '../settings'
import { find, values, propEq } from 'ramda'

export const formatMoney = (amount, currency, type) => {
  if (currency) {
    const { short, sign, name, decimals } = find(
      propEq('short', currency),
      values(currencies)
    )

    return `${sign}${(amount / Math.pow(10, decimals)).toFixed(decimals)}`
  }

  return (amount / 100).toString()

  return 'Error :)'
}

export const plusMinus = radius => (Math.random() * (radius * 2) | 0) - radius
