// import './App.css';
import './assets/css/main.css'
import myImage from './images/banner.jpg'
import React, { useState, useRef } from 'react';
// import {Camera} from "react-camera-pro";

function App() {
  // const [isVisible, setIsVisible] = useState(false);
  // const camera = useRef(null);
  // const [image, setImage] = useState(null);
  // const toggleVisibility = () => {
  //   setIsVisible(!isVisible);
  // }
  // return (
  //   <div>
  //     <p className="App-header">
  //       The Camera
  //     </p>

  //     <button onClick = {toggleVisibility}> 
  //       {isVisible ?  'Hide Camera' : 'Take a Picture'}
  //     </button>
  //     {isVisible && <Camera isImageMirror={false} ref={camera} width={320} height={240}/>}
  //     {isVisible &&  <button onClick={() => setImage(camera.current.takePhoto())}>Take photo</button> }
  //     {isVisible && <img src={image} className="image" alt='Taken photo'/> }
  //   </div>
  // );
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // You can perform further processing here, like uploading the image to a server
    if (selectedFile) {
      console.log('Selected file:', selectedFile);
      // You can use FormData to upload the selected file
      const formData = new FormData();
      formData.append('image', selectedFile);
      // Example of uploading the file
      // fetch('/upload', {
      //   method: 'POST',
      //   body: formData
      // })
      // .then(response => response.json())
      // .then(data => console.log(data))
      // .catch(error => console.error('Error uploading file:', error));
    } else {
      console.log('No file selected');
    }
  };

  return (
    <div>
      <section className="banner style1 orient-left content-align-left image-position-right fullscreen onload-image-fade-in onload-content-fade-right">
				<div className="content">
					<h1>Upload Image</h1>
          <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} className='button' accept="image/*" />
          </form><ul className="actions stacked">
						<li><a><button type="submit" className="button big wide smooth-scroll-middle">Upload</button></a></li>
					</ul>
				</div>
				<div className="image">
					<img src={myImage} alt="banner" />
          {selectedFile && (
            <div>
              <h2>Selected Image:</h2>
              <img src={URL.createObjectURL(selectedFile)} alt="Selected" style={{ width: '30px', heigh: 'auto', alignItems: 'right'}} />
            </div>
          )}
				</div>
			</section>
    </div>
  );
}

export default App;
