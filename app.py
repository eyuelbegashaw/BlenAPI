from ultralytics import YOLO
import numpy as np
from PIL import Image
import easyocr
import matplotlib.pyplot as plt
from flask import Flask ,jsonify , request , send_file
from flask_cors import CORS
import base64
import io
import base64

app = Flask(__name__)
CORS(app) 

@app.route("/hello" , methods=['POST'])
def hello_world():
    try: 
        model = YOLO("best.pt")
        print("welcome")
        if 'image' not in request.files:
            return "No image found in request", 400
        
        image = request.files['image']
        original_image = image
        print("Image received successfully")
        if image.filename == '':
            return "Empty image filename", 400

        image = Image.open(image)
        print("pillow load success")

        #prediction using model
        results = model.predict(image)
        print(results)
        #coordinates of the card
        x = results[0].boxes.data[0]
        x1 = x[0].item()
        y1 = x[1].item()
        x2 = x[2].item()
        y2 = x[3].item()

        print("coordinates received")
        print(x1)


        #crop the detected image
        cropped_image = image.crop((x1, y1, x2, y2))

        cropped_image.save('cropped_image.jpg')
    
        # Return the cropped image as a response
        return send_file('cropped_image.jpg', mimetype='image/jpeg')
    except Exception as error:
        print("An exception occurred:", error) 


@app.route("/")
def check():
    return jsonify({"message":"hello world"})

@app.route("/boom")
def imageReturn():
    return send_file('cropped_image.jpg', mimetype='image/jpeg')

    