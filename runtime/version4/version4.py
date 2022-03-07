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
monolith2_url = 'http://localhost:8080/function/monolith2'
monolith2_url_async = 'http://localhost:8080/async-function/monolith2'


# REQUEST INFORMATION
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
headers_facedetector = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Callback-Url': 'https://en18ywg3vg3z8.x.pipedream.net/'}
jpg_add = '.' + str(step) + '.jpg'


# MONOLITH PART
print('Executing the monolith2...')
monolith2_data = {"output_bucket": "image-output", "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", 
                "seconds": step, "lower_limit": 0, "upper_limit": "full"}
monolith2_req = requests.post(monolith2_url, json.dumps(monolith2_data), headers=headers)
print(str(monolith2_req.content))

end = time.time()
print(f'Runtime of the execution took {end - start}')