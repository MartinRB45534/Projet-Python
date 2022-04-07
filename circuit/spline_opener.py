import numpy as np

def readfile(filename) :

  f=open(filename,'r')
  nb_points = int(f.readline())
  assert(nb_points>3) #Rendre ça plus propre
  points=np.zeros((nb_points,3),np.double)
  print(nb_points)
  for i in range(nb_points) :
    f.readline() #Devrait être une ligne vide. Rajouter un test.
    for j in range(3):
        points[i,j]=np.double(f.readline())

  f.close() 
  return points