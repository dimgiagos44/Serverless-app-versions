import json
from statistics import mean
import matplotlib.pyplot as plt

#version = '05_20_18'
reward_str = '/home/dgiagos/openfaas/Serverless-app-versions/Dynamic-Version-Scheduler/src/logs/'
reward_str2 = '/reward.log'
time_str = '/home/dgiagos/openfaas/Serverless-app-versions/Dynamic-Version-Scheduler/src/logs/'
time_str2 = '/time.log'
action_str = '/home/dgiagos/openfaas/Serverless-app-versions/Dynamic-Version-Scheduler/src/logs/'
action_str2 = '/action.log'

#reward_path = reward_str + version + reward_str2
#rewards = open(reward_path, 'r')
#reward_data = []
reward_order = ['reward', 'input', 'time']

#time_path = time_str + version + time_str2
#times = open(time_path, 'r')
#time_data = []
time_order = ['time_quotient', 'input', 'time']

#action_path = action_str + version + action_str2
#actions = open(action_path, 'r')
#action_data = []
action_order = ['action', 'input', 'time']

def mergeResults(c, versions):
    if c == 't':
        time_data = []
        for version in versions:
            times = open(time_str + version + time_str2, 'r')
            for line in times.readlines():
                details = line.split("|")
                details[0] = details[0].split(': ')[1]
                details[1] = details[1].split(': ')[1]
                details[2] = details[2].split(':')[1]
                details = [x.strip() for x in details]
                details[0] = float(details[0])
                details[1] = int(details[1])
                structure = {key:value for key, value in zip(time_order, details)}
                time_data.append(structure)
        return time_data
    elif c == 'a':
        action_data = []
        for version in versions:
            actions = open(reward_str + version + reward_str2, 'r')
            for line in actions.readlines():
                details = line.split("|")
                details[0] = details[0].split(': ')[1]
                details[1] = details[1].split(': ')[1]
                details[2] = details[2].split(':')[1]
                details = [x.strip() for x in details]
                #print(line)
                details[0] = int(float(details[0]))
                details[1] = int(details[1])
                structure = {key:value for key, value in zip(action_order, details)}
                action_data.append(structure)
        return action_data
    elif c == 'r':
        reward_data = []
        for version in versions:
            rewards = open(reward_str + version + reward_str2, 'r')
            for line in rewards.readlines():
                details = line.split("|")
                details[0] = details[0].split(': ')[1]
                details[1] = details[1].split(': ')[1]
                details[2] = details[2].split(':')[1]
                details = [x.strip() for x in details]
                details[0] = float(details[0])
                details[1] = int(details[1])
                structure = {key:value for key, value in zip(reward_order, details)}
                reward_data.append(structure)
        return reward_data
    else:
        return []

def parseRewards(reward_data):
    rewards = ([], [], [], [])
    for reward in reward_data:
        rewards[reward['input'] - 1].append(reward['reward'])
    return rewards

def parseTimes(time_data):
    times = ([], [], [], [])
    for time in time_data:
        times[time['input'] - 1].append(time['time_quotient'])
    return times

def parseActions(action_data):
    actions = ([], [], [], [])
    for action in action_data:
        actions[action['input'] - 1].append(action['action'])
    return actions

#versions = ['05_23_15', '05_23_19', '05_23_21', '05_24_11', '05_24_12']
#versions = ['05_20_15', '05_20_18', '05_23_12']
versions = ['05_31_11', '06_01_09', '06_01_13']

time = mergeResults('t', versions)
time2 = parseTimes(time)

action = mergeResults('a', versions)
action2 = parseActions(action)

reward = mergeResults('r', versions)
reward2 = parseRewards(reward)

figure, axis = plt.subplots(3, 4, figsize=(20, 15))
axis[0, 0].plot(time2[0])
axis[0, 0].set_title('Time Input 0')

axis[0, 1].plot(time2[1])
axis[0, 1].set_title('Time Input 1')

axis[0, 2].plot(time2[2])
axis[0, 2].set_title('Time Input 2')

axis[0, 3].plot(time2[3])
axis[0, 3].set_title('Time Input 3')

axis[1, 0].plot(action2[0])
axis[1, 0].set_title('Action Input 0')

axis[1, 1].plot(action2[1])
axis[1, 1].set_title('Action Input 1')

axis[1, 2].plot(action2[2])
axis[1, 2].set_title('Action Input 2')

axis[1, 3].plot(action2[3])
axis[1, 3].set_title('Action Input 3')

axis[2, 0].plot(reward2[0])
axis[2, 0].set_title('Reward Input 0')

axis[2, 1].plot(reward2[1])
axis[2, 1].set_title('Reward Input 1')

axis[2, 2].plot(reward2[2])
axis[2, 2].set_title('Reward Input 2')

axis[2, 3].plot(reward2[3])
axis[2, 3].set_title('Reward Input 3')

plt.show()
plt.savefig('plot.png')
print(len(action), len(time), len(reward))

#print(mean(time2[0]), mean(time2[1]))