import React from 'react'
import { Icon } from 'antd'
import styled from 'styled-components'
import mansvg from './man.svg'

import { getAccounts, getAuth } from '../../utils/api'
import { Head, Center } from '../../components'

const GreenLine = styled.div`
  position: absolute;
  left: 0;
  height: 100%;
  width: 0px;
  background: #00be73;
  transition: .2s width ease;
`

const RightGreen = styled.div`
  position: absolute;
  right: 0;
  width: 40px;
  height: 100%;
  background: #e0ffe5;
  align-items: center;
  justify-content: center;
  display: none;
`

const SubHead = styled.div`
	font-size: 30px;
	font-weight: 500;
	text-align: center;
  color: #ffffff;
  margin-bottom: 32px;
`

const AccountWrapper = styled.div`
  width: 470px;
	height: 140px;
	background-color: #ffffff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: row;
  margin-top: 8px;
  cursor: pointer;
  position: relative;
  &:hover ${GreenLine} {
    width: 6px;
  }
  &:hover ${RightGreen} {
    display: flex;
  }
`

const Ava = styled.div`
  display: flex;
  width: 140px;
  height: 140px;
  padding: 16px;
`

const Info = styled.div`
  display: flex;
  flex-direction: column;
  padding: 16px;
`

const Name = styled.div`
  font-size: 26px;
  font-weight: 500;
  color: #2a2a2a;
`

const Curr = styled.div`
  font-size: 12px;
  font-weight: 500;
  color: #838383;
`

const CurrAcc = styled.div`
  font-size: 11px;
  font-weight: 500;
  color: #2a2a2a;
`

const Account = ({ name, ethereum_address, qiwi_address, uuid, takeAccount }) =>
  <AccountWrapper onClick={() => takeAccount(uuid)} >
    <Ava>
      <img alt='avatar' src={mansvg} width='100%' height='100%' />
    </Ava>
    <Info>
      <Name>{name}</Name>
      <Curr>QIWI</Curr>
      <CurrAcc>{qiwi_address}</CurrAcc>
      {ethereum_address && <Curr>ETH</Curr>}
      {ethereum_address && <CurrAcc>{ethereum_address}</CurrAcc>}
    </Info>
    <GreenLine />
    <RightGreen>
      <Icon type='right' style={{ color: '#00be73' }} />
    </RightGreen>
  </AccountWrapper>

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

  takeAccount = (uuid) => {
    const { history, store } = this.props

    getAuth(uuid).then(account => {
      store.setAccount(account)
      history.push('/sellbuy')
    })
  }

  render() {
    const { accounts } = this.state

    return (
      <Center>
        <Head>CreativeBase</Head>
        <SubHead>Choose Your account</SubHead>
        {accounts && accounts.map(({ ethereum_address, name, qiwi_address, uuid }) =>
          <Account
            key={uuid}
            name={name}
            qiwi_address={qiwi_address}
            ethereum_address={ethereum_address}
            uuid={uuid}
            takeAccount={this.takeAccount}
          />
        )}
      </Center>
    )
  }
}

export {
  Accounts
}
