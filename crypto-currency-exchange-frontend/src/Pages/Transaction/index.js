import React from 'react'
import styled from 'styled-components'
import { executeTransaction } from '../../utils/api'
import { Icon } from 'antd'
import { Flex, Center, ButtonGreen } from '../../components'

const Information = Flex.extend`
  width: 470px;
  height: 80px;
  padding: 16px 16px;
  margin-top: 2px;
  position: relative;
`

const LinkToEtherscan = styled.a`
  font-size: 30px;
  font-family: Futura;
`

const Text = styled.span`
  font-size: 30px;
  font-family: Futura;
`

const Refresh = styled.div`
  position: absolute;
  height: 80px;
  right: 0;
  top: 0;
  width: 80px;
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

class Transaction extends React.Component {
  state = {}

  componentDidMount() {
    // const uuid = 'd16a5022-9e97-475d-a32b-7a5fc96d3f02'
    const { store } = this.props
    const uuid = store.transaction_uuid

    executeTransaction({
      body: JSON.stringify({
        transaction_uuid: uuid,
      })
    }).then(res => {
      console.log(res)
      this.setState({
        ...res,
        time: (new Date()).toString(),
      })
    })
  }

  refresh = () => {
    // const uuid = 'd16a5022-9e97-475d-a32b-7a5fc96d3f02'
    const { store } = this.props
    const uuid = store.transaction_uuid

    executeTransaction({
      body: JSON.stringify({
        transaction_uuid: uuid,
      })
    }).then(res => {
      console.log(res)
      this.setState({
        ...res,
        time: (new Date()).toString(),
      })
    })
  }

  render() {
    const { tx_id, state, time } = this.state

    return (
      <Center>
        <Information style={{ padding: '8px 20px', height: '40px', fontSize: '16px' }}>
          {time}
        </Information>
        {tx_id && <Information>
          <LinkToEtherscan
            href={`https://rinkeby.etherscan.io/tx/${tx_id}`}
            target='_blank'
          >Check on Etherscan</LinkToEtherscan>
        </Information>}
        <Information>
          <Text>{'Status: '}</Text><Text style={{
            color: (state === 'finished' && 'green') || 'gray'
          }}>{state}</Text>
          <Refresh onClick={this.refresh}>
            <Icon type='retweet' />
          </Refresh>
        </Information>
      </Center>
    )
  }
}

export {
  Transaction
}
