export default function ImageLoader(originalImage, generatedImage, loader) {
    return (
        <div className="container p-4 d-flex justify-content-center">
            <div className="float-start">
                <h3 className="mb-4 text-center">Hazy Image</h3>
                <img src="https://i.pinimg.com/originals/24/8a/45/248a452587f56539da876d6e2bd13007.png" class="rounded float-start" alt="..." />
            </div>
            <div className="float-start z-1 position-absolute d-none">
                <h3 className="mb-4">Dehaze Image</h3>
                <img src="https://i.pinimg.com/originals/24/8a/45/248a452587f56539da876d6e2bd13007.png" class="rounded float-start" alt="..." />
            </div>
        </div>
    )
}