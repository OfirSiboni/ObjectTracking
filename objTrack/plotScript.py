import matplotlib.pyplot as plt
import numpy as np
distanceData = []
timeData = []
'''
This file is part of the FollowMe's program and is protected by the CC BY-NC-ND 3.0 licence.
Written by Ofir Siboni in 2/2021
'''
#TODO: fix overeating
def update(distance, time):
    plt.show()
    distanceData.append(distance)
    timeData.append(time)

    plt.plot(distanceData,timeData)
    plt.show()
