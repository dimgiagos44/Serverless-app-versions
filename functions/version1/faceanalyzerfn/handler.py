import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import io 
from PIL import Image 
import urllib3
from minio import Minio
import json
import cv2
import numpy as np
import requests
from tensorflow.keras.models import model_from_json
import numpy as np

class FacialExpressionModel(object):

    EMOTIONS_LIST = ["Angry", "Disgust", "Fear", "Happy", "Neutral","Sad","Surprised"]
    
    def __init__(self, model_json_file, model_weights_file):
        with open(model_json_file,"r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        self.loaded_model.load_weights(model_weights_file)

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]

FACE_CLASSIFIER_XML = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
facec = cv2.CascadeClassifier(FACE_CLASSIFIER_XML)
model = FacialExpressionModel("/home/app/function/model.json", "/home/app/function/model_weights.h5")
#font = cv2.FONT_HERSHEY_SIMPLEX
font = cv2.FONT_HERSHEY_PLAIN



client = Minio(
        "10.102.201.185:80",
        access_key="7bde2761-ccfe-4c09-9018-15198e31caaf",
        secret_key="7ed4980e-9480-4eb0-a507-fe44f60c4470",
        secure=False,
        http_client=urllib3.PoolManager(cert_reqs="CERT_NONE")
)

def download_stream(bucket, file):
        data = client.get_object(bucket, file)
        return data.read()

def process(image_bytes):
        image = np.asarray(Image.open(io.BytesIO(image_bytes)))
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(image_gray, 1.3, 5)
        preds = []
        for (x, y, w, h) in faces:
            fc = image_gray[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            preds.append(pred)
            
        return preds

def handle(req):

    input = json.loads(req)
    input_bucket = input['input-bucket']
    key = input['key']
    key = key.split('\n')[0]
    image_bytes = download_stream(input_bucket, key)
    preds = process(image_bytes)
    result = {
        'predictions': preds,
        'bucket': input_bucket,
        'key': key
    }

    url = 'https://en18ywg3vg3z8.x.pipedream.net/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = requests.post(url, json.dumps(result), headers=headers)

    return json.dumps(result)