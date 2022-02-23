from cv2 import MARKER_SQUARE, MARKER_TILTED_CROSS, MARKER_TRIANGLE_UP
import matplotlib.pyplot as plt
import numpy as np

ticks = [1, 2]

barWidth = 0.20
fig, ax = plt.subplots(figsize =(12, 8))

# set height of bar
'''
labels = ['single-16', 'multi-16', 'single-32', 'multi-32', 'single-65', 'multi-65']
after_framer = [15.52, 15.59, 16.51, 16.38, 18.91, 19.49]
after_face = [20.21, 21.47, 26.48, 28.17, 37.99, 39.97]
after_inf = [25.93, 26.90, 37.21, 39.45, 59.81, 62.24]
total = [26.58, 27.56, 37.91, 40.16, 60.49, 62.89]

rects1 = plt.bar(br1, after_framer, color ='r', width = barWidth,
        edgecolor ='grey', label ='after_framer')
rects2 = plt.bar(br2, after_face, color ='g', width = barWidth,
        edgecolor ='grey', label ='after_face')
rects3 = plt.bar(br3, after_inf, color ='b', width = barWidth,
        edgecolor ='grey', label ='after_inf')
rects4 = plt.bar(br4, total, color ='y', width = barWidth,
        edgecolor ='grey', label ='total')
'''

labels = ['16_frames', '32_frames', '65_frames']
version1_single_1 = [47.81, 61.58, 85.77]
version1_multi_1 = [48.42, 58.82, 82.89]
version1_multi_3 = [48.14, 59.92, 85.41]
version4 = [42.88, 52.55, 69.23]

br1 = np.arange(len(version1_single_1))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]


rects1 = plt.bar(br1, version1_single_1, color ='r', width = barWidth,
        edgecolor ='grey', label ='version1_single_1_davinci')
rects2 = plt.bar(br2, version1_multi_1, color ='g', width = barWidth,
        edgecolor ='grey', label ='version1_multi_1')
rects3 = plt.bar(br3, version1_multi_3, color ='b', width = barWidth,
        edgecolor ='grey', label ='version1_multi_3')
rects4 = plt.bar(br4, version4, color ='y', width = barWidth,
        edgecolor ='grey', label ='version4_davinci')

plt.xlabel('1-1-1', fontweight ='bold', fontsize = 15)
plt.ylabel('Average exec time (s)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(version1_single_1))], labels)

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
ax.bar_label(rects4, padding=3)
# function to show the plot
#plt.show()
plt.legend()
plt.show()
plt.savefig('plot.png')