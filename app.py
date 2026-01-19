from flask import Flask, request, jsonify
import face_recognition
import base64
import requests
from io import BytesIO
import numpy as np
import cv2

app = Flask(__name__)

# -------- BASE64 → OPENCV --------
def base64_to_image(base64_str):
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        img_bytes = base64.b64decode(base64_str)
        img_array = np.frombuffer(img_bytes, np.uint8)

        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            return None

        # BGR → RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

    except Exception as e:
        print("BASE64 ERROR:", e)
        return None


# -------- URL → OPENCV --------
def url_to_image(url):
    try:
        res = requests.get(url)
        img_array = np.frombuffer(res.content, np.uint8)

        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            return None

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

    except Exception as e:
        print("URL ERROR:", e)
        return None


# -------- API --------
@app.route("/verify-face", methods=["POST"])
def verify():

    data = request.json

    live_img = base64_to_image(data.get("live"))
    stored_img = url_to_image(data.get("stored"))

    if live_img is None or stored_img is None:
        return jsonify({
            "success": False,
            "msg": "Invalid image data"
        })

    try:
        enc1 = face_recognition.face_encodings(live_img)
        enc2 = face_recognition.face_encodings(stored_img)

    except Exception as e:
        print("ENCODING ERROR:", e)
        return jsonify({
            "success": False,
            "msg": "Encoding failed"
        })

    if len(enc1)==0 or len(enc2)==0:
        return jsonify({
            "success": False,
            "msg": "Face not detected"
        })

    distance = face_recognition.face_distance(
        [enc2[0]], enc1[0]
    )[0]

    match = distance < 0.45

    return jsonify({
        "success": bool(match),
        "distance": float(distance)
    })


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)