from datetime import datetime
from pathlib import Path
import subprocess
import gym
import os
import tensorflow as tf
import time
import threading
import numpy as np
import dequeue
import random
import json

containerReward = {
    'reward': [],
    'lock': threading.Lock()
}

processReady = threading.Lock()

window_size = None

qosTarget = None

deques = {
    'IPC': dequeue([], maxlen=window_size),
    'MEM_READ': dequeue([], maxlen=window_size),
    'MEM_WRITE': dequeue([], maxlen=window_size),
    'L3M': dequeue([], maxlen=window_size),
    'C0RES': dequeue([], maxlen=window_size),
    'C1RES': dequeue([], maxlen=window_size),
    'NOT_C0RES_C1RES': dequeue([], maxlen=window_size),
}

EVENTS = ['IPC', 'MEM_READ', 'MEM_WRITE', 'L3M', 'C0RES', 'C1RES', 'NOT_C0RES_C1RES']
EVENT_MAX = []
EVENT_MAX = [e*2 for e in EVENT_MAX]


class CustomEnv(gym.Env):
    def __init__(self,):
        super(CustomEnv, self).__init__()
        global deques, window_size
        self.deques = deques
        self.window_size = window_size

        self.startingTime = round(time.time())
        self.process = None

        self.actionSelector = {
            0:  '01000', 1:  '0200', 2:  '0300', 3:  '0400', 4:  '1111', 5:  '1222', 6:  '1333', 7:  '1444',
            8: '1112', 9: '1113', 10: '1114', 11: '1221', 12: '1223', 13: '1224', 14: '1331', 15: '1332',
            16: '1334', 17: '1441', 18: '1442', 19: '1443', 20: '1231', 21: '1232', 22: '1233', 23: '1234',
            24: '1241', 25: '1242', 26: '1243', 27: '1244', 28: '1341', 29: '1342', 30: '1343', 31: '1344',
        }

        self.inputs = { 0: ['90', '7'], 1: ['40', '16'], 2: ['20', '32'], 3: ['10', '65']}

        self.latencies = { 
            0: [10, 15, 30, 45, 60, 90], 
            1: [10, 18, 25, 40, 50, 60, 70, 85, 90, 105, 120], 
            2: [10, 15, 20, 30, 45, 60, 75, 90, 100, 110, 130, 150], 
            3: [10, 15, 20, 30, 45, 60, 70, 80, 90, 100, 110, 120, 135, 150, 180, 190, 200, 210] 
        }

        self.action_space = gym.spaces.Discrete(len(self.actionSelector))
        self.observation_space = gym.spaces.Box() #se ti diastima timwn anikoun oi metavlites pou apartizoun to state

        self.placementInit()

    def placementInit(self):
        command = 'faas remove framerfn && faas remove facedetectornf2 && faas remove faceanalyzerfn && faas remove mobilenetfn && faas remove monolith2'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)
    
    def getMetrics(self, period=5):
        liono_command = 'go run ../influx/main.go ' + str(period) + ' average liono'
        #davinci_command = 'go run ../influx/main.go ' + str(period) + ' average davinci'
        coroni_command = 'go run ../influx/main.go ' + str(period) + ' average coroni'
        #cheetara_command = 'go run ../influx/main.go ' + str(period) + ' average cheetara'

        liono_metrics_str = subprocess.getoutput(liono_command)
        #davinci_metrics_str = subprocess.getoutput(davinci_command)
        coroni_metrics_str = subprocess.getoutput(coroni_command)
        #cheetara_metrics_str = subprocess.getoutput(cheetara_command)

        all_metrics_str = [liono_metrics_str, coroni_metrics_str]

        metrics = []
        for metrics_str in all_metrics_str:
            ipc = metrics_str.split('IPC: ')[1].split(',')[0]
            memRead = metrics_str.split('Reads: ')[1].split(',')[0]
            memWrite = metrics_str.split('Writes: ')[1].split(',')[0]
            l3m = metrics_str.split('l3m: ')[1].split(',')[0]
            c0res = metrics_str.split('average_c0res: ')[1].split(',')[0]
            c1res = metrics_str.split('average_c1res: ')[1].split(',')[0]
            not_c0res_c1res = metrics_str.split('average_not_c0res_c1res: ')[1].split(',')[0]
            metric = {
                'IPC': float(ipc),
                'MEM_READ': float(memRead),
                'MEM_WRITE': float(memWrite),
                'L3M': float(l3m),
                'C0RES': float(c0res),
                'C1RES': float(c1res),
                'NOT_C0RES_C1RES': float(not_c0res_c1res)
            }
            metrics.append(metric)
        return metrics

    def getPMC(self):
        pmc = self.getMetrics()
        return pmc

    '''
    action[0] = 0 or 1, monolith2 or spasmeno
    if action[0] == 0: deploy monolith2 on action[1] node
    else: deploy framerfn on action[1] node, facedetectorfn2 on action[2] node etc.
    '''
    def takeAction(self, input, action):
        action_vector = self.actionSelector.get(action)
        deploy_monolith_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2'
        deploy_framerfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=framerfn'
        deploy_facedetectorfn2_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=facedetectorfn2'
        deploy_faceanalyzerfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=faceanalyzerfn'
        deploy_mobilenetfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=mobilenetfn'
        constraint_worker_command = ['', ' --constraint "kubernetes.io/hostname=gworker-01"', ' --constraint "kubernetes.io/hostname=gworker-02"',
                                    ' --constraint "kubernetes.io/hostname=gworker-03"', ' --constraint "kubernetes.io/hostname=gworker-04"']
        if (action_vector[0] == 0):
            if (action_vector[1] >= 1 or action_vector[1] <= 4):
                command = deploy_monolith_command + constraint_worker_command[action_vector[1]]
                subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                time.sleep(10)
            else:
                print('Wrong configuration on action vector #1!')
        elif (action_vector[0] == 1):
            command =  deploy_framerfn_command + constraint_worker_command[action_vector[1]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = deploy_facedetectorfn2_command + constraint_worker_command[action_vector[2]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command =  deploy_faceanalyzerfn_command + constraint_worker_command[action[3]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = deploy_mobilenetfn_command + constraint_worker_command[action_vector[3]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(10)
        else:
            print('Wrong configuration on action vector #2!')
        
        if (action_vector[0] == 0):
            command = 'python3 ../../runtime/version4/version4fn.py ' + self.inputs[input][0] + ' ' + self.inputs[input][1]
            res = subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            latency = float(res.split(':')[1])
        elif (action_vector[0] == 1):
            command = 'python3 ../../runtime/version1/version1fn.py ' + self.inputs[input][0] + ' ' + self.inputs[input][1]
            res = subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            latency = float(res.split(':')[1])
        else: 
            print('Error occured in action taking!')
        return 0, latency

    # @must
    def reset(self):
        state = None
        return state
    
    def normData(self):
        return None
    
    
    def getState(self, before, after):
        return 0
    
    def getReward(self, ignoreAction = 0, latency = 0, input_index = 0):
        global containerReward
        while(len(containerReward['reward']) == 0):
            time.sleep(0.01)
            
        containerReward['lock'].acquire()
        sjrn99 = np.percentile(containerReward['reward'], 99)
        qos = round(sjrn99/1e3)
        containerReward['lock'].release()

        qos = latency

        qosTargetIndex = random.randint(0, len(self.latencies[input_index]) - 1)
        qosTarget = self.latencies[qosTargetIndex]
        if qos > qosTarget:
            reward = None
        else:
            reward = None
        if ignoreAction != 0:
            reward = None
        
        return 0

    def clearReward(self):
        global containerReward
        containerReward['lock'].acquire()
        containerReward['reward'] = []
        containerReward['lock'].release()
        return None

    # @must
    def step(self, action):
        while(not processReady.acquire(blocking=False)):
            time.sleep(1)
            print('Waiting on process to be ready')
        pmc_before = self.getPMC()
        input_index = random.randint(0, 3)
        ignored_action, latency = self.takeAction(input_index, action)
        self.clearReward()
        time.sleep(4)
        pmc_after = self.getPMC()
        state = self.getState(pmc_before, pmc_after)
        reward = self.getReward(ignored_action, latency, input_index)
        processReady.release()
        return state, reward, 0, {}

dt = datetime.now().strftime("%m_%d_%H")
Path("./models/%s" % dt).mkdir(parents=True, exist_ok=True)

env = CustomEnv()

policy_kwargs = dict(act_fun=tf.nn.relu, layers=[512, 256, 128])

model = None

if __name__ == "__main__":
    model.learn(total_timesteps=20000)
    model.save("./models/%s/model.zip" % dt)

#TODO: reward function
#TODO: input: # of frames & desired qos
#TODO: possible actions