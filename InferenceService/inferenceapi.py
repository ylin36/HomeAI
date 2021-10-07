"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
from logging import debug
import torch
import jwt
import datetime
from PIL import Image
from flask import Flask, request, jsonify, make_response
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'w6iq01EhWRrsZgDD2wTQeQwbdJrKU2Rny3jPuM6vUTnRCtIYcOF9mKwms46l2HI'

DETECTION_URL = "/v1/object-detection/yolov5s"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Missing token'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)
    return decorated

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route(DETECTION_URL, methods=["POST"])
@token_required
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=1000)  
        return results.pandas().xyxy[0].to_json(orient="records")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    app.run(host="0.0.0.0", port=args.port, debug=True)  # debug=True causes Restarting with stat
