import React from 'react'
import styled from 'styled-components'

import { Center } from '../../components'
import { getListOffers } from '../../utils/api'
import { Offer } from './Offer'


class OfferList extends React.Component {
  state = {
    offers: [],
  }

  componentDidMount() {
    getListOffers().then(offers => {
      this.setState({
        offers,
      })
    })
  }

  takeOffer = (uuid) => {
    const { history, store } = this.props
    const { offers } = this.state

    const offer = offers.find(
      ({ offer }) => offer.uuid === uuid
    )
    store.setCurrentOffer(offer)

    history.push('/accept_offer')
  }

  render() {
    const { offers } = this.state

    return (
      <Center>
        {offers && offers.map((params) =>
          <Offer
            key={params.offer.uuid}
            {...params}
            takeOffer={this.takeOffer}
          />
        )}
        {(!offers || !offers.length) &&
          <div style={{ color: '#fff', fontWeight: '500' }}>
            Loading...
          </div>
        }
      </Center>
    )
  }
}

export {
  OfferList
}
