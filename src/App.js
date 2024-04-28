import './App.css';
import CameraComponent from './camera';

function showCamera() {
  alert('Poggers')
}

function App() {
  return (
    <div>
      <p className="App-header">
        The Camera
      </p>

      <button onClickv= {showCamera}> 
        Take a Picture
      </button>
      <CameraComponent className="camera" >

      </CameraComponent>
    </div>
  );
}

export default App;
