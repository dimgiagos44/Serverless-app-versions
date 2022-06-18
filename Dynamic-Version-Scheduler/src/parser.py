import json
from statistics import mean
import matplotlib.pyplot as plt

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

#versions = ['05_23_15', '05_23_19', '05_23_21', '05_24_11']
#versions = ['05_20_15', '05_20_18', '05_23_12']
#versions = ['05_31_11', '06_01_09', '06_01_13']
#versions = ['06_05_14', '06_05_21']
#versions = ['06_06_10', '06_06_14']
#versions = ['06_06_20']
#versions = ['06_07_11']
#versions = ['06_11_20']
#versions = ['06_16_10'] #512... #explor_factor=0.1
#versions = ['06_16_18']
#versions = ['06_17_01']
versions = ['06_18_14']
'''
model = DQN("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1, train_freq=(1, "step"), learning_rate=0.0025, learning_starts=15,
            batch_size=32, buffer_size=1000000, target_update_interval=50, gamma=0.99, exploration_fraction=0.15, 
            exploration_initial_eps=1, exploration_final_eps=0.01, tensorboard_log="./logs/%s/" % dt)
'''
time = mergeResults('t', versions)
time2 = parseTimes(time)

action = mergeResults('a', versions)
action2 = parseActions(action)

reward = mergeResults('r', versions)
reward2 = parseRewards(reward)

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
vals = []
for i in range(0, 300, 5):
    a = my_mean(reward2[1][(i):(i+5)])
    vals.append(a)

axis[3,1].plot(vals)
axis[3, 1].set_title('Reward escalation for input2 Step: 5')

frequency = {}
for item in action2[1]:
   if item in frequency:
      frequency[item] += 1
   else:
      frequency[item] = 1

print('ACTIONS SELECTED FREQUENCY:', {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1])})

print('Violations')
t = []
count = 0
for i in range(0, len(reward2[1])):
    if (int(reward2[1][i]) > 0):
        t.append(1)
        count += 1
    else:
        t.append(-1)
print(t, count, len(t)-count)
axis[4,1].plot(t)
axis[4, 1].set_title('+- escalation for input2 Step: 5')
#print(mean(time2[0]), mean(time2[1]))
plt.show()
plt.savefig('../images/' + versions[0] + '.png')