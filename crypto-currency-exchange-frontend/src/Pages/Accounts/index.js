import React from 'react'
import { Col, Button } from 'antd'
import { find, propEq } from 'ramda'

import { getAccounts, getAuth } from '../../utils/api'

class Accounts extends React.Component {
  state = {
    accounts: [],
  }

  componentDidMount() {
    getAccounts().then(accounts => {
      this.setState({
        accounts,
      })
    })
  }

  takeAccount = (e) => {
    e.preventDefault()
    const { history, store } = this.props
    const { id: uuid } = e.target
    getAuth(uuid).then(account => {
      console.log(account)
      store.setAccount(account)
      history.push('/sellbuy')
    })
  }

  render() {
    const { store } = this.props
    const { accounts } = this.state

    return (
      <Col span={20} offset={2}>
        {accounts && accounts.map(({ ethereum_address, name, qiwi_address, uuid }) =>
          <ul key={uuid}>
            <li>Name: {name}</li>
            {ethereum_address && <li>ETH: {ethereum_address}</li>}
            <li>QIWI: {qiwi_address}</li>
            <li><Button id={uuid} onClick={this.takeAccount}>take account</Button></li>
          </ul>
        )}
      </Col>
    )
  }
}

export {
  Accounts
}
