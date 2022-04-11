import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from circuit.circuit import Circuit
from circuit.spline import spline
from affichage.camera import Camera, Camera_troisieme_personne

circuit = Circuit(spline)
circuit.cabine.vitesse=3

fig = plt.figure()
plt.style.use('dark_background')
camera_globale = Camera(circuit)
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.grid(False)
camera_tp = Camera_troisieme_personne(circuit)
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.grid(False)

def draw_global(ax):
    spline_reliee = np.append(circuit.spline[:,:],circuit.spline[:1,:],axis=0)
    ax.plot3D(spline_reliee[:,0],spline_reliee[:,1],spline_reliee[:,2],linestyle='-')#, marker='o')
    pos_cabine = circuit.get_pos_cabine()
    ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
    ax.grid(False)
    ax.set_axis_off()
    
def draw_tp(ax):
    spline_reliee = np.append(circuit.spline[:,:],circuit.spline[:1,:],axis=0)
    ax.plot3D(spline_reliee[:,0],spline_reliee[:,1],spline_reliee[:,2],linestyle='-')#, marker='o')
    pos_cabine = circuit.get_pos_cabine()
    dir_cabine = circuit.get_dir_cabine()
    a=np.array([1,0])
    b=dir_cabine[:2]/np.linalg.norm(dir_cabine[:2]) # On ne veut que les coordonées horizontales
    xlim=ax.get_xlim()
    ylim=ax.get_ylim()
    zlim=ax.get_zlim()
    ax.set_xlim(xlim+pos_cabine[0]-np.mean(xlim))
    ax.set_ylim(ylim+pos_cabine[1]-np.mean(ylim))
    ax.set_zlim(zlim+pos_cabine[2]-np.mean(zlim))

    ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
    
    ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
    ax.grid(False)
    ax.set_axis_off()

def draw_local(ax):
    pass

def animate(i):
    ax1.clear()
    ax2.clear()
    camera_globale.draw(ax1)
    camera_tp.draw(ax2)
    circuit.deplace()

# run the animation

ani = FuncAnimation(fig, animate, interval=20, repeat=True)

plt.show()
