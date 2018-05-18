import React from 'react'
import styled from 'styled-components'
import ethLogo from './eth_logo.svg'

const LogoWrapper = styled.div`
  width: 4rem;
  height: 4rem;
  display: inline-block;
`

export const EthLogo = () =>
  <LogoWrapper>
    <img src={ethLogo} alt='eth logo' width='100%' height='100%' />
  </LogoWrapper>
