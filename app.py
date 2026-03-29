from flask import Flask, request, jsonify
import classify
import base64
import firebase
import env
from flask_cors import CORS

# Instantiate Flask
app = Flask(__name__)
CORS(app)  # Allow React frontend to call this API


# Health check
@app.route('/status')
def health_check():
    return 'Running!'


# Performing image recognition on image sent as JSON via POST
# Expected payload: { "image": "<base64string>", "lat": 12.34, "lng": 56.78 }
@app.route('/detect', methods=["POST"])
def detect():
    data = request.get_json()

    # Decode image
    imgdata = base64.b64decode(data['image'])
    with open("temp.png", 'wb') as f:
        f.write(imgdata)

    print("Successfully received image")

    # Get GPS coordinates if provided
    lat = data.get('lat', None)
    lng = data.get('lng', None)

    # Classify image
    result = classify.an

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)