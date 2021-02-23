import matplotlib.pyplot as plt
import numpy as np
distanceData = []
timeData = []


def update(distance, time):
    plt.show()
    distanceData.append(distance)
    timeData.append(time)

    plt.plot(distanceData,timeData)
    plt.show()
