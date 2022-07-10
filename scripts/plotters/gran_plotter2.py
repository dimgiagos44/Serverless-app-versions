import matplotlib.pyplot as plt
import numpy as np

x = ['version1', 'version2', 'version3', 'version4']

times7 = [15, 15.2, 16.3, 15]
times16 = [20, 20.3, 20.15, 15.4]
times32 = [28.3, 28.3, 27.8, 22.4]
times65 = [66.5, 67.2, 58.3, 46]

plt.plot(0, 15, marker="o", color="red")
plt.plot(0, 20, marker="o", color="red")
plt.plot(0, 28.3, marker="o", color="red")
plt.plot(0, 66.5, marker="o", color="red")

plt.plot(1, 15.2, marker="o", color="red")
plt.plot(1, 20.3, marker="o", color="red")
plt.plot(1, 28.3, marker="o", color="red")
plt.plot(1, 67.2, marker="o", color="red")

plt.plot(2, 16.3, marker="o", color="red")
plt.plot(2, 20.15, marker="o", color="red")
plt.plot(2, 27.8, marker="o", color="red")
plt.plot(2, 58.3, marker="o", color="red")

plt.plot(3, 15, marker="o", color="red")
plt.plot(3, 15.4, marker="o", color="red")
plt.plot(3, 22.4, marker="o", color="red")
plt.plot(3, 46, marker="o", color="red")

width = 0.35  # the width of the bars

plt.xlabel('Granularity Levels')
plt.ylabel('Execution Time (sec)')
plt.title('Granularity-based Workflow Execution - FaasFlow')
plt.plot(x, times7, label='7 frames', linestyle="-.")
plt.plot(x, times16, label='16 frames', linestyle="-.")
plt.plot(x, times32, label='32 frames', linestyle="-.")
plt.plot(x, times65, label='65 frames', linestyle="-.")
plt.legend()
plt.savefig('granularity.png')