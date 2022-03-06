import numpy as np
import matplotlib
import matplotlib.pyplot as plt

workers = ['1', '2', '4', '8', '16']
replicas = ['0-0-4', '0-4-0', '4-0-0', '0-0-0']

times = np.array([[15.21, 26, 18, 11, 10],
                    [14.85, 27, 14, 8.3, 8],
                    [14.31, 26.7, 16, 8.4, 8],
                    [14.18, 26.5, 13.66, 7.25, 8]])


fig, ax = plt.subplots()
im = ax.imshow(times)

# Show all ticks and label them with the respective list entries
#ax.set_xticks(np.arange(len(farmers)), labels=farmers)
#ax.set_yticks(np.arange(len(vegetables)), labels=vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(replicas)):
    for j in range(len(workers)):
        text = ax.text(j, i, times[i, j],
                       ha="center", va="center", color="w")

ax.set_title('Facedetector latencies (sec) - frames: 65')
#fig.tight_layout()
plt.xticks(np.arange(len(workers)), labels=workers)
plt.yticks(np.arange(len(replicas)), labels=replicas)
ax.set_xlabel('# Queue-workers')
ax.set_ylabel('Cluster pressure configuration')
plt.show()

plt.savefig('plot3.png')