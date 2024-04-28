import './App.css';
import './assets/css/main.css'
import myImage from './images/banner.jpg'
import React, { useState, useRef } from 'react';
import {Camera} from "react-camera-pro";

function App() {
  
  const [isVisible, setIsVisible] = useState(false);
  const camera = useRef(null);
  const [image, setImage] = useState(null);
  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  }


  const [selectedFile, setSelectedFile] = useState(null);
  const [diagnosisText, setDiagnosisText] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const sendFile = (file) => {

    var data = new FormData()
    data.append('file', file)
    setDiagnosisText("loading....")

    fetch("http://127.0.0.1:5000/upload", {
      method: 'POST',
      body: data
    }).then((response) => {
      response.json().then((value) => {
        setDiagnosisText(value.body)
      })
    }).catch(() => {
      setDiagnosisText("Error, tokens may have run out")
    })
  }

  return (
    <div className='content'>
      <section class="banner style1 orient-left content-align-left image-position-right fullscreen onload-image-fade-in onload-content-fade-right">
						<div class="content">
							<h1>Upload Image</h1>
              <form onSubmit={(e)=>{e.preventDefault();}}>
                <input type="file" onChange={handleFileChange} className='button' accept="image/*" />
                <button type="submit" className='button' onClick={()=>sendFile(selectedFile)}>Upload File</button>
              </form>
              {selectedFile && (
                <div>
                  <h2>Selected Image:</h2>
                  <img src={URL.createObjectURL(selectedFile)} alt="Selected" style={{ maxWidth: '100%' }} />
                </div>
              )}
              <div>
                <button onClick = {toggleVisibility}> 
                  {isVisible ?  'Hide Camera' : 'Take a Picture'}
                </button>
                <div style={{'width': 200, margin: 20}}>
                  {isVisible && <Camera aspectRatio={1} ref={camera} />}
                </div>
                {isVisible && <button onClick={() => setImage(camera.current.takePhoto())}>Take photo</button> }
                {image && <img style={{'width': 200, margin: 20, display: 'block'}} src={image} alt='capture'/> }
              </div>
              {image && <button type="submit" className='button' onClick={() => sendFile(image)}>Upload Capture</button>}
						</div>
						<div className="responseText">
              <p>
                {diagnosisText}
              </p>
						</div>
					</section>
    </div>
  );
}

export default App;
