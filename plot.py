import matplotlib.pyplot as plt
import numpy as np

# With Indexing
xpoints_indexing = np.array([0,1,2,3,4,5,6,7,8,9,10])
ypoints_indexing=np.array([0.001,0.52,0.57,1.28,3.6,3.8,4,3.93,4.10,4.3,4.15])

# Without Indexing
xpoints = np.array([0,1,2,3,4,5,6,7,8,9,10])
ypoints = np.array([192.04,194.63,194.63,220,200.9,195,197.78,194,194,193.3,194])

plt.plot(xpoints_indexing,ypoints_indexing)
plt.plot(xpoints,ypoints)
plt.show()