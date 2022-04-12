import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from circuit.circuit import Circuit
from circuit.spline import spline
from affichage.camera import Camera, Camera_premiere_personne, Camera_troisieme_personne, Camera_fixe_dirigee

circuit = Circuit(spline)
circuit.cabine.vitesse=3

fig = plt.figure()
plt.style.use('dark_background')
camera_globale = Camera(circuit)
ax1 = fig.add_subplot(1, 4, 1, projection='3d')
ax1.grid(False)
camera_tp = Camera_troisieme_personne(circuit)
ax2 = fig.add_subplot(1, 4, 2, projection='3d')
ax2.grid(False)
camera_pp = Camera_premiere_personne(circuit)
ax3 = fig.add_subplot(1, 4, 3, projection='3d')
ax3.grid(False)
camera_fd = Camera_fixe_dirigee(circuit,[np.array([1,1,1])])
ax4 = fig.add_subplot(1, 4, 4, projection='3d')
ax4.grid(False)

def draw_global(ax):
    spline_reliee = np.append(circuit.spline[:,:],circuit.spline[:1,:],axis=0)
    ax.plot3D(spline_reliee[:,0],spline_reliee[:,1],spline_reliee[:,2],linestyle='-')#, marker='o')
    pos_cabine = circuit.get_pos_cabine()
    ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
    ax.grid(False)
    ax.set_axis_off()

def animate(i):
    camera_globale.draw(ax1)
    camera_tp.draw(ax2)
    camera_pp.draw(ax3)
    camera_fd.draw(ax4)
    circuit.deplace()

# run the animation

ani = FuncAnimation(fig, animate, interval=20, repeat=True)

plt.show()
