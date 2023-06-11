from flask import Flask , jsonify, request
import cv2
import easyocr
import subprocess
import shutil
import os 

app = Flask(__name__)

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

    save_path = 'test/images/' + image.filename
    image.save(save_path)
    print(image.filename)
  
   
    command = [
    'yolo',
    'task=detect',
    'mode=predict',
    'model=best.pt',
    'conf=0.25',
    'source=test/images',
    'save_crop'
     ]
    subprocess.run(command)

    cropedImage = cv2.imread(f"./runs/detect/predict/crops/Card/{image.filename}")
    reader = easyocr.Reader(['en'] , gpu=False)
    result = reader.readtext(cropedImage, allowlist ='0123456789' ,detail = 0)
    cleanedNumbers = "".join(result)
    print(image.filename)
    test_path = f'./test/images/{image.filename}'  
    run_path = './runs'
    try:
        os.remove(test_path)
        shutil.rmtree(run_path)
        print("Folder deleted successfully.")
    except OSError as e:
        print(f"Error: {e.strerror}")

    return jsonify({ "message" :  cleanedNumbers})
