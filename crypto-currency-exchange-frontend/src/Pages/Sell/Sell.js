import React, { Component } from 'react'
import { evolve, not } from 'ramda'
import {
  Layout,
  Col,
  Row,
  Input,
  Button,
  Form,
  Switch,
} from 'antd'
import { QR, Title } from '../../components'
import { formatMoney } from '../../utils'
import { localize } from '../../settings'

class Sell extends Component {
  state = {
    autoExchange: false,
  }

  copyWalletUUID = () => {
    var copyText = document.getElementById('showWalletUUID')
    copyText.select()
    document.execCommand('copy')

    if (window.getSelection) {
      window.getSelection().removeAllRanges()
    } else if (document.selection) {
      document.selection.empty()
    }
  }

  toggleAutoExchange = () => {
    this.setState(evolve({
      autoExchange: not,
    }))
  }

  render() {
    const { store } = this.props
    const { walletUUID } = store
    const { autoExchange } = this.state

    return (
      <Layout>
        <Row>
          <Col offset={2} span={12} style={{ padding: '2rem 0' }}>
            <Title>{localize.Sell.title}</Title>
            <Form>
              <Form.Item>
                <Input.Search
                  id='showWalletUUID'
                  value={walletUUID}
                  onSearch={this.copyWalletUUID}
                  enterButton='copy'
                  onChange={() => null}
                />
              </Form.Item>
              <Form.Item>
                <QR src={walletUUID} />
              </Form.Item>
            </Form>
          </Col>
        </Row>
        <Row>
          <Col offset={2} span={18} style={{ padding: '2rem 0' }}>
            <Form layout='inline'>
              <Form.Item>
                <Input
                  addonAfter='ETH'
                  value={formatMoney(100)}
                  onChange={() => null}
                />
              </Form.Item>
              <Form.Item>
                <Input
                  addonAfter='RUB'
                  value={formatMoney(4200000)}
                  onChange={() => null}
                />
              </Form.Item>
            </Form>
            <Form layout='inline'>
              <Form.Item>
                <Button disabled={autoExchange}>{localize.Sell.exchange}</Button>
              </Form.Item>
              <Form.Item>
                <Switch
                  value={autoExchange}
                  onChange={this.toggleAutoExchange}
                /> {localize.Sell.autoExch}
              </Form.Item>
            </Form>
          </Col>
        </Row>
      </Layout>
    )
  }
}

export {
  Sell
}
