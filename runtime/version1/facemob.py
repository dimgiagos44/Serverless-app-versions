#import grequests
import requests
import time
import urllib
import json
import sys
from datetime import datetime


start = time.time()

# GLOBALS
step = int(sys.argv[1])
frames_number = int(sys.argv[2])

# FUNCTION URLS

faceanalyzer_url = 'http://localhost:8080/function/faceanalyzer'
faceanalyzer_url_async = 'http://localhost:8080/async-function/faceanalyzer'

mobilenet_url = 'http://localhost:8080/function/mobilenet'
mobilenet_url_async = 'http://localhost:8080/async-function/mobilenet'

# REQUEST INFORMATION
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
headers_facedetector = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'https://en18ywg3vg3z8.x.pipedream.net/'}
jpg_add = '.' + str(step) + '.jpg'

# FACEANALYZER, MOBILENET PART
print('Executing the faceanalyzer and mobilenet...')
face_exists_array_7 = ['f', 't', 'f', 'f', 't', 'f', 'f']
face_exists_array_16 = ['t', 't', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f']
face_exists_array_32 = ['t', 't', 'f', 't', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f']
face_exists_array_65 = ['f', 't',  't', 't', 't', 'f', 't', 't', 'f', 't', 'f',  't', 't', 't', 'f', 'f', 'f', 't', 't', 'f', 'f',  'f',  't',  'f', 'f', 'f', 'f', 'f', 'f', 't', 't', 'f', 't', 'f', 't', 'f', 'f', 'f',  'f', 'f', 'f', 't', 't', 't', 't',  't', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']

if (frames_number == 7):
    face_exists = face_exists_array_7
elif (frames_number == 16):
    face_exists = face_exists_array_16
elif (frames_number == 32):
    face_exists = face_exists_array_32
elif (frames_number == 65):
    face_exists = face_exists_array_65
else: 
    print('Error at faceanalyzer-mobilenet step!') 

i = 0
faceanalyzer_results = []
mobilenet_results = []
for flag in face_exists:
    name = str(i) + jpg_add
    data = {"input-bucket": "image-output", "key": name}
    if (flag == 't'):
        faceanalyzer_req = requests.post(faceanalyzer_url_async, json.dumps(data), headers=headers_facedetector)
        faceanalyzer_results.append(faceanalyzer_req.content)
        i = i + 1
    else:
        mobilenet_req = requests.post(mobilenet_url_async, json.dumps(data), headers=headers_facedetector)
        mobilenet_results.append(mobilenet_req.content)
        i = i + 1

print('faceanalyzer results: ', faceanalyzer_results)
print('mobilenet results: ', mobilenet_results)

end = time.time()
print(f'Runtime of the execution took {end - start}')