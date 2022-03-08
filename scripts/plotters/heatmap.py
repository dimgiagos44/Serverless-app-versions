import numpy as np
import matplotlib
import matplotlib.pyplot as plt

workers = ['1', '2', '4', '8', '16']
replicas = ['16', '8', '4', '2', '1']

times = np.array([[1.2, 1, 1, 1, 1.2],
                    [1, 1, 1, 1, 1.4],
                    [1.75, 1.25, 1.5, 1, 1.2],
                    [2.75, 2.25, 2.25, 2.75, 3],
                    [1.62, 4.75, 5, 5, 5]])


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

ax.set_title('Facedetector latencies (sec) - frames: 7')
#fig.tight_layout()
plt.xticks(np.arange(len(workers)), labels=workers)
plt.yticks(np.arange(len(replicas)), labels=replicas)
ax.set_xlabel('# Facedetector replicas')
ax.set_ylabel('# Queue-workers')
plt.show()

plt.savefig('plot2.png')