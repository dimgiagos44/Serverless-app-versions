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
from scheduler2 import CustomEnv
import loggers

rewardLogger, actionLogger, timeLogger, stateLogger = loggers.setupDataLoggers()
input_index = 2
qos = 29


myenv = CustomEnv(training=False, inputIndex=input_index, qos=qos)
models_dir = "./models/"
model_path = f"{models_dir}/06_18_21/model_final.zip"

model = DQN.load(model_path, myenv)

obs = myenv.reset()
i = 0
print('INFERENCE')
while i < 50:
    action, _ = model.predict(obs)
    obs, reward, done, info = myenv.step(action)
    i += 1

