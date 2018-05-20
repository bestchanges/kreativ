import React from 'react'
import { Router, Route, Link } from 'react-router-dom'
import createBrowserHistory from 'history/createBrowserHistory'
import { observer } from 'mobx-react'
import { Layout, Col, Button, Icon, Row } from 'antd'
import styled from 'styled-components'

import {
  SellerBuyer,
  Wallet,
  Sell,
  Accounts,
  CreateOffer,
} from './Pages'
import { Store } from './Store'

const Logo = styled.span`
  font-size: 2rem;
  font-family: futura;
  color: #fff;
`

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
  }
]

const store = new Store()
const history = createBrowserHistory()

const BackButton = ({ history }) => history.location.pathname !== '/'
  ? <Button onClick={history.goBack}>
      <Icon type='left' />Back
    </Button>
  : null

const App = () =>
  <Router history={history}>
    <Layout className='app'>
      <Layout.Header>
        <Link to='/'><Logo>Creative</Logo></Link>
      </Layout.Header>
      <Layout style={{ paddingTop: '2rem' }}>
        <Row>
          <Col offset={2} span={20}>
            <Route component={BackButton} />
          </Col>
        </Row>
        <Row>
          {routes.map(({ component: Container, ...route }) =>
            <Route
              key={route.path}
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
      <Layout.Footer>© 2018 Actum Digital Hackaton “Creative” team</Layout.Footer>
    </Layout>
  </Router>

export default App
