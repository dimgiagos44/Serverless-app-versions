import io
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import Image 
import urllib3
from minio import Minio
import json
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

model = ResNet50(weights='imagenet')

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

def classify(img_resized):
    x = image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    return predictions


def handle(req):
    input = json.loads(req)
    input_bucket = input['input-bucket']
    key = input['key']
    key = key.split('\n')[0]

    img = download_stream(input_bucket, key)
    img = Image.open(io.BytesIO(img))
    img_resized = img.resize((224, 224))
    predictions = classify(img_resized)

    results = decode_predictions(predictions, top=3)[0]
    print(results)
    results2 = {
        "first": results[0][1],
        "second": results[1][1],
        "third": results[2][1],
        "bucket": input_bucket,
        "key": key
    }

    return json.dumps(results2)

