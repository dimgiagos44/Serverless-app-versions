import matplotlib.pyplot as plt
import numpy as np

labels = ['7', '16', '32', '65']
version1 = {'0': [33.71, 40.66, 57.23, 90.59], '10': [33.71, 40.66, 57.23, 90.59],
            '50': [38.7, 48.38, 67.79, 103.48], '80': [51.29, 62.38, 84.59, 129.84]}

version4 = {'0': [28.46, 32.31, 41.24, 60.19], '10': [29.43, 34.6, 44.31, 64.6],
            '50': [33.83, 39.7, 50.66, 73], '80': [47.33, 55.13, 69.17, 95.2]}



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
plt.savefig('interference_coroni.png')