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


        self.action_space = gym.spaces.Discrete(8)
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
    def takeAction(self, action):
        deploy_monolith_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2'
        deploy_framerfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=framerfn'
        deploy_facedetectorfn2_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=facedetectorfn2'
        deploy_faceanalyzerfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=faceanalyzerfn'
        deploy_mobilenetfn_command = 'faas deploy -f ../../functions/version4/functions.yml --filter=mobilenetfn'
        constraint_worker_command = ['', ' --constraint "kubernetes.io/hostname=gworker-01"', ' --constraint "kubernetes.io/hostname=gworker-02"',
                                    ' --constraint "kubernetes.io/hostname=gworker-03"', ' --constraint "kubernetes.io/hostname=gworker-04"']
        if (action[0] == 0):
            command = 'faas remove monolith2'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
            if (action[1] >= 1 or action[1] <= 4):
                command = deploy_monolith_command + constraint_worker_command[action[1]]
                subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                time.sleep(3)
            else:
                print('Wrong configuration on action vector #1!')
        elif (action[0] == 1): 
            command = 'faas remove framerfn && faas remove facedetectornf2 && faas remove faceanalyzerfn && faas remove mobilenetfn'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
            command =  deploy_framerfn_command + constraint_worker_command[action[1]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = deploy_facedetectorfn2_command + constraint_worker_command[action[2]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command =  deploy_faceanalyzerfn_command + constraint_worker_command[action[3]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = deploy_mobilenetfn_command + constraint_worker_command[action[4]]
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        else:
            print('Wrong configuration on action vector #2!')
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