export default function ImageLoader({ originalImage, generatedImage, originalImageLoading, generatedImageloading }) {

    const hazyImageClassName = generatedImage ? "float-start d-none" : "float-start";
    const dehazeImageClassName = generatedImage ? "float-start" : "float-start d-none";
    const defaultImage = 'http://127.0.0.1:5000/static/generated/default.png'
    return (
        <div className="container p-4 d-flex justify-content-center">
            <div className="float-start">
                <h3 className="mb-4 text-center">Hazy Image</h3>
                {originalImageLoading ? <div class="spinner-border text-success" role="status" /> :
                    <img src={originalImage} style={{ margin: "34px", padding: "5px" }} height="256px" width="256px" class="rounded float-start" alt="HazeImage" />
                }
            </div>
            <div className="float-start">
                <h3 className="mb-4 text-center">Dehaze Image</h3>
                {generatedImageloading ? <div className="d-flex justify-content-center" style={{marginTop:"150px"}}>
                    <div class="spinner-grow text-secondary" role="status"></div>
                    <div class="spinner-grow text-secondary" role="status"></div>
                    <div class="spinner-grow text-secondary" role="status"></div>
                </div> :
                    <img src={generatedImage ? generatedImage : defaultImage} class="rounded float-start" alt="DehazeImage" />
                }
            </div>
        </div>
    )
}