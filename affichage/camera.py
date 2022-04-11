from calendar import c
import numpy as np

class Camera:
    def __init__(self,circuit):
        self.circuit = circuit
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)

    def draw(self,ax):
        ax.plot3D(self.spline_reliee[:,0],self.spline_reliee[:,1],self.spline_reliee[:,2],linestyle='-')#, marker='o')
        pos_cabine = self.circuit.get_pos_cabine()
        ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
        ax.grid(False)
        ax.set_axis_off()
        
class Camera_troisieme_personne(Camera):
    def draw(self,ax):
        Camera.draw(self,ax)
        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        a=np.array([1,0])
        b=dir_cabine[:2]/np.linalg.norm(dir_cabine[:2]) # On ne veut que les coordonées horizontales
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        zlim=ax.get_zlim()
        ax.set_xlim(xlim+pos_cabine[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_cabine[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_cabine[2]-np.mean(zlim))
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        
class Camera_premiere_personne(Camera):
    def reduit_spline(self):
        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        

    def draw(self,ax):
        self.reduit_spline()
        Camera.draw(self,ax)
        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        a=np.array([1,0])
        b=dir_cabine[:2]/np.linalg.norm(dir_cabine[:2]) # On ne veut que les coordonées horizontales
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        zlim=ax.get_zlim()
        ax.set_xlim(xlim+pos_cabine[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_cabine[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_cabine[2]-np.mean(zlim))
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)