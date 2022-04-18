from stable_baselines3 import DQN

model = DQN.load("./models/04_15_17/model.zip")

print(model)