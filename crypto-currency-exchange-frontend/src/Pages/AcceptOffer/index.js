import React from 'react'
import styled from 'styled-components'
import { path } from 'ramda'
import { Icon } from 'antd'
import { getWalletBalance, createTransaction } from '../../utils/api'
import { Offer } from '../OfferList/Offer'
import { Center, ButtonGreen } from '../../components'

import transferSrc from './transfer.svg'

const QiwiHelp = styled.div`
  display: flex;
  width: 470px;
  height: 165px;
  background-color: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  margin-top: 2px;
`

const QiwiAmount = styled.div`
  display: flex;
  flex-direction: column;
  width: 290px;
  height: 100px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  background-color: #fff;
  padding: 12px;
  position: relative;
`

const HelpField = styled.div`
  width: 178px;
  height: 100px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  margin-left: 2px;
`

const Row = styled.div`
  display: flex;
  margin-top: 2px;
  flex-direction: row;
`

const Exchange = styled.div`
  width: 470px;
  height: 94px;
  background-color: #fff;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
  margin-top: 2px;
  position: relative;
`

const ButtonsField = styled.div`
	width: 470px;
  height: 60px;
  margin-top: 2px;
	background-color: #ffffff;
	box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
`

const BackButton = ButtonGreen.extend`
  margin-top: 4px;
  width: 100px;
`

const BuyButton = ButtonGreen.extend`
  width: 140px;
  position: absolute;
  right: 0;
  left: 0;
  margin: auto;
  margin-top: 4px;
`

const Input = styled.input`
  border: none;
  outline: none;
  font-family: Helvetica;
  width: 190px;
	font-size: 30px;
	font-weight: 500;
  color: #2a2a2a;
  position: absolute;
  left: 50px;
  top: 2px;
`

const InputRight = styled.input`
  border: none;
  outline: none;
  font-family: Helvetica;
  width: 250px;
  font-size: 18px;
  font-weight: 500;
  color: #2a2a2a;
  position: absolute;
  top: 50px;
  left: 55px;
`

const EthC = styled.div`
  position: absolute;
  font-size: 16px;
  left: 13px;
  top: 52px;
`

const RubC = styled.div`
  position: absolute;
  font-size: 16px;
  left: 13px;
  top: 16px;
`

const QiwiTitle = styled.div`
  font-family: Helvetica;
  font-size: 30px;
  font-weight: 500;
  color: #2a2a2a;
  margin-bottom: -8px;
`

const TransferIcon = styled.img`
  width: 30px;
  height: 30px;
  position: absolute;
  left: 400px;
  top: 35px;
`

const Refresh = styled.div`
  position: absolute;
  height: 100px;
  right: 0;
  top: 0;
  width: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f6f6f6;
  font-size: 30px;
  cursor: pointer;
  &:hover .anticon {
    transform: rotate(3600deg);
    transition: 15s transform linear;
  }
`

class AcceptOffer extends React.Component {
  state = {
    balance: null,
    amount: '0',
    eth: '0',
  }

  onInput = (e) => {
    let { value } = e.target

    if (value.length === 2 && value[0] == 0) {
      value = value[1]
    }

    if (value.length === 0) {
      value = '0'
    }

    this.setState({
      amount: value.replace(/\D/g, '').slice(0, 6),
    })
  }

  componentDidMount() {
    const { store } = this.props
    const walletuuid = path(['account', 'wallets', 'RUB (QIWI)', 0, 'uuid'], store)

    getWalletBalance(walletuuid).then(balance => {
      this.setState({
        balance
      })
    })
  }

  back = () => {
    const { history } = this.props
    history.goBack()
  }

  buy = () => {
    const { amount } = this.state
    const { store, history } = this.props
    const { offer, account } = store
    const { uuid: offer_uuid } = offer.offer
    const { uuid: account_uuid } = account
    const from_wallet_uuid = path(['account', 'wallets', 'RUB (QIWI)', 0, 'uuid'], store)
    const to_wallet_uuid = path(['account', 'wallets', 'ETH', 0, 'uuid'], store)

    createTransaction({
      body: JSON.stringify({
        offer_uuid,
        account_uuid,
        from_wallet_uuid,
        to_wallet_uuid,
        amount,
      })
    }).then(result => {
      store.setTransactionUUID(result.uuid)
      history.push('/transaction')
    })
  }

  refresh = () => {
    const { store } = this.props
    const walletuuid = path(['account', 'wallets', 'RUB (QIWI)', 0, 'uuid'], store)

    getWalletBalance(walletuuid).then(balance => {
      this.setState({
        balance
      })
    })
  }

  render() {
    const { store } = this.props
    console.log(store.offer)
    const { balance } = this.state

    const inEth = store.offer
      && (this.state.amount != 0)
      && (this.state.amount / store.offer.offer.rate)
      || ''

    return (
      <Center style={{
        width: '470px',
        display: 'flex',
        margin: 'auto',
      }}>
        {store.offer && <Offer {...store.offer} />}
        {/* <QiwiHelp /> */}
        <Row>
          <QiwiAmount>
            <QiwiTitle>QIWI balance</QiwiTitle>
            {balance && <QiwiTitle>{balance}₽</QiwiTitle>}
            <Refresh onClick={this.refresh}>
              <Icon type='retweet' />
            </Refresh>
          </QiwiAmount>
          <HelpField>
          </HelpField>
        </Row>
        <Exchange>
          <RubC>RUB</RubC>
          <Input
            onInput={this.onInput}
            value={this.state.amount}
            style={{ color: +this.state.amount > +balance ? 'red' : 'black' }}
          />
          <TransferIcon src={transferSrc} alt='' />
          <EthC>ETH</EthC>
          <InputRight
            value={inEth}
            style={{ color: +this.state.amount > +balance ? 'red' : 'black' }}
          />
        </Exchange>
        <ButtonsField>
          <BackButton onClick={this.back}>Back</BackButton>
          <BuyButton onClick={this.buy}>Buy</BuyButton>
        </ButtonsField>
      </Center>
    )
  }
}

/*
offer
buyer_fee : 0
rate : 4200045
rate_index : 1
seller_account_uuid : "872de911-f26b-45ed-9341-5a33b28451da"
seller_fee : 0
seller_from_wallet_uuid : "2239b0be-55db-47e2-9551-539ac20fc617"
seller_to_wallet_uuid : "2239b0be-55db-47e2-9551-539ac20fc617"
state : "open"
uuid : "b3369554-3c57-4023-9171-40e903d98a12"
_id : "5b00fc37e389a21d19bdde6c"

wallet
account_uuid : "872de911-f26b-45ed-9341-5a33b28451da"
address : "0xf5cAc2eAC19E047A4C6CB641E264Fa0E5b3A3Af1"
api_token : ""
balance : 0.039979
currency : "ETH"
private_key : "0xad93660f5a2a6dd168faac2ebc978a500fcf280cd2c82c54b73930eef4809c39"
uuid : "2239b0be-55db-47e2-9551-539ac20fc617"
_id : "5b00d004e389a275e09a20b6"
*/

export {
  AcceptOffer
}
