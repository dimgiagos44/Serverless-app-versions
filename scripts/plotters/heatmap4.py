import numpy as np
import matplotlib
import matplotlib.pyplot as plt

frames = ['7', '16', '32', '65']
configs = ['cheetara2', 'cheetara1', 'coroni', 'liono', 'davinci']

#frames = len([])
#configs= len([[]])
times = np.array([[70.71, 77.58, 94.36, 127.83],
                    [44.39, 50.91, 64.23, 89.66],
                    [30.10, 34.58, 45.01, 64.42],
                    [19.83, 24.81, 34.58, 50.91],
                    [18.98, 22.22, 30.99, 48.10]])
fig, ax = plt.subplots()
im = ax.imshow(times)

# Show all ticks and label them with the respective list entries
#ax.set_xticks(np.arange(len(farmers)), labels=farmers)
#ax.set_yticks(np.arange(len(vegetables)), labels=vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(configs)):
    for j in range(len(frames)):
        text = ax.text(j, i, times[i, j],
                       ha="center", va="center", color="w")

ax.set_title('Version4 latencies (sec)')
#fig.tight_layout()
plt.xticks(np.arange(len(frames)), labels=frames)
plt.yticks(np.arange(len(configs)), labels=configs)
ax.set_xlabel('# Queue-workers')
ax.set_ylabel('Placement configuration')
plt.show()

plt.savefig('plot3.png')