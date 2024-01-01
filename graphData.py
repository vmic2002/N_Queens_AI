import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np

# Load your data from 'data.csv'
points = pd.read_csv('data.csv')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = points['N'].values
y = points['numThreads'].values
z = points['time'].values

# Create a unique color for each numThreads value
unique_numThreads = np.unique(y)
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_numThreads)))

for i, numThread in enumerate(unique_numThreads):
    mask = y == numThread
    ax.scatter(x[mask], y[mask], z[mask], c=[colors[i]], label=f'numThreads = {numThread}', marker='o')

ax.set_xlabel('N')
ax.set_ylabel('numThreads')
ax.set_zlabel('time (sec)')

# Add a legend to distinguish different numThreads values
#ax.legend()


# Set the "time" axis to use a logarithmic scale
#ax.set_zscale('log')



plt.show()

