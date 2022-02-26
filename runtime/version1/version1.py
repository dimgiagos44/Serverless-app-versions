import requests
import time
import urllib
import json

# GLOBALS
step = 40
frames_number = 16

# FUNCTION URLS
framerfn_url = 'http://localhost:8080/function/framerfn'
framerfn_url_async = 'http://localhost:8080/async-function/framerfn'

facedetectorfn_url = 'http://localhost:8080/function/facedetectorfn'
facedetectorfn_url_async = 'http://localhost:8080/async-function/facedetectorfn'

faceanalyzer_url = 'http://localhost:8080/function/faceanalyzer'
faceanalyzer_url_async = 'http://localhost:8080/async-function/faceanalyzer'

mobilenet_url = 'http://localhost:8080/function/mobilenet'
mobilenet_url_async = 'http://localhost:8080/async-function/mobilenet'

# REQUEST INFORMATION
headers = {'Content-Type': 'application/x-www-form-urlencoded'}


# FRAMERFN PART
print('Executing the framer...')

framerfn_data = {"output_bucket": "image-output", "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", 
                "seconds": step, "lower_limit": 0, "upper_limit": "full"}
framerfn_req = requests.post(framerfn_url, json.dumps(framerfn_data), headers=headers)
print(str(framerfn_req.content))
#frame_names = ['0.90.jpg', '1.90.jpg', '2.90.jpg', '3.90.jpg', '4.90.jpg', '5.90.jpg', '6.90.jpg']
#frame_names = ['0.40.jpg', '0.40.jpg', '0.40.jpg', '0.40.jpg', '0.40.jpg', '0.40.jpg', '0.40.jpg', '0.40.jpg', '0.40.jpg']

# FACEDETECTORFN PART
print('Executing the facedetector...')
facedetector_results = []
for i in range(frames_number):
    name = str(i) + '.' + str(step) + '.jpg'
    facedetectorfn_data = {"input-bucket": "image-output", "key": name}
    facedetectorfn_req = requests.post(facedetectorfn_url_async, json.dumps(facedetectorfn_data), headers=headers)
    facedetector_results.append(facedetectorfn_req.content)
print(facedetector_results)

# FACEANALYZER, MOBILENET PART
print('Executing the faceanalyzer...')

