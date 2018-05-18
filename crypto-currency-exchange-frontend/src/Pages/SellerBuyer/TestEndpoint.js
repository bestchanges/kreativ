import React, { Component } from 'react'
import { Input, Form } from 'antd'

class TestEndpoint extends Component {
  render() {
    return (
      <Form>
        <Form.Item>
          <Input />
        </Form.Item>
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