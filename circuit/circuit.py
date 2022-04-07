from matplotlib.pyplot import pause
from cabine.cabine import Cabine
import numpy as np
from variables.constantes import *

class Circuit:
    def __init__(self,spline):
        self.spline = spline
        self.cabine = Cabine()

    def deplace(self):
        self.update_vitesse()
        # On fait avancer la cabine
        point_1 = self.spline[self.cabine.intervalle,:]
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
        longueur = np.sqrt(sum(np.power((point_1-point_2),2))) #La longueur du segment intervalle, itervalle+1
        distance = self.cabine.vitesse*dt #La distance que parcourt la cabine sur un intervalle de temps
        while distance > longueur:
            distance -= longueur
            self.cabine.intervalle+=1
            if self.cabine.intervalle >= self.spline.shape[0]:
                self.cabine.intervalle = 0
            point_1 = point_2
            point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
            longueur = np.sqrt(sum(np.power((point_1-point_2),2)))
        while distance < 0:
            distance += longueur
            if self.cabine.intervalle <= 0:
                self.cabine.intervalle = self.spline.shape[0]
            self.cabine.intervalle-=1
            point_2 = point_1
            point_1 = self.spline[self.cabine.intervalle,:]
            longueur = np.sqrt(sum(np.power((point_1-point_2),2)))
        proportion=distance/longueur #Cette distance, exprimée en proportion de la longueur du segment
        self.cabine.position = proportion

    def update_vitesse(self):
        #On commence par calculer l'accélération
        point_1 = self.spline[self.cabine.intervalle,:]
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
        longueur = np.sqrt(sum(np.power((point_1-point_2),2)))
        u=(point_2-point_1)/longueur
        a=G*np.dot(np.array([0,0,-1]),u)-k*self.cabine.vitesse/m
        self.cabine.vitesse += a*dt

    def get_dir_cabine(self):
        point_1 = self.spline[self.cabine.intervalle,:]
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
        return point_1-point_2

    def get_pos_cabine(self):
        point_1 = self.spline[self.cabine.intervalle,:]
        point_2 = np.append(self.spline[1:,:],self.spline[:1,:],axis=0)[self.cabine.intervalle,:]
        return point_1*(1-self.cabine.position)+point_2*self.cabine.position

