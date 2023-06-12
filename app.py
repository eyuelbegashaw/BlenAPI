from ultralytics import YOLO
import numpy as np
from PIL import Image
import easyocr
import matplotlib.pyplot as plt


app = Flask(__name__)
model = YOLO("best.pt")

@app.route("/")
def check():
    return jsonify({"message":"hello world"})


@app.route("/cardRecognition")
def hello_world():
    if 'image' not in request.files:
        return "No image found in request", 400

    image = request.files['image']
    if image.filename == '':
        return "Empty image filename", 400

    #prediction using model
    results = model.predict(image)

    #coordinates of the card
    x = results[0].boxes.data[0]
    x1 = x[0].item()
    y1 = x[1].item()
    x2 = x[2].item()
    y2 = x[3].item()

    #crop the detected image
    cropped_image = image.crop((x1, y1, x2, y2))

    #Perform ocr on the cropped image
    reader = easyocr.Reader(['en'] , gpu=False)
    arrayImage = np.asarray(cropped_image)
    result = reader.readtext(arrayImage, allowlist ='0123456789' ,detail = 0)
    cleanedNumbers = "".join(result)

    return ({"cardNumbers" : cleanedNumbers}) 