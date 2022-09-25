import styled from 'styled-components'


const Cam = message => {
	const VideoFeedSection = styled.section`
        display: flex;
        flex-direction: column;
        margin: 10px 10px;
        
        
        padding: 20px;
        width: 50%;
        -webkit-box-sizing: border-box;
        h2 {
            margin-top : 10px;
            font-size: 30px;
            line-height: 1;
            font-weight: normal;
            color: #B8860B;
            text-align: center;
        }
        
        .video {
         margin: 10px 0px;
        }
`


return (

	<VideoFeedSection className='some-space'>
        <h2>Real-time predictions</h2>

        <div class="video">

           <img width="100%"
            src="http://localhost:3000/video_feed"
            alt="Video"
           />

        </div>

	</VideoFeedSection>

 );
};

export default Cam;