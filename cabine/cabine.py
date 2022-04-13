import numpy as np

class Cabine:
    """Représente la cabine. Sert juste à stocker la position et la vitesse."""
    def __init__(self):
        self.position = 0 #La position (entre les points d'indices intervalle et intervalle+1)
        self.intervalle = 0 #L'intervalle sur lequel la cabine se trouve
        self.vitesse = 0 #La vitesse (augmentation de la position par intervalle de temps)
