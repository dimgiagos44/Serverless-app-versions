import matplotlib.pyplot as plt
import numpy as np

labels = ['7', '16', '32', '65']
version1 = [23.4, 32.09, 46.96, 79.9]
version4 = [17.18, 21.3, 28.64, 42.08]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, version1, width, label='Version1')
rects2 = ax.bar(x + width/2, version4, width, label='Version4')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Execution time (sec)')
ax.set_xlabel('Input size (# of frames)')

ax.set_title('Granularity-based Workflow Execution Time (Davinci)')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()
plt.savefig('granularity_davinci.png')