import React from 'react'
import styled from 'styled-components'
import MegaFonSrc from './megafon-logo-white.svg'

const LeftTopCorner = styled.div`
  top: 24px;
  left: 24px;
  position: absolute;
`

export class MegaFon extends React.Component {
  render() {
    return (
      <LeftTopCorner>
        <img src={MegaFonSrc} alt='megafon' />
      </LeftTopCorner>
    )
  }
}
