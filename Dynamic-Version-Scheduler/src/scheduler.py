from datetime import datetime
from pathlib import Path
import subprocess
import gym
import os
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import tensorflow as tf
import torch
import time
import threading
import numpy as np
from stable_baselines3 import DQN
import random
import json

#containerReward = {'reward': [],'lock': threading.Lock()}

#processReady = threading.Lock()

EVENTS = ['IPC', 'MEM_READ', 'MEM_WRITE', 'L3M', 'C0RES', 'C1RES', 'NOT_C0RES_C1RES']
EVENT_MAX = [5, 5, 5, 5, 5, 5, 5]
EVENT_MAX = [e*2 for e in EVENT_MAX]


class CustomEnv(gym.Env):
    def __init__(self,):
        super(CustomEnv, self).__init__()

        self.startingTime = round(time.time())

        self.inputs = { 0: ['90', '7'], 1: ['40', '16'], 2: ['20', '32'], 3: ['10', '65']}

        self.latencies = { 
            0: [10, 15, 30, 45, 60, 90], 
            1: [10, 18, 25, 40, 50, 60, 70, 85, 90, 105, 120], 
            2: [10, 15, 20, 30, 45, 60, 75, 90, 100, 110, 130, 150], 
            3: [10, 15, 20, 30, 45, 60, 70, 80, 90, 100, 110, 120, 135, 150, 180, 190, 200, 210] 
        }

        self.action_space = gym.spaces.Discrete(8) # totally 8 possible actions for the agent
        self.observation_space = gym.spaces.Box(low=0, high=5, shape=(10,), dtype=np.float64) # se ti diastima timwn anikoun oi metavlites pou apartizoun to state

        self.placementInit()

    def placementInit(self):
        #command = 'faas remove framerfn && faas remove facedetectornf2 && faas remove faceanalyzerfn && faas remove mobilenetfn && faas remove monolith2'
        #subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(5)
        print('Executing the init method..')
    
    def getMetrics(self, period=5):
        liono_command = 'go run main.go ' + str(period) + ' average liono'
        davinci_command = 'go run main.go ' + str(period) + ' average liono'
        coroni_command = 'go run main.go ' + str(period) + ' average coroni'
        cheetara_command = 'go run main.go ' + str(period) + ' average coroni'

        liono_metrics_str = subprocess.getoutput(liono_command)
        davinci_metrics_str = subprocess.getoutput(davinci_command)
        coroni_metrics_str = subprocess.getoutput(coroni_command)
        cheetara_metrics_str = subprocess.getoutput(cheetara_command)

        all_metrics_str = [liono_metrics_str, liono_metrics_str, liono_metrics_str, liono_metrics_str]

        metrics = []
        scores = []
        for metrics_str in all_metrics_str:
            score = metrics_str.split('Score: ')[1].split(',')[0]
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
            scores.append(score)
        
        return metrics, scores
    
    def findBestScore(self, scores):
        return scores.index(max(scores))

    '''
    action[0] = 0 or 1, monolith2 or spasmeno
    if action[0] == 0: deploy monolith2 on action[1] node
    else: deploy framerfn on action[1] node, facedetectorfn2 on action[2] node etc.
    '''
    def takeAction(self, action, bestScoreIndex):
        #deploy_monolith_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2'
        deploy_framerfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=framerfn'
        deploy_facedetectorfn2_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=facedetectorfn2'
        deploy_faceanalyzerfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=faceanalyzerfn'
        deploy_mobilenetfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=mobilenetfn'
        scale_models_commnand = 'kubectl scale deployment facedetectorfn2 faceanalyzerfn mobilenetfn -n openfaas-fn --replicas='
        replicas_command = ['', '1', '2', '3', '4']
        constraint_worker_command = ['', ' --constraint "kubernetes.io/hostname=gworker-01"', ' --constraint "kubernetes.io/hostname=gworker-02"',
                                    ' --constraint "kubernetes.io/hostname=gworker-03"', ' --constraint "kubernetes.io/hostname=gworker-04"']

        if action == 0:
            command = deploy_framerfn_command  + constraint_worker_command[bestScoreIndex]
            subprocess.getoutput(command)
        elif action == 1:
            command = deploy_facedetectorfn2_command + constraint_worker_command[bestScoreIndex]
            subprocess.getoutput(command)
        elif action == 2:
            command = deploy_faceanalyzerfn_command + constraint_worker_command[bestScoreIndex]
            subprocess.getoutput(command)
            commnad = deploy_mobilenetfn_command + constraint_worker_command[bestScoreIndex]
            subprocess.getoutput(command)
        elif action == 3:
            command = scale_models_commnand + replicas_command[1]
            subprocess.getoutput(command)
        elif action == 4:
            command = scale_models_commnand + replicas_command[2]
            subprocess.getoutput(command)
        elif action == 5:
            command = scale_models_commnand + replicas_command[3]
            subprocess.getoutput(command)
        elif action == 6:
            command = scale_models_commnand + replicas_command[4]
            subprocess.getoutput(command)
        else:
            print('Maintaining..')
        print('Took action:', action)
        time.sleep(3)

        #command = 'python3 ../../runtime/version1/version1fn.py ' + self.inputs[input][0] + ' ' + self.inputs[input][1]
        command = 'python3 ../../runtime/version1/version1fn.py 20 32'
        res = subprocess.getoutput(command)
        latency = float(res.split(':')[1])
        print('Latency =', latency)

        return 0, latency

    # @must
    def reset(self):
        #state = [0] * (len(EVENTS) + 2)
        state = [0] * 10
        return state
    
    def normData(self, state):
        state_space = []
        for i in range(0, 7):
            out = state[i]/(EVENT_MAX[i])
            state_space.append(out)
        state_space.append(state[-3])
        state_space.append(state[-2])
        state_space.append(state[-1])
        return np.array(state_space)
    
    def getState(self, before, after):
        state = [0] * len(EVENTS)
        #state = []
        #thelei allagi
        for i in range(0, 4):
            state[0] += after[i]['IPC']
            state[1] += after[i]['MEM_READ']
            state[2] += after[i]['MEM_WRITE']
            state[3] += after[i]['L3M']
            state[4] +=after[i]['C0RES']
            state[5] += after[i]['C1RES']
            state[6] += after[i]['NOT_C0RES_C1RES']
        
        for i in range(0, len(state)):
            state[i] = state[i] / 4
        
        check_framerfn_pos_command = 'kubectl get pods -n openfaas-fn -o wide | grep framerfn'
        check_facedetectorfn2_pos_command = 'kubectl get pods -n openfaas-fn -o wide | grep facedetectorfn2'
        check_models_pos_command = 'kubectl get pods -n openfaas-fn -o wide | grep mobilenetfn'
        
        framerfn_pos_str = subprocess.getoutput(check_framerfn_pos_command)
        framerfn_pos = int(framerfn_pos_str.split('gworker-0')[1].split(' ')[0])
        facedetectorfn2_pos_str = subprocess.getoutput(check_facedetectorfn2_pos_command)
        facedetectorfn2_pos = int(facedetectorfn2_pos_str.split('gworker-0')[1].split(' ')[0])
        models_pos_str = subprocess.getoutput(check_models_pos_command)
        models_pos = int(models_pos_str.split('gworker-0')[1].split(' ')[0])
        
        state.append(framerfn_pos)
        state.append(facedetectorfn2_pos)
        state.append(models_pos)
        normalized = self.normData(state)

        return list(normalized)
    
    def getReward(self, ignoreAction = 0, latency = 0, input_index = 3):
        qos = latency
        qosTarget = 35
        if qos > qosTarget:
            reward = -1
        else:
            reward = 1
        if ignoreAction != 0:
            reward = -10
        return reward

    '''
    def clearReward(self):
        global containerReward
        containerReward['lock'].acquire()
        containerReward['reward'] = []
        containerReward['lock'].release()
        return None
    '''

    # @must
    def step(self, action):
        pmc_current, scores = self.getMetrics(period=5)
        #inputIndex = random.randint(0, 3)
        bestScoreIndex = self.findBestScore(scores)
        ignored_action, latency = self.takeAction(action, bestScoreIndex)
        #self.clearReward()
        time.sleep(4)
        pmc_next, scores = self.getMetrics(period=5)
        time.sleep(4)
        observedState = self.getState(pmc_current, pmc_next)
        print('observed state ->', observedState)
        reward = self.getReward(ignored_action, latency)
        #processReady.release()
        return observedState, reward, 0, {}

dt = datetime.now().strftime("%m_%d_%H")
Path("./models/%s" % dt).mkdir(parents=True, exist_ok=True)

env = CustomEnv()

policy_kwargs = dict(activation_fn=torch.nn.ReLU, net_arch=[512, 256, 128])

model = DQN("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1,
            train_freq=1,
            learning_rate=0.0025, learning_starts=750,
            batch_size=64, buffer_size=1000000, target_update_interval=150,
            gamma=0.99, exploration_fraction=0.1, exploration_initial_eps=1, exploration_final_eps=0.01,
            tensorboard_log="./logs/%s/" % dt
            )

if __name__ == "__main__":
    model.learn(total_timesteps=20000)
    model.save("./models/%s/model.zip" % dt)
