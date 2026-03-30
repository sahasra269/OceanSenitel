from flask import Flask, request, jsonify
import classify
import base64
import firebase
import env
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Health check
@app.route('/status')
def health_check():
    return 'Running!'

@app.route('/detect', methods=["POST", "OPTIONS"])
def detect():
    if request.method == "OPTIONS":
        return jsonify({}), 200

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
    result = classify.analyse("temp.png")

    # Add location to result
    result['lat'] = lat
    result['lng'] = lng

    # Push to Firebase
    try:
        db = firebase.Firebase()
        db.authenticate()
        db.push(result)
        print("Updated Firebase.")
    except Exception as e:
        print("Firebase error:", e)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)