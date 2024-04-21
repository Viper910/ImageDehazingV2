import './App.css';
import { useState } from "react"
import DragDrop from './components/DragDrop';
import ImageLoader from './components/ImageLoader';
function App() {

  const [loading, setLoading] = useState(false);

  const generateHandler = () => {
    setLoading(true)
  }

  return (
    <div className="App d-flex flex-column min-vh-100">
      <nav class="navbar bg-body-tertiary p-3">
        <div class="container-fluid">
          <span class="navbar-brand mb-0 h1">ImageDehazingV2</span>
        </div>
      </nav>
      <div className="container p-4 d-flex justify-content-center">
        <DragDrop />
      </div>

      <ImageLoader originalImage="https://i.pinimg.com/originals/24/8a/45/248a452587f56539da876d6e2bd13007.png" generatedImage="https://i.pinimg.com/originals/24/8a/45/248a452587f56539da876d6e2bd13007.png" loader={loading}/>
      
      <div class="container text-center p-4">
        {loading ? <div class="spinner-border text-success" role="status">
        </div> :
          <button onClick={generateHandler} type="button" class="btn btn-success float-center p-2">Generate</button>
        }
        <br/>
        <button onClick={generateHandler} type="button" class="btn btn-success float-center m-2 p-2">Comaprison</button>
      </div>
      <footer className='mt-auto text-center'>
         This website will dehaze the satellite images.
      </footer>
    </div>
  );
}

export default App;
