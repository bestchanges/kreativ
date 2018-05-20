import React from 'react'
import { Button, Col } from 'antd'
import styled from 'styled-components'
import { QR, Center, ButtonGreen } from '../../components'

import { createOffer } from '../../utils/api'

const EthAddress = styled.div`
  margin-top: 20px;
  font-size: 20px;
  color: white;
`

class CreateOffer extends React.Component {
  componentDidCatch() {}

  state = {}

  createOffer = () => {
    const { store } = this.props
    const { account } = store

    createOffer({
      body: JSON.stringify({
        seller_from_wallet_uuid: account.wallets.ETH[0].uuid,
        seller_account_uuid: account.uuid,
        seller_to_wallet_uuid: account.wallets['RUB (QIWI)'][0].uuid,
      }),
    }).then(res => {
      console.log(res)
      this.setState(res)
    })
  }

  render() {
    const { store, history } = this.props
    const { wallet } = this.state

    return (
      <Center>
        <ButtonGreen onClick={this.createOffer}>Create offer</ButtonGreen>
        {wallet && wallet.address && <QR src={wallet.address} />}
        {wallet && wallet.address && <EthAddress>{wallet.address}</EthAddress>}
        <div style={{ padding: '32px' }} />
        <ButtonGreen onClick={() => history.goBack()}>Back</ButtonGreen>
      </Center>
    )
  }
}

export {
  CreateOffer
}
