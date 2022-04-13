import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from circuit.circuit import Circuit
from circuit.spline_generator import cree_spline
from circuit.spline_opener import readfile
from affichage.camera import Camera, Camera_premiere_personne, Camera_troisieme_personne, Camera_fixe_dirigee

circuit = Circuit(cree_spline(readfile('rollercoaster.mycustomfileextension')))
circuit.cabine.vitesse=3

fig = plt.figure()
plt.style.use('dark_background')
camera_globale = Camera(circuit) #La caméra classique
ax1 = fig.add_subplot(1, 4, 1, projection='3d')
ax1.grid(False)
camera_tp = Camera_troisieme_personne(circuit) #La caméra qui suit la cabine de loin
ax2 = fig.add_subplot(1, 4, 2, projection='3d')
ax2.grid(False)
camera_pp = Camera_premiere_personne(circuit) #La caméra qui suit la cabine de près
ax3 = fig.add_subplot(1, 4, 3, projection='3d')
ax3.grid(False)
camera_fd = Camera_fixe_dirigee(circuit,[np.array([4,-4,0]),np.array([15,-5,0]),np.array([9,5,0]),np.array([3,5,0])]) #Les caméras qui tournent pour suivre la cabine
ax4 = fig.add_subplot(1, 4, 4, projection='3d')
ax4.grid(False)

def animate(i):
    camera_globale.draw(ax1)
    camera_tp.draw(ax2)
    camera_pp.draw(ax3)
    camera_fd.draw(ax4)
    circuit.deplace()

ani = FuncAnimation(fig, animate, interval=20, repeat=True)

plt.show()
