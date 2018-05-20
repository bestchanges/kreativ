import React from 'react'
import { Input, Form } from 'antd'
import styled from 'styled-components'

import { localize } from '../../settings'
import { formatMoney } from '../../utils'

const SubTitle = styled.div`
  color: #444;
  font-size: 1rem;
`

const Amount = styled.div`
  color: #333;
  font-size: 3rem;
`

const CurrencyInfo = ({ exchangeRate, totalAmount, sell, totalAmountCurrency, right }) =>
  <Form style={{ textAlign: right ? 'right' : 'left' }}>
    <Form.Item>
      <SubTitle>{sell ? localize.SellerBuyer.sellRate : localize.SellerBuyer.buyRate}</SubTitle>
      {exchangeRate && <Amount>{formatMoney(exchangeRate, 'RUB')}</Amount>}
    </Form.Item>
    <Form.Item>
      <SubTitle>{localize.SellerBuyer.totalAmount}</SubTitle>
      {exchangeRate && <Amount>{formatMoney(totalAmount, totalAmountCurrency)}</Amount>}
    </Form.Item>
  </Form>

export {
  CurrencyInfo
}
