import React from 'react'
import styled from 'styled-components'
import { EthLogo } from '../attach'

import { color } from './styles'

const Head = styled.div`
  font-size: 2rem;
  color: ${color.black};
`

const Header = () =>
  <Head>
    Currency exchange test <EthLogo />
  </Head>

export {
  Header,
}
