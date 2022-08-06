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
from scheduler_fullmap import CustomEnv
import loggers

rewardLogger, actionLogger, timeLogger, stateLogger = loggers.setupDataLoggers()

input_index = 2
qos = 35
myenv = CustomEnv(training=False, inputIndex=input_index, qos=qos)
obs = myenv.reset()

models_dir = "./models_fullmap"
model_path = f"{models_dir}/07_30_12/model_final.zip"
model = DQN.load(model_path, myenv)


i = 0
print('INFERENCE')
while i < 50:
    action, _ = model.predict(obs)
    obs, reward, done, info = myenv.step(action)
    i += 1

myenv.qos = 26
while i < 100:
    action, _ = model.predict(obs)
    obs, reward, done, info = myenv.step(action)
    i += 1

