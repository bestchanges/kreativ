import React, { Component } from 'react'
import styled from 'styled-components'

import { fetchRates } from '../../utils/api'
import { formatMoney } from '../../utils'
import { Head, Center, ButtonGreen } from '../../components'
import ethLogo from '../../attach/eth_logo.svg'


const Pair = styled.div`
  display: flex;
  flex-direction: row;
  margin-top: 66px;
  font-family: Helvetica;
`

const Card = styled.div`
  width: 380px;
  height: 300px;
  background: #fff;
  transition: .2s background ease;
  &:hover {
    background: #f6f6f6;
  }
  position: relative;
  cursor: pointer;
`

const CustomButton = ButtonGreen.extend`
  width: 120px;
  position: absolute;
  right: 0;
  bottom: 32px;
  z-index: 1;
`

const Info = styled.div`
  padding: 37px 0 0 60px;
`

const Title = styled.div`
  font-size: 36px;
  font-weight: 500;
  color: #2a2a2a;
`

const Amount = styled.div`
  font-size: 24px;
  font-weight: 500;
  color: #2a2a2a;
  margin-top: 35px;
  &:after {
    content: 'for 1 ETH';
    font-size: 12px;
    color: #838383;
    font-weight: 300;
    padding-left: 8px;
  }
`

const Available = styled.div`
  font-size: 24px;
  font-weight: 500;
  color: #2a2a2a;
  margin-top: 35px;
  &:before {
    content: 'Available amount';
    display: block;
    font-size: 12px;
    font-weight: 300;
    color: #838383;
  }
`

const Rubl = styled.div`
  font-family: Helvetica;
  font-size: 64px;
  font-weight: 300;
  color: #2a2a2a;
  position: absolute;
  right: 24px;
  top: 2px;
`

const EthLogo = styled.div`
  height: 72px;
  width: 32px;
  position: absolute;
  right: 24px;
  top: 18px;
`

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
    fetchRates().then(({ eth_qw, sum_all_offers } = {}) => {
      this.setState({
        rateSell: eth_qw,
        rateBuy: eth_qw,
        sum_all_offers,
      })
    })
  }

  toCreateOffer = () => {
    const { history } = this.props
    history.push('/create_offer')
  }

  toListOffer = () => {
    const { history } = this.props
    history.push('/offer_list')
  }

  render() {
    const { rateSell, rateBuy, sum_all_offers } = this.state

    return (
      <Center>
        <Head>CreativeBase</Head>
        <Pair>
          <Card onClick={this.toCreateOffer}>
            <Info>
              <Title>Sell Ether</Title>
              {rateSell && <Amount>{formatMoney(rateSell, 'RUB')}</Amount>}
            </Info>
            <CustomButton>Sell</CustomButton>
            <Rubl>₽</Rubl>
          </Card>
          <Card onClick={this.toListOffer}>
            <Info>
              <Title>Buy Ether</Title>
              {rateBuy && <Amount>{formatMoney(rateBuy, 'RUB')}</Amount>}
              <Available>{Number(sum_all_offers).toFixed(6)} ETH</Available>
            </Info>
            <CustomButton>Buy</CustomButton>
            <EthLogo>
              <img src={ethLogo} alt='eth logo' width='100%' height='100%' />
            </EthLogo>
          </Card>
        </Pair>
      </Center>
    )
  }
}

export {
  SellerBuyer
}
