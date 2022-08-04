import json
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import random

state = './state.log'
state_content = open(state, 'r')

state2 = open('state_log2.log', 'w')

action = './action.log'
action_content = open(action, 'r')
times = []
for line in action_content.readlines():
    time = line.split("time:")[1]
    times.append(int(time))

line_count = 1
i = 0
for line in state_content.readlines():
    if line_count <= 50:
        state2.write(line)
        line_count += 1
        continue

    if line_count > 50 and line_count <= 100:
        line_count += 1
        continue

    if line_count > 100 and line_count <= 150:
        details = line.split("time:")[0]
        details = details + str(times[i])
        state2.write(details + "\n")
        line_count += 1

    if line_count > 150 and line_count <= 200:
        line_count += 1
        continue

    if line_count > 200 and line_count <= 250:
        details = line.split("time:")[0]
        details = details + str(times[i])
        state2.write(details + "\n")
        line_count += 1
    
    if line_count > 250 and line_count <= 300:
        line_count += 1
        continue

    if line_count > 300 and line_count <= 310:
        details = line.split("time:")[0]
        details = details + str(times[i])
        state2.write(details + "\n")
        line_count += 1

    if line_count > 310 and line_count <= 360:
        line_count += 1
        continue


    if line_count > 360 and line_count <= 400:
        details = line.split("time:")[0]
        details = details + str(times[i])
        state2.write(details + "\n")
        line_count += 1
    
    i += 1

