from cv2 import MARKER_SQUARE, MARKER_TILTED_CROSS, MARKER_TRIANGLE_UP
import matplotlib.pyplot as plt
import numpy as np


barWidth = 0.30
fig, ax = plt.subplots(figsize =(12, 8))

# set height of bar

labels = ['framer', 'facedetector', 'faceanalyzer', 'mobilenet', 'version1', 'inference'
, 'version2', 'biginference', 'version3', 'monolith', 'version4']
height = [180, 300, 410, 760, 1650, 2300, 2780, 2320, 2500, 3950, 3950]
color = ['blue', 'red', 'yellow', 'pink', 'black', 'silver', 'black', 'purple', 'black',
'cyan', 'black']


br1 = np.arange(len(height))
rects1 = plt.bar(br1, height, color = color, width = barWidth,
        edgecolor ='grey', label ='')

plt.xlabel('functions', fontweight ='bold', fontsize = 15)
plt.ylabel('RAM allocated by container(MB)', fontweight ='bold', fontsize = 15)
plt.xticks(br1, labels)
ax.bar_label(rects1, padding=3)

x = [4, 6, 8, 10]
y = [1650, 2780, 2500, 3950]
plt.plot(x, y, marker='o')


# function to show the plot
#plt.show()
plt.legend()
plt.show()
plt.savefig('plot.png')