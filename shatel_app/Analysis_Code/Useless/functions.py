import numpy as np
import matplotlib.pyplot as plt
def bar_plot(H, title, ylabel):
    #print H[0][1]
    labels = [row[0] for row in H]
    values = [row[1] for row in H]
    y_pos = np.arange(len(labels))
    plt.xticks(y_pos, labels, rotation = 15, ha="right", size=9.5)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.bar(y_pos, values, align = 'center', alpha=0.5, color='#FFC222')
    plt.show()  