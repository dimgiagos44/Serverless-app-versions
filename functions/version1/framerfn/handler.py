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


def download_stream(bucket, file):
        data = client.get_object(bucket, file)
        return data.read()

def upload_stream(bucket, file, bytes_data):
        client.put_object(bucket, file, bytes_data, bytes_data.getbuffer().nbytes)
        return 

def process(image_array):
        image = Image.fromarray(image_array)
        out = io.BytesIO()
        image.save(out, format='jpeg')
        out.seek(0)
        return out

def handle(req):

    input = json.loads(req)
    #input_bucket = input['input-bucket']
    output_bucket = input['output_bucket']
    url = input['url']
    seconds = input['seconds']
    lower_limit = input['lower_limit'] #from here (seconds)
    upper_limit = input['upper_limit'] #until here (seconds)
    url = url.split('\n')[0] # e.g key = sample2.mp4

    vidcap = cv2.VideoCapture(url)
    success, image = vidcap.read()
    successOpen = success
    #seconds = 20
    frame_num = 0
    s = '.' + str(seconds) + '.jpg'
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
        
        if success == False:
                break

        if frameId < lower_limit_frames:
                continue

        if frameId > upper_limit_frames:
                break

        if frameId % multiplier == 0:
                image_file = process(image)
                name = str(frame_num) + s
                upload_stream(output_bucket, name, image_file)
                key_names.append(name)
                frame_num += 1
        
    
    vidcap.release()
    result = {
            'output_bucket': output_bucket,
            'frame_names': key_names,
            'frame_number': frame_num,
            'request_status': successOpen
    }

    return json.dumps(result)
