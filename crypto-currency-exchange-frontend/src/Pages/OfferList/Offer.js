import React from 'react'
import styled from 'styled-components'

const OfferWrapper = styled.div`
  width: 470px;
  height: 68px;
  background-color: #fff;
  box-shadow: 0 1px 1px 0 rgba(0, 0, 0, 0.21);
  display: flex;
  flex-direction: row;
  padding: 0 16px;
  margin-top: 2px;
  cursor: pointer;
`

const Title = styled.div`
  font-family: Futura;
  font-size: 10px;
  font-weight: 500;
  color: #838383;
`

const X1 = styled.div`
  font-size: 16px;
  font-weight: 500;
  color: #2a2a2a;
`

const Rate = styled.div`
  font-size: 12px;
  font-weight: 500;
  color: #2a2a2a;
`

const Colon = styled.div`
  display: flex;
  flex-direction: column;
  padding: 16px 8px;
`

export const Offer = ({ offer, wallet, takeOffer }) =>
  <OfferWrapper onClick={() => takeOffer && takeOffer(offer.uuid)}>
    <Colon>
      <Title>sell</Title>
      <X1>{wallet.balance} {wallet.currency}</X1>
    </Colon>
    <Colon>
      <Title>buy</Title>
      <X1>{(offer.rate * wallet.balance).toFixed(6)}</X1>
    </Colon>
    <Colon>
      <Title>Rate</Title>
      <Rate>{offer.rate}</Rate>
    </Colon>
    <Colon>
      <Title>Rate index</Title>
      <Rate>{offer.rate_index}</Rate>
    </Colon>
  </OfferWrapper>
