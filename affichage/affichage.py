from circuit.spline import *

import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot3D(spline[:,0],spline[:,1],spline[:,2],linestyle='-')#, marker='o')
plt.show()