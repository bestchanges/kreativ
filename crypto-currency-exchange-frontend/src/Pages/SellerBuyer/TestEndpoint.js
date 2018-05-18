import React, { Component } from 'react'
import { Input, Form, Button } from 'antd'

class TestEndpoint extends Component {
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

  submit = () => {
    fetch(`${window.endpointOrigin}/createaccountqiwi`, {
      method: 'POST',
      body: JSON.stringify(this.state)
    })
      .then(res => res.json())
      .then(console.log)
  }

  render() {
    const { token, phone, wallet } = this.state

    return (
      <Form>
        <Form.Item>
          <Input
            id='token'
            addonBefore='token'
            onChange={this.onChange}
            value={token}
          />
        </Form.Item>
        <Form.Item>
          <Input
            id='phone'
            addonBefore='phone'
            onChange={this.onChange}
            value={phone}
          />
        </Form.Item>
        <Form.Item>
          <Input
            id='wallet'
            addonBefore='wallet'
            onChange={this.onChange}
            value={wallet}
          />
        </Form.Item>
        <Button onClick={this.submit}>Request</Button>
      </Form>
    )
  }
}

export {
  TestEndpoint
}

/*

/createaccountqiwi

{
  'token': token,
  'phone': phone
}

*/