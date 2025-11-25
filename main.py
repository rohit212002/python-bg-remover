"""
Python Background Removal Microservice
Install: pip install flask rembg pillow flask-cors
Run: python bg_service.py
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import requests

app = Flask(__name__)
CORS(app)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Check if URL or file upload
        if 'url' in request.json:
            # Download from URL
            response = requests.get(request.json['url'])
            input_image = Image.open(io.BytesIO(response.content))
        elif 'image' in request.files:
            # Direct file upload
            input_image = Image.open(request.files['image'])
        else:
            return jsonify({'error': 'No image provided'}), 400

        # Remove background
        output_image = remove(input_image)
        
        # Convert to bytes
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)