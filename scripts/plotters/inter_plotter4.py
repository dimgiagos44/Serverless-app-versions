import matplotlib.pyplot as plt
import numpy as np

labels = ['7', '16', '32', '65']
version1 = {'0': [48.85, 57.27, 78.57, 117.1], '10': [51.6, 63.8, 85.14, 127.51],
            '50': [67.7, 80.55, 106.04, 153.45], '80': [100.57, 118.91, 151.19, 218.5]}

version4 = {'0': [44.01, 50.71, 64.47, 89.02], '10': [46.26, 52.62, 67.8, 96.87],
            '50': [62.28, 71.69, 89.09, 119.8], '80': [96.11, 106.72, 131.6, 176.37]}



figure, axis = plt.subplots(2, 2, figsize=(18, 12))


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

rects1 = axis[0, 0].bar(x - width/2, version1['0'], width, label='Version1')
rects2 = axis[0, 0].bar(x + width/2, version4['0'], width, label='Version4')

# Add some text for labels, title and custom x-axis tick labels, etc.
axis[0, 0].set_ylabel('Execution time (sec)')
axis[0, 0].set_xlabel('Input size (# of frames)')

axis[0, 0].set_title('0% pressure')
axis[0, 0].set_xticks(x, labels)
axis[0, 0].legend()

axis[0, 0].bar_label(rects1, padding=3)
axis[0, 0].bar_label(rects2, padding=3)


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

rects1 = axis[0, 1].bar(x - width/2, version1['10'], width, label='Version1')
rects2 = axis[0, 1].bar(x + width/2, version4['10'], width, label='Version4')

# Add some text for labels, title and custom x-axis tick labels, etc.
axis[0, 1].set_ylabel('Execution time (sec)')
axis[0, 1].set_xlabel('Input size (# of frames)')

axis[0, 1].set_title('10% pressure')
axis[0, 1].set_xticks(x, labels)
axis[0, 1].legend()

axis[0, 1].bar_label(rects1, padding=3)
axis[0, 1].bar_label(rects2, padding=3)


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

rects1 = axis[1, 0].bar(x - width/2, version1['50'], width, label='Version1')
rects2 = axis[1, 0].bar(x + width/2, version4['50'], width, label='Version4')

# Add some text for labels, title and custom x-axis tick labels, etc.
axis[1, 0].set_ylabel('Execution time (sec)')
axis[1, 0].set_xlabel('Input size (# of frames)')

axis[1, 0].set_title('50% pressure')
axis[1, 0].set_xticks(x, labels)
axis[1, 0].legend()

axis[1, 0].bar_label(rects1, padding=3)
axis[1, 0].bar_label(rects2, padding=3)

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

rects1 = axis[1, 1].bar(x - width/2, version1['80'], width, label='Version1')
rects2 = axis[1, 1].bar(x + width/2, version4['80'], width, label='Version4')

# Add some text for labels, title and custom x-axis tick labels, etc.
axis[1, 1].set_ylabel('Execution time (sec)')
axis[1, 1].set_xlabel('Input size (# of frames)')

axis[1, 1].set_title('80% pressure')
axis[1, 1].set_xticks(x, labels)
axis[1, 1].legend()

axis[1, 1].bar_label(rects1, padding=3)
axis[1, 1].bar_label(rects2, padding=3)

figure.tight_layout()

#plt.title('Interference-based Workflow Execution Time (Davinci)')
plt.show()
plt.savefig('interference_cheetara.png')