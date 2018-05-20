import React from 'react'
import { Button, Col } from 'antd'

import { createOffer } from '../../utils/api'

class CreateOffer extends React.Component {
  componentDidCatch() {}

  createOffer = () => {
    const { store } = this.props
    const { uuid } = store

    createOffer({
      body: JSON.stringify({
        seller_from_wallet_uuid: uuid,
      }),
    }).then(console.log)
  }

  render() {
    const { store } = this.props

    return (
      <Col span={20} offset={2}>
        {store.account && store.account.name}
        <Button onClick={this.createOffer}>Create offer</Button>
      </Col>
    )
  }
}

export {
  CreateOffer
}