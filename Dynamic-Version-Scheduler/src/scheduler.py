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

EVENTS = ['IPC', 'MEM_READ', 'MEM_WRITE', 'L3M', 'C0RES', 'C1RES', 'NOT_C0RES_C1RES']
EVENT_MAX = [5, 5, 5, 5, 5, 5, 5]
EVENT_MAX = [e*2 for e in EVENT_MAX]


class CustomEnv(gym.Env):
    def __init__(self,):
        super(CustomEnv, self).__init__()

        self.startingTime = round(time.time())

        self.inputs = { 1: ['90', '7'], 2: ['40', '16'], 3: ['20', '32'], 4: ['10', '65']}

        self.qosValues = { 
            1: [17, 45.25, 73.5, 84.75, 130], 
            2: [18.5, 51.25, 65.5, 117, 150], 
            3: [19.6, 60, 102, 144, 185], 
            4: [23.5, 81.2, 138, 196.75, 231] 
        }

        self.actionText = { 0: 'Moving framer', 1: 'Moving facedetector', 2: 'Moving models', 3: 'Scaling models UP', 4: 'Scaling models DOWN', 5: 'Scaling facedetectorfn UP',
                            6: 'Scaling facedetectorfn2 DOWN', 7: 'Maintaining'}

        self.state = [0] * 35

        self.action_space = gym.spaces.Discrete(8) # totally 8 possible actions for the agent
        self.observation_space = gym.spaces.Box(low=0, high=300, shape=(35,), dtype=np.float64) # se ti diastima timwn anikoun oi metavlites pou apartizoun to state
        self.placementInit()

    def placementInit(self):
        print('Executing the init method..')
        command = 'faas remove framerfn && faas remove facedetectorfn2 && faas remove faceanalyzerfn && faas remove mobilenetfn'
        subprocess.getoutput(command)
        time.sleep(15)

        framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', 'kubernetes.io/hostname=gworker-02']
        subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', 'kubernetes.io/hostname=gworker-02']
        subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        faceanalyzerfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=faceanalyzerfn', '--constraint', 'kubernetes.io/hostname=gworker-02']
        subprocess.check_call(faceanalyzerfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        mobilenetfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=mobilenetfn', '--constraint', 'kubernetes.io/hostname=gworker-02']
        subprocess.check_call(mobilenetfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(10)
    
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
        #return scores.index(max(scores))
        random_list = [2, 3, 4]
        return random.choice(random_list)

    def takeAction(self, action, bestScoreIndex, inputIndex):
        number_of_models_command = 'faas list | grep mobilenetfn'
        number_of_models_str = subprocess.getoutput(number_of_models_command)
        number_of_models = int(number_of_models_str[-5])

        number_of_facedetector_command = 'faas list | grep facedetectorfn2'
        number_of_facedetector_str = subprocess.getoutput(number_of_facedetector_command)
        number_of_facedetector = int(number_of_facedetector_str[-5])

        scale_models_commnand = 'kubectl scale deployment faceanalyzerfn mobilenetfn -n openfaas-fn --replicas='
        scale_facedetector_command = 'kubectl scale deployment facedetectorfn2 -n openfaas-fn --replicas='

        replicas_command = ['', '1', '2', '3', '4']
        constraint_worker_command = ['', 'kubernetes.io/hostname=gworker-01', 'kubernetes.io/hostname=gworker-02', 'kubernetes.io/hostname=gworker-03', 'kubernetes.io/hostname=gworker-04']

        if action == 0:
            framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', constraint_worker_command[bestScoreIndex]]
            subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            
        elif action == 1:
            if (number_of_facedetector >= 2):
                command = 'faas remove facedetectorfn2'
                subprocess.getoutput(command)
                time.sleep(8)
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', constraint_worker_command[bestScoreIndex]]
            subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        
        elif action == 2:
            if (number_of_models >= 2):
                command = 'faas remove faceanalyzerfn && faas remove mobilenetfn'
                subprocess.getoutput(command)
                time.sleep(8)
            faceanalyzerfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=faceanalyzerfn', '--constraint', constraint_worker_command[bestScoreIndex]]
            subprocess.check_call(faceanalyzerfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            mobilenetfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=mobilenetfn', '--constraint', constraint_worker_command[bestScoreIndex]]
            subprocess.check_call(mobilenetfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) 

        elif action == 3:
            if (number_of_models == 4):
                return -1, 0
            else:
                number_of_models += 1
                command = scale_models_commnand + replicas_command[number_of_models]
                subprocess.getoutput(command)

        elif action == 4:
            if (number_of_models == 1):
                return -1, 0
            else:
                number_of_models -= 1
                command = scale_models_commnand + replicas_command[number_of_models]
                subprocess.getoutput(command)
        
        elif action == 5:
            if (number_of_facedetector == 4):
                return -1, 0
            else:
                number_of_facedetector += 1
                command = scale_facedetector_command + replicas_command[number_of_facedetector]
                subprocess.getoutput(command)

        elif action == 6:
            if (number_of_facedetector == 1):
                return -1, 0
            else:
                number_of_facedetector -= 1
                command = scale_facedetector_command + replicas_command[number_of_facedetector]
                subprocess.getoutput(command)

        else:
            pass

        print('\n--------------------------------------------------------------')
        print('Applying the configuration before executing... (5 sec delay)\nAction No:', action, '=>', self.actionText[action])
        time.sleep(5)
        command = 'python3 ../../runtime/version1/version1fn.py ' + self.inputs[inputIndex][0] + ' ' + self.inputs[inputIndex][1]
        res = subprocess.getoutput(command)
        latency = float(res.split(':')[1])

        return 0, latency

    # @must
    def reset(self):
        print('Reset() called atm')
        self.state = [0] * 35
        self.state[28:35] = [1.0, 1.0, 1.0, 1.0, 1.0, 15, 1]
        print('Init state ->', self.state[28:33])
        return self.state
    
    def normData(self, state):
        state_space = []
        for i in range(0, 4):
            out = state[i]/(EVENT_MAX[0])
            out1 = state[i+1]/(EVENT_MAX[1])
            out2 = state[i+2]/(EVENT_MAX[2])
            out3 = state[i+3]/(EVENT_MAX[3])
            out4 = state[i+4]/(EVENT_MAX[4])
            out5 = state[i+5]/(EVENT_MAX[5])
            out6 = state[i+6]/(EVENT_MAX[6])
            state_space.extend([out, out1, out2, out3, out4, out5, out6])
            #state_space.append(out)
        state_space.extend([int(state[-7]), int(state[-6]), int(state[-5]), int(state[-4]), int(state[-3]), int(state[-2]), int(state[-1])])
        return np.array(state_space)
    
    def getState(self, pmc, qosTarget=0, inputIndex=0):
        state = [0] * 35
        for i in range(0, 4):
            state[i] += pmc[i]['IPC']
            state[i+1] += pmc[i]['MEM_READ']
            state[i+2] += pmc[i]['MEM_WRITE']
            state[i+3] += pmc[i]['L3M']
            state[i+4] += pmc[i]['C0RES']
            state[i+5] += pmc[i]['C1RES']
            state[i+6] += pmc[i]['NOT_C0RES_C1RES']
        
        check_framerfn_pos_command = 'kubectl get pods -n openfaas-fn -o wide | grep framerfn'
        check_facedetectorfn2_pos_command = 'kubectl get pods -n openfaas-fn -o wide | grep facedetectorfn2'
        check_models_pos_command = 'kubectl get pods -n openfaas-fn -o wide | grep mobilenetfn'
        number_of_models_command = 'faas list | grep mobilenetfn'
        number_of_facedetector_command = 'faas list | grep facedetectorfn2'
        
        framerfn_pos_str = subprocess.getoutput(check_framerfn_pos_command)
        framerfn_pos = int(framerfn_pos_str.split('gworker-0')[1].split(' ')[0])
        facedetectorfn2_pos_str = subprocess.getoutput(check_facedetectorfn2_pos_command)
        facedetectorfn2_pos = int(facedetectorfn2_pos_str.split('gworker-0')[1].split(' ')[0])
        models_pos_str = subprocess.getoutput(check_models_pos_command)
        models_pos = int(models_pos_str.split('gworker-0')[1].split(' ')[0])
        number_of_models_str = subprocess.getoutput(number_of_models_command)
        number_of_models = int(number_of_models_str[-5])
        number_of_facedetector_str   = subprocess.getoutput(number_of_facedetector_command)
        number_of_facedetector = int(number_of_facedetector_str[-5])

        state[28:35] = [framerfn_pos, facedetectorfn2_pos, models_pos, number_of_facedetector, number_of_models, qosTarget, inputIndex]
        normalized = self.normData(state)

        return list(normalized)
    
    def spreadCalculator(self):
        if (self.state[28] == self.state[29]):
            if (self.state[28] == self.state[30]):
                return 1
            else:
                return 2
        elif (self.state[28] == self.state[30]):
            return 2
        elif (self.state[29] == self.state[30]):
            return 2
        else:
            return 3
        
    
    def getReward(self, ignoredAction, latency, qosTarget):
        qos = latency
        #positions: framer_pos, facedetector_pos, models_pos, #facedetector, #models
        if qos > qosTarget:
            reward = -10
        else:
            spread = self.spreadCalculator()
            reward = (20 - (self.state[31] + (2 * self.state[32]))) / spread
        if ignoredAction != 0:
            reward = -10
        return reward

    def qosGenerator(self, inputIndex=1):
        return self.qosValues[inputIndex][random.randint(0, len(self.qosValues[inputIndex])) - 1]
        

    # @must
    def step(self, action):
        bestScoreIndex = self.findBestScore([])
        qosTarget = self.state[-2]
        inputIndex = int(self.state[-1])
        
        ignoredAction, latency = self.takeAction(action, bestScoreIndex, inputIndex)
        reward = self.getReward(ignoredAction, latency, qosTarget)
        print('qosTarget =', qosTarget, '\ninput-index =', inputIndex, 'bestScoreIndex =', bestScoreIndex)
        print('latency =', latency, '\nreward =', reward)
        time.sleep(7)

        pmc, _ = self.getMetrics(period=5)
        inputIndex = random.randint(1, 4)
        qosTarget = self.qosGenerator(inputIndex)
        observedState = self.getState(pmc, qosTarget, inputIndex)
        print('observed state after action ->', observedState[28:33])
        self.state = observedState
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
            #tensorboard_log="./logs/%s/" % dt
            )



if __name__ == "__main__":
    model.learn(total_timesteps=50)
    model.save("./models/%s/model.zip" % dt)


#TODO count max values of pmc metrics. to be done last thing before training
#TODO load, save model
#TODO possible reset() bug
#TODO hyperparameters check.
#TODO qos percentages again