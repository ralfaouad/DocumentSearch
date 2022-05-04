import matplotlib.pyplot as plt
import numpy as np

# With Indexing
# xpoints_indexing = np.array([0,1,2,3,4,5,6,7,8,9,10])
# ypoints_indexing=np.array([0.001,0.52,0.57,1.28,3.6,3.8,4,3.93,4.10,4.3,4.15])

# # Without Indexing
# xpoints = np.array([0,1,2,3,4,5,6,7,8,9,10])
# ypoints = np.array([192.04,194.63,194.63,220,200.9,195,197.78,194,194,193.3,194])

# plt.plot(xpoints_indexing,ypoints_indexing,color='r',label="Indexing")
# plt.plot(xpoints,ypoints,color='b',label="No Indexing")
# plt.title("Indexing vs No Indexing Comparison")
# plt.xlabel("Number of hits")
# plt.ylabel("Time (s)")
# # plt.show()

# VSM vs TED text
#!10: VSM 0.0, TED 0.02
#!50: 0.007    0.47
#!100: 0.01  1.65
#!500: 0.04  41.2

figure, axis = plt.subplots(1,2)

figure.suptitle("TED vs VSM comparison")

xpts = np.array([10,50,100,500])

ypts1 = np.array([0.0,0.007,0.01,0.04])
ypts2 = np.array([0.02,0.47,1.65,41.2])

axis[0].plot(xpts,ypts1, color='r', label='VSM')
axis[0].plot(xpts,ypts2, color='b', label='TED')
axis[0].set_title(".txt input")
axis[0].set(xlabel= "Words", ylabel="Time (s)")



ypts11 = np.array([0.007,0.04,0.09,0.24])
ypts22 = np.array([0.04,0.16,0.65,14.6])

axis[1].plot(xpts,ypts11, color='r',label="VSM")
axis[1].plot(xpts,ypts22,color='b', label='TED')
axis[1].set_title(".xml input")
axis[1].set(xlabel= "Nodes", ylabel="Time (s)")


#VSM vs TED xml
#!10: 0.007 0.04
#!50: 0.04  0.16
#!100: 0.09     0.6
#!500: 0.24     14.6




plt.legend()
plt.show()
