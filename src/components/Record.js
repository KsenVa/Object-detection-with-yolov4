import React, {useState, useEffect, useRef} from 'react';
import styled from 'styled-components'


const Cam = message => {


	const VideoFeedSection = styled.section`
        display: flex;
        flex-direction: column;
        margin: 10px 10px;
        background-color: #1c1b1b;
        padding: 20px;
        width: 45%;
        high: 600px;
        -webkit-box-sizing: border-box;
        font-size: 15px;
        line-height: 1;
        font-weight: normal;
        color: #A0522D;
        
        
        .layer {
            overflow: auto; /* Добавляем полосы прокрутки */
            width: 100%; /* Ширина блока */
            height: 432px; /* Высота блока */
            padding: 5px; /* Поля вокруг текста */
           }
           
         .layer::-webkit-scrollbar {
          width: 6px;
        }
        
        .layer::-webkit-scrollbar-track {
          -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, 0.2) inset;
          background-color: #f9f9fd;
        }
        
        .layer::-webkit-scrollbar-thumb {
          background-color: #ba4a52;
          background-image: -webkit-linear-gradient(45deg,rgba(255, 255, 255, .25) 25%,
                            transparent 25%,
                            transparent 50%,
                            rgba(255, 255, 255, .25) 50%,
                            rgba(255, 255, 255, .25) 75%,
                            transparent 75%,
                            transparent);
        }
        h2 {
            margin-top : 0;
            font-size: 30px;
            line-height: 1;
            font-weight: normal;
            color: #B8860B;
            text-align: center;
        }
        
        .btn-group button {
        background-color: #ba4a52; /* Green background */
        border: 2px solid #B8860B; /* Green border */
        color: #faf7edf7; /* White text */
        padding: 10px 40px; /* Some padding */
        cursor: pointer; /* Pointer/hand icon */
        float: left; /* Float the buttons side by side */
        border-radius: 4px;
         margin: 20px;
         text-align: center;
         align-items: center;
         position: relative;
         left: 30%;
         transform: translate(-50%, 0);
        }
        .btn-group button:not(:last-child) {
        border-right: none; /* Prevent double borders */
        }
      
        /* Add a background color on hover */
        .btn-group button:hover {
            background-color: #995536;
        }
        .btn-group button:focus {
            color: #1c1b1b;
        }
        
        IMG.displayed {
        display: block;
        margin-left: auto;
        margin-right: auto 
        }
        
`

    const [records, setRecords] = useState([]);
	let title
    let detection = 0
    const name = useRef("initialValue")


    function startRecord(){
             name.current = "record";
    }

     function stopRecord(){
            name.current = "notRecord";
    }

    useEffect(() => {

        setInterval(() => {
        console.log("usef",name)
                if(name.current === "record"){

                    fetch('/detect').then(res => res.json()).then(data => {
                    if (data.detect === 1) {
                        detection = 1
                        title = new Date().toLocaleString()

                        fetch('/image').then(function (response) {
                            return response.blob();
                        })
                            .then(function (imageBlob) {
                                console.log("frame")
                                let blob = new Blob([imageBlob], {type: 'image/jpeg'});
                                const href = URL.createObjectURL(blob);
                                setRecords(records => {
                                    return [...records, {href, title}];
                                });

                            });


                        console.log("records", records)
                        console.log("detection", detection)

                    } else {
                        detection = 0
                        console.log("not detected")

                    }
                });

                }

                if (name.current==="notRecord") {
                    console.log(name)
                }


        }, 100)
    }, );


return (
	<VideoFeedSection className='some-space'>

        <h2>Records </h2>

        <div class="btn-group" >
          <div>
            <button id="start_rec" className="btn-success" onClick={() => {startRecord();}} > Start recording </button>
          </div>

          <div className="btn-group mr-2" role="group">
            <button className="btn btn-danger" onClick={() => {stopRecord();}} > Stop recording </button>
          </div>

        </div>
        <div className="layer">
        <div class="row">

            {!records.length
                ? null
                :

                records.slice().reverse().map(record => {
                    return (
                        <div class="record" key={record.title}>
                            <div class="card">
                                <h5 className="card-title" align="center">Object detected! ({record.title})</h5>
                                <img class="displayed" width="416" height="290" src={record.href} />
                            </div>
                        </div>
                    );
                })}
        </div>
        </div>
	</VideoFeedSection>
 )
};
export default Cam;







