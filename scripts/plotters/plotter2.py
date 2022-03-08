from cv2 import MARKER_SQUARE, MARKER_TILTED_CROSS, MARKER_TRIANGLE_UP
import matplotlib.pyplot as plt

ticks = [1, 2]
labels = ['Single-node', 'Multi-node']
# line 1 points
x1 = [1, 2]
#y1 = [731, 511, 752, 897]
#y1 = [704, 499, 678, 739]
y1_avg = [14.81, 14.88]

# plotting the line 1 points
plt.plot(x1, y1_avg, label = "url1_avg", marker = "o", color = "blue", markersize=8)
 
# line 2 points
x4 = [1, 2]
#y4 = [611, 471, 684, 852]
#y4 = [704, 487, 642, 869]
y4_avg = [21.27, 22.56]
# plotting the line 2 points
plt.plot(x4, y4_avg, label = "url4_avg", marker = "o", color = "red", markersize=8, ls='--')

x5 = [1, 2]
#y5 = [711, 538, 612, 763]
y5_avg = [31.22, 31.95]
plt.plot(x5, y5_avg, label = "url5_avg", marker = "o", color = "green", markersize=8, ls='--')


x6 = [1, 2]
y6_avg = [68.33, 68.73]
plt.plot(x6, y6_avg, label = "url6_avg", marker = "o", color = "grey", markersize=8, ls='--')

x7 = [1, 2]
y7_avg = [108.57, 106.77]
plt.plot(x7, y7_avg, label = 'url7_avg', marker = "o", color = "black", markersize=8, ls="--")

# naming the x axis
plt.xlabel('Workflow Versions')
plt.xticks(ticks, labels)
# naming the y axis
plt.ylabel('Average execution time (s)')
# giving a title to my graph
#plt.title('Version1 vs Version4 execution duration')
plt.title('Single-node vs Multi-node version1(3)') 
# show a legend on the plot
plt.legend()
 
# function to show the plot
#plt.show()

plt.savefig('plot.png')