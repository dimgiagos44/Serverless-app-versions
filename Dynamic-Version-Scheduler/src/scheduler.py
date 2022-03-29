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
        self.observation_space = gym.spaces.Box()

        self.placementInit()

    def placementInit():
        command = 'faas remove framerfn && faas remove facedetectornf2 && faas remove faceanalyzerfn && faas remove mobilenetfn && faas remove monolith2'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)

    def getPMC(self):
        pmc = None
        return pmc

    def takeAction(self, action):
        if (action >= 0 and action <= 3):
            command = 'faas remove monolith2'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        else: 
            command = 'faas remove framerfn && faas remove facedetectornf2 && faas remove faceanalyzerfn && faas remove mobilenetfn'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        if (action == 0):
            command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2 --constraint "kubernetes.io/hostname=gworker-01"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        elif (action == 1):
            command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2 --constraint "kubernetes.io/hostname=gworker-02"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        elif (action == 2):
            command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2 --constraint "kubernetes.io/hostname=gworker-03"'
            subprocess.getoutput(command)
            time.sleep(3)
        elif (action == 3):
            command = 'faas deploy -f ../../functions/version4/functions.yml --filter=monolith2 --constraint "kubernetes.io/hostname=gworker-04"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        elif (action == 4):
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=framerfn --constraint "kubernetes.io/hostname=gworker-01"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=facedetectorfn2 --constraint "kubernetes.io/hostname=gworker-01"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=faceanalyzerfn --constraint "kubernetes.io/hostname=gworker-01"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=mobilenetfn --constraint "kubernetes.io/hostname=gworker-01"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        elif (action == 5):
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=framerfn --constraint "kubernetes.io/hostname=gworker-02"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=facedetectorfn2 --constraint "kubernetes.io/hostname=gworker-02"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=faceanalyzerfn --constraint "kubernetes.io/hostname=gworker-02"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=mobilenetfn --constraint "kubernetes.io/hostname=gworker-02"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        elif (action == 6):
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=framerfn --constraint "kubernetes.io/hostname=gworker-03"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=facedetectorfn2 --constraint "kubernetes.io/hostname=gworker-03"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=faceanalyzerfn --constraint "kubernetes.io/hostname=gworker-03"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=mobilenetfn --constraint "kubernetes.io/hostname=gworker-03"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        elif (action == 7):
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=framerfn --constraint "kubernetes.io/hostname=gworker-04"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=facedetectorfn2 --constraint "kubernetes.io/hostname=gworker-04"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=faceanalyzerfn --constraint "kubernetes.io/hostname=gworker-04"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            command = 'faas deploy -f ../../functions/version1/functions.yml --filter=mobilenetfn --constraint "kubernetes.io/hostname=gworker-04"'
            subprocess.getoutput(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)
        else:
            print('no action taken')
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