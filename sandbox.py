import matplotlib.pyplot as plt

import numpy as np

def makeFig():
    plt.scatter(xList,yList) # I think you meant this

plt.ion() # enable interactivity
fig=plt.figure() # make a figure

xList=list()
yList=list()

for i in np.arange(50):
    y=np.random.random()
    xList.append(i)
    yList.append(y)
    makeFig()
    plt.draw()
    #makeFig()      The drawnow(makeFig) command can be replaced
    #plt.draw()     with makeFig(); plt.draw()
    plt.pause(0.001)
    for i in range(100000):
        print(1)