import React from 'react'
import { Input, Button, Col, Form } from 'antd'

import { localize } from '../../settings'
import { formatMoney } from '../../utils'

const CurrencyInfo = ({ exchangeRate, totalAmount }) =>
  <Form>
    <Form.Item>
      <Input
        addonBefore={localize.SellerBuyer.exchangeRate}
        value={formatMoney(exchangeRate)}
        onChange={() => null}
      />
    </Form.Item>
    <Form.Item>
      <Input
        addonBefore={localize.SellerBuyer.totalAmount}
        value={formatMoney(totalAmount)}
        onChange={() => null}
      />
    </Form.Item>
    <Button>{localize.SellerBuyer.exchangeButton}</Button>
  </Form>

export {
  CurrencyInfo
}
