
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

workers = ['1', '2', '4', '8', '16']
configs = ['dav-lio-coroni', 'dav-liono', 'coroni', 'liono', 'davinci']

#workers = len([])
#configs= len([[]])
times = np.array([[82.82, 55.32, 43.82, 39.82, 36.1],
                    [79.49, 51.33, 36.83, 33.34, 32.3],
                    [90.05, 62.78, 50.18, 46.26, 44.16],
                    [83.85, 59.59, 43.76, 37.32, 36.92],
                    [80.09, 49.86, 37.41, 34.41, 31.97]])
'''
times = np.array([[49.37, 35.37, 29.87, 28.37, 27.87],
                    [47.28, 33.95, 26.12, 23.62, 23.62],
                    [56.76, 44, 36.3, 35.28, 34.48],
                    [50.29, 35.58, 30.43, 29.33, 27.05],
                    [45.31, 32.62, 26.32, 24.51, 23.31]])              
                    
                       
times = np.array([[32.66, 27, 23, 22, 22],
                    [31.13, 25.13, 20.80, 19.80, 18.80],
                    [40.98, 34.92, 31.04, 30.44, 29.45],
                    [34.90, 28.89, 23.52, 24.59, 22.52],
                    [30.34, 23.83, 20.01, 19.42, 18.56]])


times = np.array([[25.98, 21.98, 20.98, 20.68, 20.7],
                    [22.67, 20.01, 18.34, 17.01, 17.51],
                    [33.67, 29.31, 27.65, 27.29, 27.51],
                    [25.29, 23.15, 21.18, 20.25, 20.23],
                    [22.46, 19.05, 17.85, 17.17, 16.42]])
'''
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
    for j in range(len(workers)):
        text = ax.text(j, i, times[i, j],
                       ha="center", va="center", color="w")

ax.set_title('Version1 latencies (sec) - frames: 65')
#fig.tight_layout()
plt.xticks(np.arange(len(workers)), labels=workers)
plt.yticks(np.arange(len(configs)), labels=configs)
ax.set_xlabel('# Queue-workers')
ax.set_ylabel('Placement configuration')
plt.show()

plt.savefig('plot3.png')