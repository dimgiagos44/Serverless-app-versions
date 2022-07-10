import json
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

def most_frequent(List):
    return max(set(List), key = List.count)

def my_mean(data):
    n = 0
    mean = 0.0
 
    for x in data:
        n += 1
        mean += (x - mean)/n

    if n < 1:
        return float('nan')
    else:
        return mean


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
            actions = open(action_str + version + action_str2, 'r')
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
    rewards = ([], [], [], [], [])
    for reward in reward_data:
        rewards[reward['input'] - 1].append(reward['reward'])
        if (int(reward['reward']) > 0):
            rewards[4].append(1)
        else:
            rewards[4].append(-1)
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

#versions = ['06_11_20']
#versions = ['06_16_10'] #512... #explor_factor=0.1
#versions = ['06_16_18']
#versions = ['06_17_01']
#versions = ['06_18_14'] #gia single-qos = 34.0 sec - input=2
#versions = ['06_18_21'] #gia ginglq-qos = 29.0 sec - input=2
#versions = ['06_19_06']
#versions = ['06_19_12']
#versions = ['06_19_19']
#versions = ['06_24_13', '06_24_17', '06_24_18']
#versions = ['07_03_20']
versions = ['07_10_10']
time = mergeResults('t', versions)
time2 = parseTimes(time)

action = mergeResults('a', versions)
action2 = parseActions(action)

reward = mergeResults('r', versions)
reward2 = parseRewards(reward)

frequency = {}
for item in action2[2]:
   if item in frequency:
      frequency[item] += 1
   else:
      frequency[item] = 1

figure, axis = plt.subplots(5, 4, figsize=(30, 19))
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

print('FOR VERSIONS:', str(versions))
print('action-len =', len(action), ', time-len =', len(time), ', reward-len =', len(reward))
print('TIMES AVG / 100 STEPS:', my_mean(time2[1][0:100]), my_mean(time2[1][100:200]), my_mean(time2[1][200:300]), my_mean(time2[1][300:400]))
print('REWARDS AVG / 100 STEPS:', my_mean(reward2[1][0:100]), my_mean(reward2[1][100:200]), my_mean(reward2[1][200:300]), my_mean(reward2[1][300:400]))
print('ACTIONS SELECTED FREQUENCY:', {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1])})
vals = []
for i in range(0, 450, 5):
    a = my_mean(reward2[1][(i):(i+5)])
    vals.append(a)


axis[3,2].plot(vals)
axis[3, 2].set_title('Average reward taken (Average per 5 training steps)')

reward_sign = reward2[4]
print('VIOLATIONS: ', len(reward_sign)-reward_sign.count(1), 'out of', len(reward_sign))

#axis[3,1].plot(vals)

y1, y2 = [], []

i = 0
minus_ones, ones = 0, 0
for i in range(len(reward_sign)):
    if (reward_sign[i] == 1):
        ones += 1
    else:
        minus_ones += 1
    y1.append(ones)
    y2.append(minus_ones)

axis[4, 2].set_xlabel('training steps')
axis[4, 2].set_ylabel('Count')
axis[4, 2].plot(y1, label='positive rewards')
axis[4, 2].plot(y2, label='negative rewards')
axis[4, 2].set_title('Positive-Negative reward input2')
axis[4, 2].legend()
#axis[4, 1].hist([y1, y2],color=colors, bins=62, label=['positive_rewards', 'negative_rewards'])
#axis[4, 1].set_xlim(-5,8)
#axis[4, 1].set_ylabel("Count")
#axis[4,1].plot(reward_sign)
#axis[4, 1].set_title('Positive-Negative reward input2')
plt.show()
plt.savefig('../images/' + versions[0] + '.png')