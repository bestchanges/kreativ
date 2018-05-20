import React, { Component } from 'react'
import { Input, Form, Button, Col } from 'antd'

import { localize } from '../../settings'
import { createQiwiAccount } from '../../utils/api'
import { Title } from '../../components'

const formItemLayout = {
  labelCol: {
    xs: { span: 3 },
  },
  wrapperCol: {
    xs: { span: 10 },
  },
}

const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 10,
      offset: 3,
    },
  },
}

class Wallet extends Component {
  state = {
    token: '',
    phone: '',
    wallet: ''
  }

  onChange = (e) => {
    e.preventDefault()
    const { id, value } = e.target
    this.setState({ [id]: value })
  }

  submit = (e) => {
    e.preventDefault()
    const { history, store } = this.props
    store.setWalletUUID('0x98ee18d7a1f7510b78b36f5a16471c7cd0c1c531')
    createQiwiAccount({
      body: JSON.stringify(this.state),
    }).then(json => {
      console.log(json)
      console.log(history)
      history.push('/sell')
    })
  }

  render() {
    const { token, phone, wallet } = this.state

    return (
      <Col span={20} offset={2} style={{ padding: '2rem 0' }}>
        <Title>{localize.Wallet.title}</Title>
        <Form>
          <Form.Item label={localize.Wallet.token} {...formItemLayout}>
            <Input
              id='token'
              onChange={this.onChange}
              value={token}
            />
          </Form.Item>
          <Form.Item label={localize.Wallet.phone} {...formItemLayout}>
            <Input
              id='phone'
              onChange={this.onChange}
              value={phone}
            />
          </Form.Item>
          <Form.Item label={localize.Wallet.wallet} {...formItemLayout}>
            <Input
              id='wallet'
              onChange={this.onChange}
              value={wallet}
            />
          </Form.Item>
          <Form.Item {...tailFormItemLayout}>
            <Button onClick={this.submit}>{localize.Wallet.submit}</Button>
          </Form.Item>
        </Form>
      </Col>
    )
  }
}

export {
  Wallet
}
