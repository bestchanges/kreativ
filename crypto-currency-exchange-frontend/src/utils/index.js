import { currencies } from '../settings'
import { find, values, propEq } from 'ramda'

export const formatMoney = (amount, currency, type) => {
  if (currency) {
    const { sign, decimals } = find(
      propEq('short', currency),
      values(currencies)
    )

    return `${amount}${sign}`
  }

  return (amount).toString()
}

export const plusMinus = radius => (Math.random() * (radius * 2) | 0) - radius
