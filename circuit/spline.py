import numpy as np
from circuit.spline_generator import *
from circuit.spline_opener import *

cospi4 = np.sqrt(1/2)
control = np.array([[1,0,0],[3,0,0],[4,1,1],[4,3,1],[3,4,0],[1,4,0],[0,3,0],[0.1,2,0],[0.05,1.5,0.5],[0,2,1],[-0.05,2.5,0.5],[-0.1,2,0],[0,1,0]])

#control = np.array([[1,1,1],[1,1,2],[1,2,2],[1,2,1],[2,2,1],[2,2,2],[2,1,2],[2,1,1]])

#control = np.array([[1,1,1],[1,2,1],[2,2,1],[2,1,1]])

#control = np.array([[2,3,4],[4,1,1],[9,2,4],[1,9,5],[15,5,5]])

spline = cree_spline(control)

