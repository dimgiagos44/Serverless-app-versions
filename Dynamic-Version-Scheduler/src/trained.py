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
from scheduler import CustomEnv


    
#customEnv = CustomEnv()
models_dir = "./models/"
model_path = f"{models_dir}/05_20_13/model_final.zip"

#model = DQN.load(model_path, env=customEnv)
model = DQN.load(model_path, env=CustomEnv())
'''
episodes = 5


for ep in range(episodes):
    obs = customEnv.reset()

    action, _ = model.predict(obs)
    obs, reward, done, info = customEnv.step(action)
    print(obs, reward, done, info)

customEnv.close()
'''


print(model.get_parameters())
print('SOOOOOOOOOOOOOOOOOOOOOOS')