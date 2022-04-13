import numpy as np

def readfile(filename) :
  """Opens a rollercoaster file."""
  f=open(filename,'r')
  nb_points = int(f.readline())
  try:
    assert(nb_points>3)
  except:
    raise Not_enough_points(nb_points)
  points=np.zeros((nb_points,3),np.double)
  try:
    for i in range(nb_points) :
      f.readline() #Devrait être une ligne vide. Rajouter un test.
      for j in range(3):
          points[i,j]=np.double(f.readline())
  except:
    raise Not_enough_lines()

  f.close() 
  return points

class File_opening_error(Exception):
  pass

class Not_enough_points(File_opening_error):
  def __init__(self, nb_points):
    self.nb_points = nb_points
    self.message = f"Il faut au moins 3 points pour dessiner une spline, le fichier n'en a que {nb_points} !"
    super().__init__(self.message)

class Not_enough_lines(File_opening_error):
  def __init__(self):
    super().__init__("File is too short !")