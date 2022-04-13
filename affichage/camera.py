from calendar import c
from operator import itemgetter
import numpy as np

class Camera:
    """La caméra de base"""
    def __init__(self,circuit):
        self.circuit = circuit
        self.spline_reliee = np.append(self.circuit.spline[:,:],self.circuit.spline[:1,:],axis=0) #On a le même point au début et à la fin pour avoir la boucle complète

    def draw(self,ax):
        ax.clear()
        ax.plot3D(self.spline_reliee[:,0],self.spline_reliee[:,1],self.spline_reliee[:,2],linestyle='-')
        pos_cabine = self.circuit.get_pos_cabine()
        ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r')
        ax.grid(False)
        ax.set_axis_off()
        
class Camera_troisieme_personne(Camera):
    """La caméra qui est derrière la cabine, loin"""
    def draw(self,ax):
        Camera.draw(self,ax) #On affiche normalement

        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        a=np.array([1,0])
        b=dir_cabine[:2]/np.linalg.norm(dir_cabine[:2]) # On ne veut que les coordonées horizontales
        c=dir_cabine/np.linalg.norm(dir_cabine)

        #Puis on recentre sur la cabine
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        zlim=ax.get_zlim()
        ax.set_xlim(xlim+pos_cabine[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_cabine[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_cabine[2]-np.mean(zlim))

        #Et on se dirige dans le sens du segment où se trouve la cabine
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        ax.elev = -(np.rad2deg(np.arcsin(c[2])))
class Camera_premiere_personne(Camera):
    """La même, mais proche de la cabine"""
    def points_proches(self,n):
        """Trouve les indices des points proches de la position de la cabine (qu'on ne veut pas effacer)"""
        return [i if 0<=i else i+self.circuit.spline.shape[0] if i<self.circuit.spline.shape[0] else i-self.circuit.spline.shape[0] for i in range(self.circuit.cabine.intervalle-n,self.circuit.cabine.intervalle+n+2)] #On va de -n à +n+1 parce que la cabine est entre +0 et +1

    def draw_reduit_spline(self,ax):
        """Trace le circuit en "cachant" les points "derrière" la caméra"""
        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        affiche_limite = pos_cabine + dir_cabine/np.linalg.norm(dir_cabine)*0.2 #Le point le plus loin qu'on veuille afficher
        portion_visible=None
        portions_visibles = []
        points_proches = self.points_proches(3)
        for i in range(self.spline_reliee.shape[0]):
            vect_point = self.spline_reliee[i,:]-affiche_limite
            if sum(vect_point*dir_cabine)<0 or i in points_proches: #Si le produit scalaire est négatif, le point est "devant" la caméra, on le garde
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
        else: #On rajoute éventuellement la dernière portion
            portions_visibles.append(portion_visible)
        if len(portions_visibles)>1 and (portions_visibles[0][0,:]==portions_visibles[-1][-1,:]).all():
            portions_visibles[0] = np.append(portions_visibles.pop(),portions_visibles[0][1:,:],0) #On reconnecte la première et la dernière portion s'il y a lieu
        for portion in portions_visibles:
            ax.plot3D(portion[:,0],portion[:,1],portion[:,2],linestyle='-') #On affiche chaque portion visible
        pos_cabine = self.circuit.get_pos_cabine()
        ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r') #et la cabine
        ax.grid(False)
        ax.set_axis_off()

    def draw(self,ax):
        ax.clear()
        self.draw_reduit_spline(ax) #Pour donner l'impréssion d'être proche du point, on va retirer ce qui est "derrière"

        pos_cabine = self.circuit.get_pos_cabine()
        dir_cabine = self.circuit.get_dir_cabine()
        a=np.array([1,0])
        b=dir_cabine[:2]/np.linalg.norm(dir_cabine[:2]) # On ne veut que les coordonées horizontales
        c=dir_cabine/np.linalg.norm(dir_cabine)

        #On va aussi recentrer de plus près
        xlim=np.array(ax.get_xlim())/3
        ylim=np.array(ax.get_ylim())/3
        zlim=np.array(ax.get_zlim())/3
        ax.set_xlim(xlim+pos_cabine[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_cabine[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_cabine[2]-np.mean(zlim))

        #On se dirige toujours selon le segment où est la cabine
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        ax.elev = -(np.rad2deg(np.arcsin(c[2])))
class Camera_fixe_dirigee(Camera):
    """Plusieurs caméra fixes qui "suivent" la cabine"""
    def __init__(self,circuit,positions):
        Camera.__init__(self,circuit)
        self.positions = positions

    def position_proche(self):
        """Trouve la caméra la plus proche de la cabine"""
        return self.positions[min([[i,np.linalg.norm(self.positions[i]-self.circuit.get_pos_cabine())]for i in range(len(self.positions))],key = itemgetter(1))[0]]

    def points_proches(self,n):
        """Trouve les indices des points proches de la position de la cabine (qu'on ne veut pas effacer)"""
        return [i if 0<=i else i+self.circuit.spline.shape[0] if i<self.circuit.spline.shape[0] else i-self.circuit.spline.shape[0] for i in range(self.circuit.cabine.intervalle-n,self.circuit.cabine.intervalle+n+2)]

    def draw_reduit_spline(self,ax):
        """Trace le circuit en "cachant" les points "derrière" la caméra"""
        pos_camera = self.position_proche()
        dir_camera = self.circuit.get_pos_cabine()-pos_camera
        affiche_limite = pos_camera #Le point le plus loin qu'on veuille afficher
        portion_visible=None
        portions_visibles = []
        for i in range(self.spline_reliee.shape[0]):
            vect_point = self.spline_reliee[i,:]-affiche_limite
            if sum(vect_point*dir_camera)>0 or i in self.points_proches(3): #Si le produit scalaire est positif, le point est "devant" la caméra, on le garde
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
        else: #On rajoute éventuellement la dernière portion
            portions_visibles.append(portion_visible)
        if len(portions_visibles)>1 and (portions_visibles[0][0,:]==portions_visibles[-1][-1,:]).all():
            portions_visibles[0] = np.append(portions_visibles.pop(),portions_visibles[0][1:,:],0) #On reconnecte la première et la dernière portion s'il y a lieu
        for portion in portions_visibles:
            ax.plot3D(portion[:,0],portion[:,1],portion[:,2],linestyle='-') #On affiche chaque portion visible
        pos_cabine = self.circuit.get_pos_cabine()
        ax.scatter(pos_cabine[0],pos_cabine[1],pos_cabine[2],marker='o',color='r') #et la cabine
        ax.scatter(np.asarray(self.positions)[:,0],np.asarray(self.positions)[:,1],np.asarray(self.positions)[:,2],marker='o',color='g') #et les caméras
        ax.grid(False)
        ax.set_axis_off()
        return pos_camera,dir_camera

    def draw(self,ax):
        ax.clear()
        pos_camera,dir_camera = self.draw_reduit_spline(ax)
        
        a=np.array([-1,0])
        b=dir_camera[:2]/np.linalg.norm(dir_camera[:2]) # On ne veut que les coordonées horizontales
        c=dir_camera/np.linalg.norm(dir_camera)

        #On se centre sur la caméra
        xlim=np.array(ax.get_xlim())/2
        ylim=np.array(ax.get_ylim())/2
        zlim=np.array(ax.get_zlim())/2
        ax.set_xlim(xlim+pos_camera[0]-np.mean(xlim))
        ax.set_ylim(ylim+pos_camera[1]-np.mean(ylim))
        ax.set_zlim(zlim+pos_camera[2]-np.mean(zlim))

        #On se dirige vers la cabine pour qu'elle reste dans le champ de vision
        ax.azim = np.rad2deg(np.sign(np.linalg.det(np.stack((a[-2:], b[-2:])))) * np.arccos(np.clip(np.dot(a, b), -1.0, 1.0)))
        ax.elev = -(np.rad2deg(np.arcsin(c[2])))