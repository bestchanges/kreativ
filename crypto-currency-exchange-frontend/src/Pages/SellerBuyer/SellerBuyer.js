import React, { Component } from 'react'
import { evolve, add } from 'ramda'
import { Input, Button, Col, Row, Form } from 'antd'

import { localize } from '../../settings'
import { plusMinus, formatMoney } from '../../utils'

import { CurrencyInfo } from './CurrencyInfo'
import { TestEndpoint } from './TestEndpoint'

const fetchTimeout = 3000

class SellerBuyer extends Component {
  static defaultProps = {
    exchangeRate: 4114613,
    totalAmount: 7575391,
  }

  state = {
    exchangeRate: this.props.exchangeRate,
    totalAmount: this.props.totalAmount,
  }

  componentDidMount() {
    this.fetch = setInterval(() => {
      this.setState(evolve({
        exchangeRate: add(plusMinus(100)),
        totalAmount: add(plusMinus(400)),
      }))
    }, fetchTimeout)
  }

  componentWillUnmount() {
    clearInterval(this.fetch)
  }

  render() {
    const { exchangeRate, totalAmount } = this.state

    return (
      <div>
        <Row style={{ paddingTop: '2rem' }}>
          <Col span={9} offset={2}>
            <CurrencyInfo
              exchangeRate={exchangeRate}
              totalAmount={totalAmount}
            />
          </Col>
          <Col span={9} offset={2}>
            <CurrencyInfo
              exchangeRate={exchangeRate}
              totalAmount={totalAmount}
            />
          </Col>
        </Row>

        <Row style={{ marginTop: '4rem' }}>
          <Col span={20} offset={2}>
            <TestEndpoint />
          </Col>
        </Row>
      </div>
    )
  }
}

export {
  SellerBuyer
}
