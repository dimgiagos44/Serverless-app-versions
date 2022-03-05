import numpy as np
import matplotlib
import matplotlib.pyplot as plt

workers = ['1', '2', '4', '8', '16']
replicas = ['16', '8', '4', '2', '1']

times = np.array([[3, 3, 3, 3, 3],
                    [5, 6, 5, 5, 5.8],
                    [12, 11, 11, 11, 11],
                    [24, 23, 24, 23, 23],
                    [9.42, 46, 48, 48, 48]])


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

ax.set_title('Faceanalyzer-Mobilenet latencies (sec) - frames: 65')
#fig.tight_layout()
plt.xticks(np.arange(len(workers)), labels=workers)
plt.yticks(np.arange(len(replicas)), labels=replicas)
ax.set_xlabel('# Faceanalyzer-Mobilenet replicas')
ax.set_ylabel('# Queue-workers')
plt.show()

plt.savefig('plot3.png')