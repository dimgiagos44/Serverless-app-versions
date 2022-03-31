#import grequests
import os
import subprocess
import requests
import time
import urllib
import json
import sys
from datetime import datetime


start = time.time()
now0 = datetime.now()
started_time = now0.strftime("%H:%M:%S")
print("Started time =", started_time)

# GLOBALS
step = int(sys.argv[1])
frames_number = int(sys.argv[2])

# FUNCTION URLS
framerfn_url = 'http://localhost:8080/function/framerfn'
framerfn_url_async = 'http://localhost:8080/async-function/framerfn'

facedetectorfn_url = 'http://localhost:8080/function/facedetectorfn'
facedetectorfn_url_async = 'http://localhost:8080/async-function/facedetectorfn'

facedetectorfn2_url = 'http://localhost:8080/function/facedetectorfn2'
facedetectorfn2_url_async = 'http://localhost:8080/async-function/facedetectorfn2'

faceanalyzer_url = 'http://localhost:8080/function/faceanalyzer'
faceanalyzer_url_async = 'http://localhost:8080/async-function/faceanalyzer'

mobilenet_url = 'http://localhost:8080/function/mobilenet'
mobilenet_url_async = 'http://localhost:8080/async-function/mobilenet'

# REQUEST INFORMATION
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
headers_facedetector = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'https://en18ywg3vg3z8.x.pipedream.net/'}
headers_facedetector_yes = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'http://gateway:8080/async-function/faceanalyzerfn'}
headers_facedetector_no = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'http://gateway:8080/async-function/mobilenetfn'}
jpg_add = '.' + str(step) + '.jpg'

'''
# FRAMERFN PART
print('Executing the framer...')
framerfn_data = {"output_bucket": "image-output", "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", 
                "seconds": step, "lower_limit": 0, "upper_limit": "full"}
framerfn_req = requests.post(framerfn_url, json.dumps(framerfn_data), headers=headers)
print(str(framerfn_req.content))
'''
# FACEDETECTOR-FACEANALYZER-MOBILENET PART
print('Executing the facedetector-faceanalyzer-mobilenet...')
face_exists_array_7 = ['f', 't', 'f', 'f', 't', 'f', 'f']
face_exists_array_16 = ['t', 't', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f']
face_exists_array_32 = ['t', 't', 'f', 't', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f']
face_exists_array_65 = ['f', 't',  't', 't', 't', 'f', 't', 't', 'f', 't', 'f',  't', 't', 't', 'f', 'f', 'f', 't', 't', 'f', 'f',  'f',  't',  'f', 'f', 'f', 'f', 'f', 'f', 't', 't', 'f', 't', 'f', 't', 'f', 'f', 'f',  'f', 'f', 'f', 't', 't', 't', 't',  't', 'f', 'f', 'f', 't', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f']

if (frames_number == 7):
    face_exists = face_exists_array_7
    time_interval = '11'
elif (frames_number == 16):
    face_exists = face_exists_array_16
    time_interval = '25'
elif (frames_number == 32):
    face_exists = face_exists_array_32
    time_interval = '48'
elif (frames_number == 65):
    face_exists = face_exists_array_65
    time_interval = '100'
else: 
    print('Error at faceanalyzer-mobilenet step!')

i = 0
for flag in face_exists:
    name = str(i) + jpg_add
    facedetector_data = {"input-bucket": "image-output", "key": name}
    if (flag == 't'):
        faceanalyzer_req = requests.post(facedetectorfn2_url_async, json.dumps(facedetector_data), headers=headers_facedetector_yes)
        i = i + 1
    else:
        mobilenet_req = requests.post(facedetectorfn2_url_async, json.dumps(facedetector_data), headers=headers_facedetector_no)
        i = i + 1

frames_received = -1
command_received = 0
started = False
finished = True
start_now = datetime.utcnow()
start_now_str = start_now.isoformat("T") + "Z"
#print('start_now_str = ', start_now_str)


check_start_command = 'kubectl logs gateway-7ff44f68cb-x5lq9 gateway -n openfaas --since-time=' + start_now_str + '| grep -e "/function/mobilenetfn" -e "/function/faceanalyzerfn" | tail -n 1 | wc -l'
while (command_received < 1):
    command_received = int(subprocess.getoutput(check_start_command))

started = True
count_frames_command = 'kubectl logs gateway-7ff44f68cb-x5lq9 gateway -n openfaas --since-time=' + start_now_str + '| grep -e "/function/mobilenetfn" -e "/function/faceanalyzerfn" | tail -n' + str(frames_number) + ' | wc -l'
while (frames_received < frames_number - 2):
    time.sleep(0.4)
    frames_received = int(subprocess.getoutput(count_frames_command))
    if (frames_received == 0): 
        finished = False
        break

if finished == True:
    print('finally frames_received =', frames_received)
else: 
    print('Process not finished..')

end = time.time()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f'Runtime of the execution took {end - start}')
print("Current time =", current_time)