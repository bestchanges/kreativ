import React, { Component } from 'react'
import styled from 'styled-components'
import qr from 'qr-image'

const Wrapper = styled.div`
  width: 196px;
  height: 196px;
  position: relative;
  margin-top: 40px;
`

class QR extends Component {
  render() {
    const { src, alt } = this.props

    if (!src) return null

    const pngBuffer = qr.imageSync(src, {
      type: 'png',
      margin: 1,
      ec_level: 'H',
    })
    const dataURI = 'data:image/png;base64,' + pngBuffer.toString('base64')

    return (
      <Wrapper>
        <img
          width='100%'
          height='100%'
          src={dataURI}
          alt={alt}
        />
      </Wrapper>
    )
  }
}

export {
  QR
}
