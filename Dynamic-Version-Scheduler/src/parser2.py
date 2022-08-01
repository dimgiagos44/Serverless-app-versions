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


#versions = ['07_10_10']
#versions = ['07_30_12']
#versions = ['07_31_10']
versions = ['07_31_21']
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

vals = []
for i in range(0, 500, 3):
    a = my_mean(reward2[1][(i):(i+3)])
    vals.append(a)

acc_reward = 0
acc_rewards = []
for i in reward2[1]:
    acc_reward += float(i)
    acc_rewards.append(acc_reward)


reward_sign = reward2[4]
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

figure, axis = plt.subplots(2, 3, figsize=(20, 15))


axis[0,0].plot(vals)
axis[0, 0].set_title('Average reward taken (Average per 5 training steps)')
axis[0, 0].set_ylabel('Average reward')

axis[0, 1].plot(time2[1])
axis[0, 1].set_ylabel('latency / TMAX')
axis[0, 1].set_title('Time Input 1')
axis[0, 1].set_xlabel('Training steps')


axis[0, 2].plot(acc_rewards)
axis[0, 2].set_ylabel('Agent accumalative reward')
axis[0, 2].set_title('Accumulative reward')
axis[0, 2].set_xlabel('Training steps')

axis[1, 0].set_xlabel('Training Steps')
axis[1, 0].set_ylabel('Count')
axis[1, 0].plot(y1, label='positive rewards')
axis[1, 0].plot(y2, label='negative rewards')
axis[1, 0].text(5, 280, r'0-300: qos=35', fontsize=10)
axis[1, 0].text(5, 270, r'300-500: qos=26', fontsize=10)
axis[1, 0].set_title('Positive-Negative reward')
axis[1, 0].legend()

axis[1, 1].plot(action2[1])
axis[1, 1].set_ylabel('Action chosen')
axis[1, 1].set_title('Action Input 1')
axis[1, 1].set_xlabel('Training steps')


axis[1, 2].plot(reward2[1])
axis[1, 2].set_title('Reward Input 1')
axis[1, 2].set_xlabel('Training steps')



print('FOR VERSIONS:', str(versions))
print('action-len =', len(action), ', time-len =', len(time), ', reward-len =', len(reward))
print('TIMES AVG / 100 STEPS:', my_mean(time2[1][0:100]), my_mean(time2[1][100:200]), my_mean(time2[1][200:300]), my_mean(time2[1][300:400]))
print('REWARDS AVG / 100 STEPS:', my_mean(reward2[1][0:100]), my_mean(reward2[1][100:200]), my_mean(reward2[1][200:300]), my_mean(reward2[1][300:400]))
print('ACTIONS SELECTED FREQUENCY:', {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1])})
print('VIOLATIONS: ', len(reward_sign)-reward_sign.count(1), 'out of', len(reward_sign))


#axis[4, 1].hist([y1, y2],color=colors, bins=62, label=['positive_rewards', 'negative_rewards'])
#axis[4, 1].set_xlim(-5,8)
#axis[4, 1].set_ylabel("Count")
#axis[4,1].plot(reward_sign)
#axis[4, 1].set_title('Positive-Negative reward input2')
plt.show()
plt.savefig('../images/' + versions[0] + '_oracle.png')