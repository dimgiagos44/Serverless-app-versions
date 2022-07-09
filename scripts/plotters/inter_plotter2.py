import matplotlib.pyplot as plt
import numpy as np

labels = ['7', '16', '32', '65']
version1 = {'0': [25.71, 34.37, 51.27, 86.35], '10': [26.66, 35.36, 51.6, 84.2],
            '50': [29.33, 38.65, 55.36, 87.28], '80': [50.04, 63.19, 83.67, 128.33]}

version4 = {'0': [21.43, 25.29, 35.23, 52.14], '10': [21.11, 25.18, 34.36, 51.53],
            '50': [24.98, 28.91, 37.98, 54.61], '80': [51.36, 53.29, 65.47, 100.61]}



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
plt.savefig('interference_liono.png')