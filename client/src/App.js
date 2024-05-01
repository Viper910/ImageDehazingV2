import './App.css';
import { useState } from "react"
// import DragDrop from './components/DragDrop';
import ImageLoader from './components/ImageLoader';
import { FileUploader } from "react-drag-drop-files";
import { generateDehazeImage, uploadImage } from './services/imageService';

function App() {

  const [originalImageLoading, setOriginalImageLoading] = useState(false);
  const [generatedImageloading, setGeneratedImageloading] = useState(false);
  const [dehazeImage, setDehazeImage] = useState(null);
  const [uploadedImagePath, setUploadedImagePath] = useState("");
  const fileTypes = ["JPG", "PNG"];
  const [infoBarSelect, setInfoBarSelect] = useState(false);
  const [file, setFile] = useState(null);
  const formData = new FormData();
  const [infoBar, setInfoBar] = useState("alert alert-success m-4 zoom-out-box");
  const [checkImg, setCheckImg] = useState(false);

  const handleChange = async (file) => {
    setOriginalImageLoading(true);
    setFile(file);
    formData.append('image', file);
    const { data } = await uploadImage(formData);
    setUploadedImagePath(data.file_path);
    setOriginalImageLoading(false);
    setDehazeImage(null);
    setCheckImg(true);
  };

  const generateHandler = async () => {
    setGeneratedImageloading(true)
    const { data } = await generateDehazeImage(file.name);
    console.log(data);
    setDehazeImage(data);
    setGeneratedImageloading(false)
  }
  const scoreCheck = () => {
    setInfoBarSelect(!infoBarSelect);
    setInfoBar(infoBarSelect ? "alert alert-success m-4 zoom-out-box" : "alert alert-success m-4 zoom-in-box d-none");
  }

  return (
    <div className="App d-flex flex-column min-vh-100">
      <nav className="navbar bg-body-tertiary p-3">
        <div className="container-fluid">
          <span className="navbar-brand mb-0 h1">ImageDehazingV2</span>
        </div>
      </nav>
      <div className="container p-4 d-flex justify-content-center" style={{marginTop:"4%"}}>
        <FileUploader className="fileuploader" handleChange={handleChange} name="file" types={fileTypes} multiple={false} />
      </div>

      {checkImg ? <>
        <ImageLoader originalImage={uploadedImagePath} generatedImage={dehazeImage ? dehazeImage.file_path : ""} generatedImageloading={generatedImageloading} originalImageLoading={originalImageLoading} />
        <div className="container text-center p-4">
          {generatedImageloading ? <div className="spinner-border text-success" role="status">
          </div> :
            <button onClick={generateHandler} type="button" className="btn btn-success float-center p-2">Generate</button>
          }
          <br />
          {dehazeImage ? <>
            <button type="button" className="btn btn-success float-center m-2 p-2" onClick={scoreCheck}>Score Check</button>
            <div className={infoBar} role="alert">
              <p>Peak signal-to-noise ratio (PSNR) = {dehazeImage.psnr}</p>
              <p>Structural similarity index measure (ssim) = {dehazeImage.ssim}</p>
            </div>
          </> :
            <></>
          }
        </div>
      </> : <></>}
      <footer className='mt-auto text-center  bg-body-tertiary h6'>
        This website will dehaze the satellite images.
      </footer>
    </div>
  );
}

export default App;
