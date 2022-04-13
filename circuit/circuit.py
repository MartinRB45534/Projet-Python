from matplotlib.pyplot import pause
from cabine.cabine import Cabine
import numpy as np
from variables.constantes import *

class Circuit:
    """
    L'objet qui représente le circuit.
    Comprend la spline et la cabine
    """
    def __init__(self,spline):
        self.spline = spline
        self.cabine = Cabine()

    def deplace(self):
        """Modifie la position et la vitesse de la cabine"""

        # On pourrait aussi modifier la vitesse après, ça ne change pas grand-chose
        self.update_vitesse()

        # On fait avancer la cabine
        point_1 = self.spline[self.cabine.intervalle,:] #Le point de la spline "avant" la cabine ("avant" au sens de sa position dans la liste de la spline)
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:] #Et celui "après"
        longueur = np.sqrt(sum(np.power((point_1-point_2),2))) #La longueur du segment intervalle, itervalle+1
        deja_parcourue = self.cabine.position*longueur #cabine.position est la proportion du segment actuel qui a déjà été parcourue
        distance_ajoutee = self.cabine.vitesse*dt #La distance que parcourt la cabine sur un intervalle de temps
        distance = deja_parcourue+distance_ajoutee #La distance à parcourir, à partir du début du segment

        #Si la distance est positive et supérieure à la longueur du segment, il faut passer sur le segment suivant
        while distance > longueur:

            distance -= longueur #Il reste probablement encore de la distance à parcourir

            self.cabine.intervalle+=1 #On passe sur l'intervalle suivant
            if self.cabine.intervalle >= self.spline.shape[0]:
                self.cabine.intervalle = 0

            point_1 = point_2 #On réobtient les points
            point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
            longueur = np.sqrt(sum(np.power((point_1-point_2),2)))

        #Si la longueur est négative, il faut passer sur le segment précédent
        while distance < 0:

            distance += longueur

            if self.cabine.intervalle <= 0:
                self.cabine.intervalle = self.spline.shape[0]
            self.cabine.intervalle-=1 #On passe sur l'intervalle précédent

            point_2 = point_1 #On réobtient les points
            point_1 = self.spline[self.cabine.intervalle,:]
            longueur = np.sqrt(sum(np.power((point_1-point_2),2)))

        #La distance qui reste tombe dans l'intervalle courant
        proportion=distance/longueur #La position stocke la proportion de l'intervalle courant qu'on a déjà parcourue
        self.cabine.position = proportion

    def update_vitesse(self):
        #On commence par calculer l'accélération

        point_1 = self.spline[self.cabine.intervalle,:] #Le point de la spline "avant" la cabine ("avant" au sens de sa position dans la liste de la spline)
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:] #Et celui "après"
        longueur = np.sqrt(sum(np.power((point_1-point_2),2)))
        u=(point_2-point_1)/longueur #u est le vecteur unitaire le long du segment
        a=G*np.dot(np.array([0,0,-1]),u)-k*self.cabine.vitesse/m #La formule (légèrement simplifiée) de l'accélération (ici l'accélération est un scalaire)
        self.cabine.vitesse += a*dt #La vitesse est un scalaire aussi 

    def get_dir_cabine(self):
        """
        >>> circuit = Circuit(np.array([[0,0,0],[0,0,1],[0,1,1]]))
        >>> circuit.get_dir_cabine()
        array([0., 0., -1.])
        """
        point_1 = self.spline[self.cabine.intervalle,:]
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
        return point_1-point_2

    def get_pos_cabine(self):
        """
        >>> circuit = Circuit(np.array([[0,0,0],[0,0,1],[0,1,1]]))
        >>> circuit.cabine.intervalle = 1
        >>> circuit.cabine.position = 0.3
        >>> circuit.get_pos_cabine()
        array([0., 0.3, 1.])
        """
        point_1 = self.spline[self.cabine.intervalle,:]
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
        return point_1*(1-self.cabine.position)+point_2*self.cabine.position