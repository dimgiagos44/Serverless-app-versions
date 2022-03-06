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
framerfn_url = 'http://localhost:8080/function/framerfn'
framerfn_url_async = 'http://localhost:8080/async-function/framerfn'

facedetectorfn_url = 'http://localhost:8080/function/facedetectorfn'
facedetectorfn_url_async = 'http://localhost:8080/async-function/facedetectorfn'

facedetectorfn2_url = 'http://localhost:8080/function/facedetectorfn2'
facedetectorfn2_url_async = 'http://localhost:8080/async-function/facedetectorfn2'

# REQUEST INFORMATION
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
headers_facedetector = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'https://en18ywg3vg3z8.x.pipedream.net/'}
jpg_add = '.' + str(step) + '.jpg'

'''
# FRAMERFN PART
print('Executing the framer...')
framerfn_data = {"output_bucket": "image-output", "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", 
                "seconds": step, "lower_limit": 0, "upper_limit": "full"}
framerfn_req = requests.post(framerfn_url, json.dumps(framerfn_data), headers=headers)
print(str(framerfn_req.content))
'''

# FACEDETECTORFN PART
print('Executing the facedetector...')
facedetector_results = []
for i in range(frames_number):
    name = str(i) + jpg_add
    facedetectorfn_data = {"input-bucket": "image-output", "key": name}
    facedetectorfn_req = requests.post(facedetectorfn_url_async, json.dumps(facedetectorfn_data), headers=headers_facedetector)
    facedetector_results.append(facedetectorfn_req.content)
print(facedetector_results)

end = time.time()
print(f'Runtime of the execution took {end - start}')