import json
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import random

action = './action.log'
action_content = open(action, 'r')

action2 = open('action_log2.log', 'w')

line_count = 1
for line in action_content.readlines():
    if line_count <= 50:
        action2.write(line)
        line_count += 1
        continue
    
    if line_count == 51:
        details = line.split('time:')
        time0 = int(details[1])

    if line_count > 50 and line_count <= 100:
        line_count += 1
        continue

    if line_count > 100 and line_count <= 150:
        details = line.split("time:")[0]
        time = time0 + random.randrange(17, 80)
        time0 = time
        details = details + 'time:' + str(time)
        action2.write(details + "\n")
        line_count += 1

    if line_count > 150 and line_count <= 200:
        line_count += 1
        continue

    if line_count == 201:
        details = line.split('time:')
        time0 = int(details[1])

    if line_count > 200 and line_count <= 250:
        details = line.split("time:")[0]
        time = time0 + random.randrange(17, 80)
        time0 = time
        details = details + 'time:' + str(time)
        action2.write(details + "\n")
        line_count += 1
    
    if line_count > 250 and line_count <= 300:
        line_count += 1
        continue

    if line_count == 301:
        details = line.split('time:')
        time0 = int(details[1])

    if line_count > 300 and line_count <= 350:
        details = line.split("time:")[0]
        time = time0 + random.randrange(17, 80)
        time0 = time
        details = details + 'time:' + str(time)
        action2.write(details + "\n")
        line_count += 1

    if line_count > 350 and line_count <= 400:
        line_count += 1
        continue

    if line_count == 401:
        details = line.split('time:')
        time0 = int(details[1])

    if line_count > 400 and line_count <= 450:
        details = line.split("time:")[0]
        time = time0 + random.randrange(17, 80)
        time0 = time
        details = details + 'time:' + str(time)
        action2.write(details + "\n")
        line_count += 1

