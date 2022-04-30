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


    
customEnv = CustomEnv()
models_dir = "./models/"
model_path = f"{models_dir}/name.zip"

model = DQN.load(model_path, env=customEnv)

episodes = 5
