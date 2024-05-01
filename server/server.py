from flask import Flask, request, jsonify, make_response, url_for
import os
from flask_cors import CORS
from dehazeImage import generateDehazeImage
from path import BASE_PATH
app = Flask(__name__,static_url_path='/static')

CORS(app)

# Define the directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


last_uploaded = ""

# Endpoint to upload an image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return make_response(jsonify({'error': 'No file part'}), 404)
    file = request.files['image']

    if file.filename == '':
        return make_response(jsonify({'error': 'No selected file'}), 404)

    if file:
        filename = file.filename
        file_path = os.path.join('static','uploads', filename)
        last_uploaded = file_path
        file.save(file_path)
        return make_response(jsonify({'message': 'File uploaded successfully','file_path': f'http://127.0.0.1:5000{url_for('static', filename=f'uploads/{filename}')}'}),200)

@app.route('/generate/<name>',methods=['get'])
def generate(name):
    fileName = os.path.join(BASE_PATH,'static','uploads',name)
    dehaze_name = name.split('.')[0]
    (ssim, psnr) = generateDehazeImage(fileName,dehaze_name)
    ssim = round(float(ssim),2)
    psnr = round(float(psnr),2)

    # Create JSON response with converted values
    response_data = {
    'file_path': f'http://127.0.0.1:5000{url_for('static', filename=name)}',
    'ssim': ssim,
    'psnr': psnr
    }
    return make_response(jsonify({'file_path': f'http://127.0.0.1:5000{url_for('static', filename=f'generated/{name}')}','ssim': ssim,'psnr':psnr}),200)

if __name__ == '__main__':
    app.run(debug=True)
