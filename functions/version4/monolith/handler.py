import io
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
from minio import Minio
import urllib3
import json
import math
import uuid
from PIL import Image
from io import BytesIO
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.models import model_from_json

client = Minio(
        "10.102.201.185:80",
        access_key="7bde2761-ccfe-4c09-9018-15198e31caaf",
        secret_key="7ed4980e-9480-4eb0-a507-fe44f60c4470",
        secure=False,
        http_client=urllib3.PoolManager(cert_reqs="CERT_NONE")
)

def unique_name(name):
        name, extension = name.split('.')
        return '{name}.{random}.{extension}'.format(
                    name=name,
                    extension=extension,
                    random=str(uuid.uuid4()).split('-')[0]
                )

def download_stream(bucket, file):
        data = client.get_object(bucket, file)
        return data.read()

def upload_stream(bucket, file, bytes_data):
        key_name = unique_name(file)
        client.put_object(bucket, key_name, bytes_data, bytes_data.getbuffer().nbytes)
        return key_name

############## FRAMER PART ##################
def framer_process(image_array):
        image = Image.fromarray(image_array)
        out = io.BytesIO()
        image.save(out, format='jpeg')
        out.seek(0)
        return out


############# FACE DETECTOR PART ############
FACE_CLASSIFIER_XML = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'

def face_detect(image_bytes):
    image = np.asarray(Image.open(BytesIO(image_bytes)))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frontalface_cascade = cv2.CascadeClassifier(FACE_CLASSIFIER_XML)
    facerect = frontalface_cascade.detectMultiScale(
        image_gray, scaleFactor=1.1, 
        minNeighbors=1, minSize=(1, 1)
    )

    empty_tuple = tuple()
    if (facerect == empty_tuple):
        print('Face(s) dont exist here.')
        return False
    else:
        print('Face(s) exist here.')
        return True

############# Inference part ###############
class FacialExpressionModel(object):

    EMOTIONS_LIST = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprised"]
    
    def __init__(self, model_json_file, model_weights_file):
        with open(model_json_file,"r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        self.loaded_model.load_weights(model_weights_file)

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]

def process(image_bytes):
    FACE_CLASSIFIER_XML = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
    facec = cv2.CascadeClassifier(FACE_CLASSIFIER_XML)
    model = FacialExpressionModel("/home/app/function/model.json", "/home/app/function/model_weights.h5")
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

model = ResNet50(weights='imagenet')
def classify(img_resized):
    x = image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    return predictions

def handle(req):

    input = json.loads(req)
    output_bucket = input['output_bucket']
    input_bucket = output_bucket
    url = input['url']
    seconds = input['seconds']
    lower_limit = input['lower_limit'] #from here (seconds)
    upper_limit = input['upper_limit'] #until here (seconds)
    url = url.split('\n')[0] # e.g key = sample2.mp4

    vidcap = cv2.VideoCapture(url)
    success, image = vidcap.read()
    successOpen = success
    frame_num = 0
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    if upper_limit == 'full':
        frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT) 
        duration = frame_count/fps
        duration = math.floor(duration)
        upper_limit = duration

    lower_limit_frames = fps * lower_limit
    upper_limit_frames = fps * upper_limit

    multiplier = fps * seconds
    key_names = []
    
    while(success):
        frameId = int(round(vidcap.get(1)))
        success, image = vidcap.read()

        if frameId < lower_limit_frames:
                continue

        if frameId > upper_limit_frames:
                break

        if frameId % multiplier == 0:
                image_file = framer_process(image)
                key_name = upload_stream(output_bucket, 'frame.jpg', image_file)
                key_names.append(key_name)
                frame_num += 1

    vidcap.release()
    result0 = {
            'output_bucket': output_bucket,
            'frame_names': key_names,
            'frame_number': frame_num,
            'request_status': successOpen
    }

    final_results = []
    for key in key_names:
        image_bytes = download_stream(input_bucket, key)
        faceExists = face_detect(image_bytes)

        if faceExists == True:
            preds = process(image_bytes)
            temp = {
                'predictions': preds,
                'bucket': input_bucket,
                'key': key
            }
            final_results.append(temp)
        else:
            img = Image.open(io.BytesIO(image_bytes))
            img_resized = img.resize((224, 224))
            predictions = classify(img_resized)
            results = decode_predictions(predictions, top=3)[0]
            predictions2 = [str(results[0][1]), str(results[1][1]), str(results[2][1])]
            temp = {
                'predictions': predictions2,
                'bucket': input_bucket,
                'key': key
            }
            final_results.append(temp)

    return json.dumps(final_results)