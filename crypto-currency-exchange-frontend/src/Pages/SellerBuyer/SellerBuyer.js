import React, { Component } from 'react'
import styled from 'styled-components'
import { Button, Col, Row, Layout } from 'antd'
import { Link } from 'react-router-dom'

import { localize } from '../../settings'
import { fetchRates } from '../../utils/api'

import { Title } from '../../components'

import { CurrencyInfo } from './CurrencyInfo'


const fetchTimeout = 30000

class SellerBuyer extends Component {
  static defaultProps = {
    exchangeRate: 4114613,
    totalAmount: 7575391,
  }

  state = {
    totalETH: 0,
    totalRUB: 0,
  }

  componentDidMount() {
    this.fetchRate()
    this.fetch = setInterval(() => {
      this.fetchRate()
    }, fetchTimeout)
  }

  componentWillUnmount() {
    clearInterval(this.fetch)
  }

  fetchRate = () => {
    fetchRates().then(({ eth_qw } = {}) => {
      this.setState({
        rateSell: eth_qw,
        rateBuy: eth_qw,
      })
    })
  }

  render() {
    const { rateSell, rateBuy, totalETH, totalRUB } = this.state

    return (
      <Row style={{ padding: '2rem 0' }}>
        <Col span={10} offset={2} style={{ paddingRight: '1rem' }}>
          <Layout.Content style={{ textAlign: 'right' }}>
            <Title>{localize.SellerBuyer.sellTitle}</Title>
            <CurrencyInfo
              exchangeRate={rateSell}
              totalAmount={totalRUB}
              sell
              right
              totalAmountCurrency='RUB'
            />
            <Link to={'/create_offer'}>
              <Button size='large' type='primary'>{localize.SellerBuyer.sell}</Button>
            </Link>
          </Layout.Content>
        </Col>
        <Col span={10} offset={0} style={{ paddingLeft: '1rem' }}>
          <Layout.Content>
            <Title>{localize.SellerBuyer.buyTitle}</Title>
            <CurrencyInfo
              exchangeRate={rateBuy}
              totalAmount={totalETH}
              totalAmountCurrency='ETH'
            />
            <Button size='large' type='primary'>{localize.SellerBuyer.buy}</Button>
          </Layout.Content>
        </Col>
      </Row>
    )
  }
}

export {
  SellerBuyer
}
