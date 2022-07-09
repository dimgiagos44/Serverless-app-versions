import matplotlib.pyplot as plt
import numpy as np

labels = ['7', '16', '32', '65']
version1 = {'0': [23.4, 32.09, 46.96, 79.9], '10': [22.3, 32.62, 50.56, 84.51],
            '50': [24.82, 33.65, 51.36, 85.12], '80': [45.39, 56.18, 76.37, 117.97]}

version4 = {'0': [17.18, 21.3, 28.64, 42.08], '10': [17.78, 21.27, 28.62, 42.29],
            '50': [19.72, 23.32, 31.01, 45.78], '80': [38.88, 43.6, 54.39, 75.17]}



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
plt.savefig('interference_davinci.png')