import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#basic line plot
myarray = np.array([1, 2, 3])
plt.plot(myarray)
plt.xlabel('some x axis')
plt.ylabel('some y axis')
plt.show()