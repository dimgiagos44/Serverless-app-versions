from datetime import datetime
from pathlib import Path
import subprocess
import gym
import os
import tensorflow as tf
import time
import threading
import numpy as np

containerReward = {
    'reward': [],
    'lock': threading.Lock()
}

processReady = threading.Lock()

class CustomEnv(gym.Env):
    def __init__(self,):
        super(CustomEnv, self).__init__()

        self.startingTime = round(time.time())
        self.process = None

        self.switcher = {
            0:  '01000', 1:  '0200', 2:  '0300', 3:  '0400', 4:  '1111', 5:  '1222', 6:  '1333', 7:  '1444',
            8: '1112', 9: '1113', 10: '1114', 11: '1221', 12: '1223', 13: '1224', 14: '1331', 15: '1332',
            16: '1334', 17: '1441', 18: '1442', 19: '1443', 20: '1231', 21: '1233', 22: '1234', 23: '1233'
        }

        self.inputs = { 0: ['90', '7'], 1: ['40', '16'], 2: ['20', '32'], 3: ['10', '65']}

        self.action_space = gym.spaces.Discrete(len(self.switcher))
        self.observation_space = gym.spaces.Box() #se ti diastima timwn anikoun oi metavlites pou apartizoun to state

        self.placementInit()

    def placementInit():
        command = 'faas remove framerfn && faas remove facedetectornf2 && faas remove faceanalyzerfn && faas remove mobilenetfn && faas remove monolith2'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)

    def getPMC(self):
        pmc = None
        return pmc

    '''
    action[0] = 0 or 1, monolith2 or spasmeno
    if action[0] == 0: deploy monolith2 on action[1] node
    else: deploy framerfn on action[1] node, facedetectorfn2 on action[2] node etc.
    '''
    def takeAction(self, action, input):
        action_vector = self.switcher.get(action)
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
                time.sleep(3)
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
            time.sleep(3)
        else:
            print('Wrong configuration on action vector #2!')
        
        if (action_vector[0] == 0):
            command = 'python3 ../../runtime/version4/version4.py ' + self.inputs[input][0] + ' ' + self.inputs[input][1]
            latency = subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        elif (action_vector[0] == 1):
            command = 'python3 ../../runtime/version1/version1.py ' + self.inputs[input][0] + ' ' + self.inputs[input][1]
            latency = subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else: 
            print('Error occured in action taking!')
        return 0

    def reset(self):
        state = None
        return state
    
    def getState(self, before, after):
        return 0
    
    def getReward(self, ignoreAction = 0):
        return 0

    def clearReward(self):
        global containerReward
        containerReward['lock'].acquire()
        containerReward['reward'] = []
        containerReward['lock'].release()

    def step(self, action):
        while(not processReady.acquire(blocking=False)):
            time.sleep(1)
            print('Waiting on process to be ready')
        pmc_before = self.getPMC()
        ignored_action = self.takeAction(action)
        self.clearReward()
        time.sleep(2)
        pmc_after = self.getPMC()
        state = self.getState(pmc_before, pmc_after)
        reward = self.getReward(ignored_action)
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