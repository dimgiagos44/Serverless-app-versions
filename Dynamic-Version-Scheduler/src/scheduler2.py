from datetime import datetime
from pathlib import Path
import subprocess
import gym
import os
os.environ['OPENAI_LOG_FORMAT']='stdout,log,csv,tensorboard'
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import tensorflow as tf
import torch
from datetime import datetime
import time
import loggers
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
import random

EVENTS = ['IPC', 'MEM_READ', 'MEM_WRITE', 'L3M', 'C0RES', 'C1RES', 'NOT_C0RES_C1RES']

rewardLogger, actionLogger, timeLogger, stateLogger = loggers.setupDataLoggers()

class CustomEnv(gym.Env):
    def __init__(self, training=True, inputIndex=2, qos=29):
        super(CustomEnv, self).__init__()

        self.startingTime = round(time.time())

        self.training = training
        self.inputIndex = inputIndex
        self.qos = qos

        self.inputs = {1: ['90', '7'], 2: ['40', '16'], 3: ['20', '32'], 4: ['10', '65']}

        self.iterationNumber = 0
        self.spread = 1
        self.replicas = 3

        #10%-25%-50%-75%-100% of max latency per input-size\
        self.timesPool = { 
            1: [15.5, 27.25, 55.5, 85.75, 110.0],
            2: [17.8, 34.5, 69.0, 103.5, 125.0], 
            3: [19.5, 41.25, 82.5, 114.75, 165.0],
            4: [25.8, 54.5, 102.0, 140.5, 200.0] 
        }
        
        self.actionText = { 0: 'Moving framer to worker1', 1: 'Moving framer to worker2', 2: 'Moving framer to worker3',  3: 'Moving framer to worker4',
        4: 'Moving facedetector to worker1', 5: 'Moving facedetector to worker2', 6: 'Moving facedetector to worker3', 7: 'Moving facedetector to worker4',
        8: 'Moving models', 9: 'Scaling models UP', 10: 'Scaling models DOWN', 11: 'Maintaining'}

        self.state = [0] * 35

        self.action_space = gym.spaces.Discrete(12) # totally 8 possible actions for the agent
        self.observation_space = gym.spaces.Box(low=0, high=20, shape=(35,), dtype=np.float64) # se ti diastima timwn anikoun oi metavlites pou apartizoun to state
        self.placementInit()

    def placementInit(self):
        print('Executing the init method..')
        command = 'faas remove framerfn && faas remove facedetectorfn2 && faas remove faceanalyzerfn && faas remove mobilenetfn'
        subprocess.getoutput(command)
        time.sleep(18)

        try:
            framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', 'kubernetes.io/hostname=gworker-01']
            subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', 'kubernetes.io/hostname=gworker-01']
            subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            faceanalyzerfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=faceanalyzerfn', '--constraint', 'kubernetes.io/hostname=gworker-01']
            subprocess.check_call(faceanalyzerfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            mobilenetfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=mobilenetfn', '--constraint', 'kubernetes.io/hostname=gworker-01']
            subprocess.check_call(mobilenetfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(15)

        except subprocess.CalledProcessError as e:
            print('Init error handled here! Exiting')
            exit()
    
     # @must
    def reset(self):
        print('Reseting the state back to initialization.')
        self.state[28:35] = [1.0, 1.0, 1.0, 1.0, 1.0, 15.0, 1.0]
        print('Init state \u27A9', self.state[28:33])
        return self.state

    def getMetrics(self, period=5):
        liono_command = 'go run main.go ' + str(period) + ' average liono'
        davinci_command = 'go run main.go ' + str(period) + ' average davinci'
        coroni_command = 'go run main.go ' + str(period) + ' average coroni'
        cheetara_command = 'go run main.go ' + str(period) + ' average cheetara'

        liono_metrics_str = subprocess.getoutput(liono_command)
        davinci_metrics_str = subprocess.getoutput(davinci_command)
        coroni_metrics_str = subprocess.getoutput(coroni_command)
        cheetara_metrics_str = subprocess.getoutput(cheetara_command)

        all_metrics_str = [davinci_metrics_str, liono_metrics_str, coroni_metrics_str, cheetara_metrics_str]
        metrics = []
        scores = []
        for metrics_str in all_metrics_str:
            if 'Node' not in metrics_str:
                print('----------Got in panic but escaped! getMetrics() error---------')
                score = 0.002
                metric = {
                    'IPC': float(0.1),
                    'MEM_READ': float(0.02),
                    'MEM_WRITE': float(0.004),
                    'L3M': float(0.2),
                    'C0RES': float(0.9),
                    'C1RES': float(0.1),
                    'NOT_C0RES_C1RES': float(0.0)
                }
                metrics.append(metric)
                scores.append(float(score))
            else:
                score = metrics_str.split('Score: ')[1].split(',')[0]
                scoreTest = metrics_str.split('Score: ')[1]
                if ('e+' in scoreTest):
                    score = 0.00003
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
                scores.append(float(score))
        
        return metrics, scores
    
    def findBestScore(self, scores):
        return scores.index(max(scores)) + 1

    def takeAction(self, action, bestScoreIndex, inputIndex):
        self.iterationNumber += 1
        replicas_command = ['', '1', '2', '3', '4']
        scale_models_commnand = 'kubectl scale deployment faceanalyzerfn mobilenetfn -n openfaas-fn --replicas='
        scale_facedetector_command = 'kubectl scale deployment facedetectorfn2 -n openfaas-fn --replicas='
        constraint_worker_command = ['', 'kubernetes.io/hostname=gworker-01', 'kubernetes.io/hostname=gworker-02', 'kubernetes.io/hostname=gworker-03', 'kubernetes.io/hostname=gworker-04']
        number_of_models_command = 'faas list | grep mobilenetfn'
        number_of_models_str = subprocess.getoutput(number_of_models_command)
        if len(number_of_models_str) < 5:
            print('NUMBER OF MODELS ERROR')
            faceanalyzerfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=faceanalyzerfn', '--constraint', constraint_worker_command[bestScoreIndex]]
            ret1 = subprocess.check_call(faceanalyzerfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            mobilenetfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=mobilenetfn', '--constraint', constraint_worker_command[bestScoreIndex]]
            ret2 = subprocess.check_call(mobilenetfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(3)
            return -1, 0
        else: 
            number_of_models = int(number_of_models_str[-5])

        number_of_facedetector_command = 'faas list | grep facedetectorfn2'
        number_of_facedetector_str = subprocess.getoutput(number_of_facedetector_command)
        if len(number_of_facedetector_str) < 5:
            print('NUMBER OF FACEDETECTOR ERROR')
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', constraint_worker_command[bestScoreIndex]]
            ret = subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(3)
            return -1, 0
        else:
            number_of_facedetector = int(number_of_facedetector_str[-5])

        if action == 0:
            framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', constraint_worker_command[1]]
            try:
                ret = subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 1:
            framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', constraint_worker_command[2]]
            try:
                ret = subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 2:
            framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', constraint_worker_command[3]]
            try:
                ret = subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 3:
            framer_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=framerfn', '--constraint', constraint_worker_command[4]]
            try:
                ret = subprocess.check_call(framer_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 4:
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', constraint_worker_command[1]]
            try:
                ret = subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)        
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 5:
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', constraint_worker_command[2]]
            try:
                ret = subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)        
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 6:
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', constraint_worker_command[3]]
            try:
                ret = subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)        
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 7:
            facedetectorfn2_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=facedetectorfn2', '--constraint', constraint_worker_command[4]]
            try:
                ret = subprocess.check_call(facedetectorfn2_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)        
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 8:
            if (number_of_models >= 2):
                command = 'faas remove faceanalyzerfn && faas remove mobilenetfn'
                subprocess.getoutput(command)
                time.sleep(15)
            try:
                faceanalyzerfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=faceanalyzerfn', '--constraint', constraint_worker_command[bestScoreIndex]]
                ret1 = subprocess.check_call(faceanalyzerfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                mobilenetfn_command = ['faas', 'deploy', '-f', 'functions.yml', '--filter=mobilenetfn', '--constraint', constraint_worker_command[bestScoreIndex]]
                ret2 = subprocess.check_call(mobilenetfn_command, cwd='../../functions/version1', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) 
            except subprocess.CalledProcessError as e:
                print('error = ', e)
                return -1, 0
        elif action == 9:
            if (number_of_models == 4):
                return -1, 0
            else:
                number_of_models += 1
                command = scale_models_commnand + replicas_command[number_of_models]
                subprocess.getoutput(command)

        elif action == 10:
            if (number_of_models == 1):
                return -1, 0
            else:
                number_of_models -= 1
                command = scale_models_commnand + replicas_command[number_of_models]
                subprocess.getoutput(command)
        else:
            pass

        print("\n---------------ITERATION NUMBER {} ---------------------------------------".format(self.iterationNumber))
        print('\u2699 Applying the configuration before executing... (18 sec delay)\nAction No:', action, '\u27A9', self.actionText[action])
        time.sleep(18)
        command = 'python3 ../../runtime/version1/version1fn.py ' + self.inputs[inputIndex][0] + ' ' + self.inputs[inputIndex][1]
        res = subprocess.getoutput(command)
        latency = float(res.split(':')[1])
        return 0, latency
    
    def normData(self, state):
        state_space = []
        for i in range(0, 4):
            state_space.extend([state[i], state[i+1], state[i+2], state[i+3], state[i+4], state[i+5], state[i+6]])
            
        state_space.extend([int(state[-7]), int(state[-6]), int(state[-5]), int(state[-4]), int(state[-3]), int(state[-2]), int(state[-1])])
        return np.array(state_space)
    
    #loading to the vectorState: pcm + containers_pos + containers_replicas + tMax + inputIndex
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
        
    def getReward(self, ignoredAction, latency, tMax):
        #positions: framer_pos, facedetector_pos, models_pos, #facedetector, #models
        spread = self.spreadCalculator()
        replicas = int(self.state[31]) + (2 * int(self.state[32]))
        self.spread = spread
        self.replicas = replicas
        if latency > tMax:
            #reward = min(-5, latency - qosTarget)
            #reward = max(reward, -12)
            reward = max(-6,  -4 - (latency / tMax))
        elif latency == 0:
            pass
        else:
            #reward = ((latency / qosTarget) * 4) + (3 / spread) + (12 / replicas)
            reward = (3 / spread) + (12 / replicas) + (latency / tMax)*3
        if ignoredAction != 0:
            reward = -1
        
        return reward

    def qosGenerator(self, inputIndex=1):
        return self.timesPool[inputIndex][random.randint(0, len(self.timesPool[inputIndex])) - 1]
        

    # @must
    def step(self, action):
        '''
        tMax = self.state[-2] inputIndex = int(self.state[-1])
        self.qos = ...
        self.inputIndex = ...
        '''
        if (self.iterationNumber >= 150 and self.iterationNumber <= 300):
            self.qos = 35
        elif (self.iterationNumber > 300):
            self.qos = 28
        else: 
            pass
        tMax = self.qos
        inputIndex = self.inputIndex
        time.sleep(1)
        _, scores = self.getMetrics(period=5)
        bestScoreIndex = self.findBestScore(scores)
        ignoredAction, latency = self.takeAction(action, bestScoreIndex, inputIndex)
        stringTime = str(round(time.time()) - self.startingTime)
        actionLogger.info("Action taken: " + str(action) + "| input type: " + str(inputIndex) + "| time:" + stringTime)

        if ignoredAction == -1:
            print('Just ignored an action.')
            reward = -2
            observedState = self.state
        else: 
            time.sleep(8.5)
            pmc, _ = self.getMetrics(period=5)
            #newInputIndex = random.randint(1, 4) #tMax = self.qosGenerator(inputIndex)
            newInputIndex = self.inputIndex
            tMax = self.qos
            observedState = self.getState(pmc, tMax, newInputIndex) #setting here the new state
            self.state = observedState
            reward = self.getReward(ignoredAction, latency, tMax)
            print('\u2219 tMax =', tMax, '\u2219 input-index =', inputIndex, '\u2219 bestScoreIndex =', bestScoreIndex, '\u2219 scores =', scores)
            print('\u2219 latency =', latency, '\u2219 reward =', reward, '\u2219 spread =', self.spread, '\u2219 replicas =', self.replicas)
            print('observed state after action \u27A9', observedState[28:33])
            if (self.training == True):
                timeLogger.info("Time quotient is: " + str(latency / tMax) + "| input type: " + str(inputIndex) + "| time:" + stringTime + " | latency: " + str(latency))
            else:
                timeLogger.info("INFERENCE Time quotient is: " + str(latency / tMax) + "| input type: " + str(inputIndex) + "| time:" + stringTime + " | latency: " + str(latency))

        stateLogger.info("State is: %s | time: %s" % (observedState, stringTime))
        rewardLogger.info("Reward is: " + str(reward) + "| input type: " + str(inputIndex) + "| time:" + stringTime)
        return observedState, reward, 0, {}


#batch_size: # of tuples (s_t, r, a, s_t+1)to feed in an update rule
#train_freq: every train_freq steps we perform a batch_training
#target_update_interval: 


dt = datetime.now().strftime("%m_%d_%H")
Path("./models/%s" % dt).mkdir(parents=True, exist_ok=True)
env = CustomEnv(training=True, inputIndex=2, qos=44)
#model = DQN.load("./models/06_24_13/rl_model_200_steps.zip", env)
policy_kwargs = dict(activation_fn=torch.nn.ReLU, net_arch=[256, 128, 64])


model = DQN("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1, train_freq=(1, "step"), learning_rate=0.0025, learning_starts=15,
            batch_size=32, buffer_size=1000000, target_update_interval=60, gamma=0.99, exploration_fraction=0.2, 
            exploration_initial_eps=1, exploration_final_eps=0.01, tensorboard_log="./logs/%s/" % dt)

if __name__ == "__main__":
    total_timesteps = 480
    checkpoint_callback = CheckpointCallback(save_freq=100, save_path="./models/%s/" % (dt))
    model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)
    model.save("./models/%s/model_final.zip" % (dt))

# na logarw sta log files kai vlepoume me grep
# na tsekarw an logarei sto telos twn total_timesteps tipota....(ana episode diladi)