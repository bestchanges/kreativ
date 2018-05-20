import React from 'react'
import { Router, Route } from 'react-router-dom'
import createBrowserHistory from 'history/createBrowserHistory'
import { observer } from 'mobx-react'
import { Layout, Row } from 'antd'
import styled from 'styled-components'

import {
  SellerBuyer,
  Wallet,
  Sell,
  Accounts,
  CreateOffer,
  OfferList,
  AcceptOffer,
  Transaction,
} from './Pages'
import { Store } from './Store'

const routes = [
  {
    path: '/sellbuy',
    component: observer(SellerBuyer),
  }, {
    path: '/wallet',
    component: observer(Wallet),
  }, {
    path: '/sell',
    component: observer(Sell)
  }, {
    exact: true,
    path: '/',
    component: observer(Accounts)
  }, {
    path: '/create_offer',
    component: observer(CreateOffer)
  }, {
    path: '/offer_list',
    component: observer(OfferList),
  }, {
    path: '/accept_offer',
    component: observer(AcceptOffer),
  }, {
    path: '/transaction',
    component: observer(Transaction),
  }
]

const store = new Store()
const history = createBrowserHistory()

// const BackButton = ({ history }) => history.location.pathname !== '/'
//   ? <Button onClick={history.goBack}>
//       <Icon type='left' />Back
//     </Button>
//   : null

const FooterWrapper = styled.div`
  font-family: Futura;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  color: #ffffff;
`

const App = () =>
  <Router history={history}>
    <Layout className='app'>
      {/* <Layout.Header>
        <Link to='/'><Logo>Creative</Logo></Link>
      </Layout.Header> */}
      <Layout>
        {/* <Row>
          <Col offset={2} span={20}>
            <Route component={BackButton} />
          </Col>
        </Row> */}
        <Row>
          {routes.map(({ component: Container, ...route }, i) =>
            <Route
              key={i}
              render={
                (other) => <Container
                  store={store}
                  {...other}
                />
              }
              {...route}
            />
          )}
        </Row>
      </Layout>
      <Layout.Footer>
        <FooterWrapper>
          © 2018 Actum Digital Hackaton “Creative” team
        </FooterWrapper>
      </Layout.Footer>
    </Layout>
  </Router>

export default App
