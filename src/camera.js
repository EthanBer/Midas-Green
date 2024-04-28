import React, { useState, useRef } from "react";
import "./camera.css"
import {Camera} from "react-camera-pro";

const CameraComponent = () => {
    const camera = useRef(null);
    const [image, setImage] = useState(null);
  
    return (
      <div>
        <Camera ref={camera} aspectRatio={16/9}/>
        <button onClick={() => setImage(camera.current.takePhoto())}>Take photo</button>
        <img src={image} className="image" alt='Taken photo'/>
      </div>
    );
  }

  export default CameraComponent