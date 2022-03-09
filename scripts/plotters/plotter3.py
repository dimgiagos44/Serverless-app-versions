from cv2 import MARKER_SQUARE, MARKER_TILTED_CROSS, MARKER_TRIANGLE_UP
import matplotlib.pyplot as plt
import numpy as np

ticks = [1, 2]

barWidth = 0.12
fig, ax = plt.subplots(figsize =(12, 8))

# set height of bar

labels = ['7_frames', '16_frames', '32_frames', '65_frames']
version1_1 = [25.29, 34.90, 50.29, 83.85]
version1_2 = [23.15, 28.89, 35.58, 59.59]
version1_4 = [21.18, 23.52, 30.43, 43.76]
version1_8 = [20.25, 24.59, 29.33, 37.32]
version1_16 = [20.23, 22.52, 27.05, 36.92]
version4 = [19.83, 24.81, 33.66, 47.8]

br1 = np.arange(len(version1_1))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]

rects1 = plt.bar(br1, version1_1, color ='r', width = barWidth,
        edgecolor ='grey', label ='version1_1')
rects2 = plt.bar(br2, version1_2, color ='g', width = barWidth,
        edgecolor ='grey', label ='version1_2')
rects3 = plt.bar(br3, version1_4, color ='b', width = barWidth,
        edgecolor ='grey', label ='version1_4')
rects4 = plt.bar(br4, version1_8, color ='y', width = barWidth,
        edgecolor ='grey', label ='version1_8')
rects5 = plt.bar(br5, version1_16, color ='pink', width = barWidth,
        edgecolor ='grey', label ='version1_16')
rects6 = plt.bar(br6, version4, color ='black', width = barWidth,
        edgecolor ='grey', label ='version4')

plt.xlabel('# of frames \n (No pressure)', fontweight ='bold', fontsize = 15)
plt.ylabel('Average execution time (sec)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(version1_1))], labels)

ax.bar_label(rects1, padding=3, )
#ax.bar_label(rects2, padding=3)
#ax.bar_label(rects3, padding=3)
#ax.bar_label(rects4, padding=5)
#ax.bar_label(rects5, padding=3)
ax.bar_label(rects6, padding=5)
# function to show the plot
#plt.show()
plt.title('Version1 with multiple queue-workers & Version4', fontsize=20, 
        color='white', backgroundcolor='green', pad='2.0')
plt.legend()
plt.show()
plt.savefig('plot.png')