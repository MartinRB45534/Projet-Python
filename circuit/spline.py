import numpy as np
from circuit.spline_generator import *
from circuit.spline_opener import *

cospi4 = np.sqrt(1/2)
control = np.array([[1,0,0],[3,0,0],[4,1,1],[4,3,1],[3,4,0],[1,4,0],[0,3,0],[0.1,2,0],[0.075,2-cospi4/2,(1-cospi4)/2],[0.05,1.5,0.5],[0.025,2-cospi4/2,(1+cospi4)/2],[0,2,1],[-0.025,2+cospi4/2,(1+cospi4)/2],[-0.05,2.5,0.5],[-0.075,2+cospi4/2,1-cospi4],[-0.1,2,0],[0,1,0]])

#control = np.array([[1,1,1],[1,1,2],[1,2,2],[1,2,1],[2,2,1],[2,2,2],[2,1,2],[2,1,1]])

#control = np.array([[1,1,1],[1,2,1],[2,2,1],[2,1,1]])

spline = cree_spline(control)

