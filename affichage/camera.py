from calendar import c
from operator import itemgetter
import numpy as np

class Camera:
    def __init__(self,circuit):
        self.circuit = circuit
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)

    def draw(self,ax):
        ax.clear()
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
    def points_proches(self,n):
        return [i if 0<=i else i+self.circuit.spline.shape[0] if i<self.circuit.spline.shape[0] else i-self.circuit.spline.shape[0] for i in range(self.circuit.cabine.intervalle-n,self.circuit.cabine.intervalle-n+1)]

    def draw_reduit_spline(self,ax):
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)
        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        affiche_limite = pos_cabine + dir_cabine/np.linalg.norm(dir_cabine)*0.2
        portion_visible=None
        portions_visibles = []
        for i in range(self.spline_reliee.shape[0]-1,-1,-1):
            vect_point = self.spline_reliee[i,:]-affiche_limite
            if sum(vect_point*dir_cabine)<0 or i in self.points_proches(3):
                if portion_visible is None:
                    portion_visible=self.spline_reliee[i:i+1,:]
                else:
                    portion_visible=np.append(portion_visible,self.spline_reliee[i:i+1,:],0)
            else:
                if portion_visible is None:
                    pass
                else:
                    portions_visibles.append(portion_visible)
                    portion_visible = None
        if portion_visible is None:
            pass
        else:
            portions_visibles.append(portion_visible)
        if len(portions_visibles)>1 and (portions_visibles[0][0,:]==portions_visibles[-1][-1,:]).all():
            portions_visibles[0] = np.append(portions_visibles.pop(),portions_visibles[0][1:,:],0)
        for portion in portions_visibles:
            ax.plot3D(portion[:,0],portion[:,1],portion[:,2],linestyle='-')#, marker='o')
        pos_cabine = self.circuit.get_pos_cabine()
        ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
        ax.grid(False)
        ax.set_axis_off()

    def draw(self,ax):
        ax.clear()
        self.draw_reduit_spline(ax)
        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        a=np.array([1,0])
        b=dir_cabine[:2]/np.linalg.norm(dir_cabine[:2]) # On ne veut que les coordonées horizontales
        xlim=np.array(ax.get_xlim())/3
        ylim=np.array(ax.get_ylim())/3
        zlim=np.array(ax.get_zlim())/3
        ax.set_xlim(xlim+pos_cabine[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_cabine[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_cabine[2]-np.mean(zlim))
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)
class Camera_fixe_dirigee(Camera):
    def __init__(self,circuit,positions):
        Camera.__init__(self,circuit)
        self.positions = positions

    def position_proche(self):
        return self.positions[min([[i,np.linalg.norm(self.positions[i]-self.circuit.get_pos_cabine())]for i in range(len(self.positions))],key = itemgetter(1))[0]]

    def points_proches(self,n):
        return [i if 0<=i else i+self.circuit.spline.shape[0] if i<self.circuit.spline.shape[0] else i-self.circuit.spline.shape[0] for i in range(self.circuit.cabine.intervalle-n,self.circuit.cabine.intervalle-n+1)]

    def draw_reduit_spline(self,ax):
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)
        pos_camera = self.position_proche()
        dir_camera = self.circuit.get_pos_cabine()-pos_camera
        affiche_limite = pos_camera
        portion_visible=None
        portions_visibles = []
        for i in range(self.spline_reliee.shape[0]-1,-1,-1):
            vect_point = self.spline_reliee[i,:]-affiche_limite
            if sum(vect_point*dir_camera)>0 or i in self.points_proches(3):
                if portion_visible is None:
                    portion_visible=self.spline_reliee[i:i+1,:]
                else:
                    portion_visible=np.append(portion_visible,self.spline_reliee[i:i+1,:],0)
            else:
                if portion_visible is None:
                    pass
                else:
                    portions_visibles.append(portion_visible)
                    portion_visible = None
        if portion_visible is None:
            pass
        else:
            portions_visibles.append(portion_visible)
        if len(portions_visibles)>1 and (portions_visibles[0][0,:]==portions_visibles[-1][-1,:]).all():
            portions_visibles[0] = np.append(portions_visibles.pop(),portions_visibles[0][1:,:],0)
        for portion in portions_visibles:
            ax.plot3D(portion[:,0],portion[:,1],portion[:,2],linestyle='-')#, marker='o')
        pos_cabine = self.circuit.get_pos_cabine()
        ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
        ax.scatter(np.asarray(self.positions)[:,0],np.asarray(self.positions)[:,1],np.asarray(self.positions)[:,2],marker='o',color='g')
        ax.grid(False)
        ax.set_axis_off()
        return pos_camera,dir_camera

    def draw(self,ax):
        ax.clear()
        pos_camera,dir_camera = self.draw_reduit_spline(ax)
        pos_cabine = self.circuit.get_pos_cabine()
        a=np.array([-1,0])
        b=dir_camera[:2]/np.linalg.norm(dir_camera[:2]) # On ne veut que les coordonées horizontales
        xlim=np.array(ax.get_xlim())/2
        ylim=np.array(ax.get_ylim())/2
        zlim=np.array(ax.get_zlim())/2
        ax.set_xlim(xlim+pos_camera[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_camera[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_camera[2]-np.mean(zlim))
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0)