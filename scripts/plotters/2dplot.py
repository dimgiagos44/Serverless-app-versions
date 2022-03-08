import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig = plt.figure()

# syntax for 3-d projection
ax = plt.axes(projection='3d')

# defining axes
# 1 queue-worker
x1_7 = [1, 1, 1]
y1_7 = [1, 2, 4]
z1_7 = [1.62, 4.75, 5]
z1_16 = [3.51, 12, 12]
z1_32 = [7.04, 25.25, 25.5]
z1_65 = [14.18, 52.3, 52]

# 2 queue-workers
x2_7 = [2, 2, 2, 2, 2]
y2_7 = [1, 2, 4, 8, 16]
z2_7 = [2.75, 2.25, 2.25, 2.75, 3]
z2_16 = [5.5, 5.75, 6.6, 5.66, 7]
z2_32 = [12.75, 13.66, 12.3, 12.3, 13.7]
z2_65 = [26.5, 26, 26, 25.5, 28.3]

# 4 queue-workers
x4_7 = [4, 4, 4, 4, 4]
y4_7 = [1, 2, 4, 8, 16]
z4_7 = [1.75, 1.25, 1.5, 1, 1.2]
z4_16 = [3.75, 3, 3, 3, 3.5]
z4_32 = [7.5, 7, 6, 6.3, 7]
z4_65 = [13.66, 13, 12.7, 12.4, 14]

# 8 queue-workers

x8_7 = [8, 8, 8, 8, 8]
y8_7 = [1, 2, 4, 8, 16]
z8_7 = [1, 1, 1, 1, 1]
z8_16 = [1.5, 1.7, 1.7, 1.7, 1.7]
z8_32 = [4.2, 3.8, 3.8, 3.5, 3.8]
z8_65 = [7.25, 7, 7, 7, 8]

# 16 queue-workers

x16_7 = [16, 16, 16, 16, 16]
y16_7 = [1, 2, 4, 8, 16]
z16_7 = [1.2, 1, 1, 1, 1.2]
z16_16 = [2, 1.7, 1.5, 1.5, 1.5]
z16_32 = [4.3, 4, 3.3, 3.3, 5]
z16_65 = [8, 7, 7.2, 6.9, 7]

ax.scatter(x1_7, y1_7, z1_7, c='red', marker='v')
ax.scatter(x1_7, y1_7, z1_16, c='green', marker='v')
ax.scatter(x1_7, y1_7, z1_32, c='blue', marker='v')
ax.scatter(x1_7, y1_7, z1_65, c='black', marker='v')

ax.scatter(x2_7, y2_7, z2_7, c='red', marker='o')
ax.scatter(x2_7, y2_7, z2_16, c='green', marker='o')
ax.scatter(x2_7, y2_7, z2_32, c='blue', marker='o')
ax.scatter(x2_7, y2_7, z2_65, c='black', marker='o')

ax.scatter(x4_7, y4_7, z4_7, c='red', marker='x')
ax.scatter(x4_7, y4_7, z4_16, c='green', marker='x')
ax.scatter(x4_7, y4_7, z4_32, c='blue', marker='x')
ax.scatter(x4_7, y4_7, z4_65, c='black', marker='x')

ax.scatter(x8_7, y8_7, z8_7, c='red', marker='*')
ax.scatter(x8_7, y8_7, z8_16, c='green', marker='*')
ax.scatter(x8_7, y8_7, z8_32, c='blue', marker='*')
ax.scatter(x8_7, y8_7, z8_65, c='black', marker='*')

ax.scatter(x16_7, y16_7, z16_7, c='red', marker='P')
ax.scatter(x16_7, y16_7, z16_16, c='green', marker='P')
ax.scatter(x16_7, y16_7, z16_32, c='blue', marker='P')
ax.scatter(x16_7, y16_7, z16_65, c='black', marker='P')

plt.xticks([1, 2, 4, 8, 16])
plt.yticks([1, 2, 4, 8, 16])
plt.title('Facedetector latency in reference to queue-workers')
ax.set_zticks(np.arange(1, 30, 4))
ax.set_xlabel('# Queue-workers')
ax.set_ylabel('# Facedetector replicas')
ax.set_zlabel('Time (s)')

red_patch = mpatches.Patch(color='red', label='7_frames')
green_patch = mpatches.Patch(color='green', label='16_frames')
blue_patch = mpatches.Patch(color='blue', label='32_frames')
black_patch = mpatches.Patch(color='black', label='65_frames')
ax.legend(handles=[red_patch, green_patch, blue_patch, black_patch], bbox_to_anchor=(1, 0.2))

plt.savefig('plot.png')