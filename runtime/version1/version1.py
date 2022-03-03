#import grequests
import requests
import time
import urllib
import json
import sys
from datetime import datetime


start = time.time()

# GLOBALS
#step = 40
#frames_number = 16
step = int(sys.argv[1])
frames_number = int(sys.argv[2])

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
jpg_add = '.' + str(step) + '.jpg'


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
headers_facedetector = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'https://en18ywg3vg3z8.x.pipedream.net/'}
#rs = (grequests.post(facedetectorfn_url_async, data = json.dumps({"input-bucket": "image-output", "key": str(i) + jpg_add}), headers = headers_facedetector) for i in range(frames_number))
#print(grequests.map(rs))
facedetector_results = []
for i in range(frames_number):
    name = str(i) + jpg_add
    facedetectorfn_data = {"input-bucket": "image-output", "key": name}
    facedetectorfn_req = requests.post(facedetectorfn_url_async, json.dumps(facedetectorfn_data), headers=headers_facedetector)
    facedetector_results.append(facedetectorfn_req.content)
print(facedetector_results)

# FACEANALYZER, MOBILENET PART
print('Executing the faceanalyzer and mobilenet...')

face_exists_array_7 = ['f', 't', 'f', 'f', 't', 'f', 'f']
face_exists_array_16 = ['t', 't', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f']
face_exists_array_32 = ['t', 't', 'f', 't', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f']
face_exists_array_65 = ['f', 't',  't', 't', 't', 'f', 't', 't', 'f', 't', 'f',  't', 't', 't', 'f', 'f', 'f', 't', 't', 'f', 'f',  'f',  't',  'f', 'f', 'f', 'f', 'f', 'f', 't', 't', 'f', 't', 'f', 't', 'f', 'f', 'f',  'f', 'f', 'f', 't', 't', 't', 't',  't', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']

if (frames_number == 7):
    face_exists = face_exists_array_7
    time.sleep(3.5)
    print('sleeping')
elif (frames_number == 16):
    face_exists = face_exists_array_16
    time.sleep(6.8)
    print('sleeping')
elif (frames_number == 32):
    face_exists = face_exists_array_32
    time.sleep(14.5)
    print('sleeping')
elif (frames_number == 65):
    face_exists = face_exists_array_65
    time.sleep(29)
    print('sleeping')
else: 
    print('Error at faceanalyzer-mobilenet step!') 

i = 0
faceanalyzer_results = []
mobilenet_results = []
for flag in face_exists:
    if (flag == 't'):
        name = str(i) + jpg_add
        faceanalyzer_data = {"input-bucket": "image-output", "key": name}
        faceanalyzer_req = requests.post(faceanalyzer_url_async, json.dumps(faceanalyzer_data), headers=headers)
        faceanalyzer_results.append(faceanalyzer_req.content)
        i = i + 1
    else:
        name = str(i) + jpg_add
        mobilenet_data = {"input-bucket": "image-output", "key": name}
        mobilenet_req = requests.post(mobilenet_url_async, json.dumps(mobilenet_data), headers=headers)
        mobilenet_results.append(mobilenet_req.content)
        i = i + 1

print('faceanalyzer results: ', faceanalyzer_results)
print('mobilenet results: ', mobilenet_results)

end = time.time()
print(f'Runtime of the execution took {end - start}')