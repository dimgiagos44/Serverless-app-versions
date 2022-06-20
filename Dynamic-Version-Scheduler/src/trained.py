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


myenv = CustomEnv(training=False, inputIndex=2, qos=29)
models_dir = "./models/"
model_path = f"{models_dir}/06_18_14/rl_model_300_steps.zip"

model = DQN.load(model_path, myenv)

#obs = myenv.reset()
i = 0
while i < 5:
    action, _ = model.predict(obs)
    obs, reward, done, info = myenv.step(action)
    print(obs, reward, done, info)
    i += 1

