import cv2
import numpy as np
import math
from minio import Minio
import urllib3
import json
import uuid
import io
from PIL import Image

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

def process(image_array):
        image = Image.fromarray(image_array)
        out = io.BytesIO()
        image.save(out, format='jpeg')
        out.seek(0)
        return out

def handle(req):

    input = json.loads(req)
    #input_bucket = input['input-bucket']
    output_bucket = input['output-bucket']
    url = input['url']
    seconds = input['seconds']
    url = url.split('\n')[0] # e.g key = sample2.mp4

    vidcap = cv2.VideoCapture(url)
    success, image = vidcap.read()
    successOpen = success
    #seconds = 20
    frame_num = 0
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    multiplier = fps * seconds
    key_names = []
    
    while(success):
        frameId = int(round(vidcap.get(1)))
        success, image = vidcap.read()

        if frameId % multiplier == 0:
                image_file = process(image)
                key_name = upload_stream(output_bucket, 'frame.jpg', image_file)
                key_names.append(key_name)
                frame_num += 1
        
    
    vidcap.release()
    result = {
            'output-bucket': output_bucket,
            'frame-names': key_names,
            'frame-number': frame_num,
            'request-status': successOpen
    }

    return json.dumps(result)
