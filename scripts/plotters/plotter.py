from cv2 import MARKER_SQUARE, MARKER_TILTED_CROSS, MARKER_TRIANGLE_UP
import matplotlib.pyplot as plt

ticks = [1, 2, 3, 4]
labels = ['version1(1)', 'version1(3)-single', 'version1(3)-multi', 'version4']
#labels2 = ['version1', 'version2', 'version3', 'version4']
# line 1 points
x1 = [1, 2, 3, 4]
#y1 = [731, 511, 752, 897]
#y1 = [704, 499, 678, 739]
y1_avg = [26.24, 26.19, 26.67, 20.42]

# plotting the line 1 points
plt.plot(x1, y1_avg, label = "16_frames", marker = "*", color = "blue", markersize=8, ls='--')
 
# line 2 points
x4 = [1, 2, 3, 4]
#y4 = [611, 471, 684, 852]
#y4 = [704, 487, 642, 869]
y4_avg = [37.08, 37.30, 37.26, 27.33]
# plotting the line 2 points
plt.plot(x4, y4_avg, label = "32_frames", marker = "o", color = "red", markersize=8, ls='--')

x5 = [1, 2, 3, 4]
#y5 = [711, 538, 612, 763]
y5_avg = [58.41, 60.10, 63.21, 41.46]
plt.plot(x5, y5_avg, label = "65_frames", marker = "D", color = "green", markersize=8, ls='--')


x6 = [1, 2, 3, 4]
y6_avg = [106.75, 110.46, 113.22, 57.98]
#y6_avg2 = [66.34, 67.02, 57.66, 45.39]
plt.plot(x6, y6_avg, label = "130_frames", marker = MARKER_TRIANGLE_UP, color = "grey", markersize=8, ls='--')


# naming the x axis
plt.xlabel('Workflow Versions')
plt.xticks(ticks, labels)
# naming the y axis
plt.ylabel('Average execution time (s)')
# giving a title to my graph
plt.title('Version1 vs Version4 execution duration')
#plt.title('Single node (davinci) executions') 
# show a legend on the plot
plt.legend()
 
# function to show the plot
#plt.show()

plt.savefig('plot.png')