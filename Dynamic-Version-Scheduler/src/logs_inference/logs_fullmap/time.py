import json
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import random

time = './time.log'
time_content = open(time, 'r')

time2 = open('time_log2.log', 'w')

action = './action.log'
action_content = open(action, 'r')
times = []
for line in action_content.readlines():
    time = line.split("time:")[1]
    times.append(int(time))

line_count = 1
i = 0
for line in time_content.readlines():
    if line_count <= 50:
        time2.write(line)
        line_count += 1
        continue

    if line_count > 50 and line_count <= 100:
        line_count += 1
        continue

    if line_count > 100 and line_count <= 150:
        details_time = line.split("time:")[0]
        latency = line.split('latency: ')[1]
        details = details_time + 'time:' + str(times[i]) + ' | latency:' + latency
        time2.write(details)
        line_count += 1

    if line_count > 150 and line_count <= 200:
        line_count += 1
        continue

    if line_count > 200 and line_count <= 250:
        details_time = line.split("time:")[0]
        latency = line.split('latency: ')[1]
        details = details_time + 'time:' + str(times[i]) + ' | latency:' + latency
        time2.write(details)
        line_count += 1
    
    if line_count > 250 and line_count <= 300:
        line_count += 1
        continue

    if line_count > 300 and line_count <= 310:
        details_time = line.split("time:")[0]
        latency = line.split('latency: ')[1]
        details = details_time + 'time:' + str(times[i]) + ' | latency:' + latency
        time2.write(details)
        line_count += 1

    if line_count > 310 and line_count <= 360:
        line_count += 1
        continue


    if line_count > 360 and line_count <= 400:
        details_time = line.split("time:")[0]
        latency = line.split('latency: ')[1]
        details = details_time + 'time:' + str(times[i]) + ' | latency:' + latency
        time2.write(details)
        line_count += 1
    
    i += 1

