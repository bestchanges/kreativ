import styled from 'styled-components'

export { Header } from './Header'
export { QR } from './QR'
export { Title } from './Title'

export const Head = styled.div`
	font-size: 72px;
	font-weight: 500;
	text-align: center;
	color: #ffffff;
	font-family: Helvetica;
`

export const Center = styled.div`
  padding-top: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
`

export const ButtonGreen = styled.button`
  height: 50px;
  background-color: #00be73;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5), 0 2px 4px 0 rgba(0, 0, 0, 0.18);
	font-size: 24px;
	font-weight: 500;
	text-align: center;
  color: #fff;
  line-height: 48px;
  letter-spacing: 1px;
  cursor: pointer;
  outline: none;
  border: none;
  font-family: Helvetica;
`

export const Flex = styled.div`
  display: flex;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
`
