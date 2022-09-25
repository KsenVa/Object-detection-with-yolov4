import React, { Fragment } from 'react'
import VideoFeed from './components/VideoFeed'
import Records from './components/Record'
import styled from 'styled-components'

function App() {

	// * ---------- STYLE ---------- *


	const TitleOne = styled.h1`
		margin-top : 40px;
		font-size: 30px;
		line-height: 1;
		font-weight: bold;
		color: #638726;
		text-align: center;
		background-color: #1c1b1b;
	
`
	const MainContainer = styled.main`
		display: flex;
		flex-wrap: wrap;
		justify-content: flex-start;
		background-color: #1c1b1b;
		
`
	document.title = "Object detection"
	document.body.style.backgroundColor = "#1c1b1b";

	return(

		<Fragment>
			<TitleOne>Object detection with Yolov4</TitleOne>
			<MainContainer>
				<VideoFeed />
				<Records />
			</MainContainer>
		</Fragment>
	)}

export default App