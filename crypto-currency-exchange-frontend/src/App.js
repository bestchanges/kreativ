import React from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import { Layout, Col } from 'antd'
import styled from 'styled-components'

import { SellerBuyer } from './Pages'

const Logo = styled.span`
  font-size: 2rem;
  font-family: futura;
  color: #fff;
`

const WhiteSpace = styled.div`
  padding: 1rem 0;
`

const App = () =>
  <Router>
    <div className='app'>
      <Layout.Header>
        <Logo>Creative</Logo>
      </Layout.Header>
      <WhiteSpace />
      <Col offset={1} span={22}>
        <Layout>
          <Route path='/' component={SellerBuyer} />
        </Layout>
      </Col>
    </div>
  </Router>

export default App
