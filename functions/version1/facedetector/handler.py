import cv2
import urllib3
import json
from minio import Minio
import uuid
import numpy as np
from PIL import Image
from io import BytesIO


client = Minio(
        "10.102.201.185:80",
        access_key="7bde2761-ccfe-4c09-9018-15198e31caaf",
        secret_key="7ed4980e-9480-4eb0-a507-fe44f60c4470",
        secure=False,
        http_client=urllib3.PoolManager(cert_reqs="CERT_NONE")
)

FACE_CLASSIFIER_XML = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'

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


def handle(req):

    input = json.loads(req)
    input_bucket = input['input-bucket']
    #output_bucket = input['output-bucket']
    key = input['key']
    key = key.split('\n')[0]

    image_bytes = download_stream(input_bucket, key)
    faceExists = face_detect(image_bytes)

    result = {
        'faceExists': faceExists
    }

    return json.dumps(result)
