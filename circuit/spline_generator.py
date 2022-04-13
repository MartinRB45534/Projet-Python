import numpy as np

def D(points):
    """
    Calcule la matrice D

    >>> points=np.array([[1,2,3],[2,3,4],[3,4,5]])
    >>> D(points)
    array([[-1., -1., -1.],
           [ 2.,  2.,  2.],
           [-1., -1., -1.]])
    """
    Ds=np.zeros(points.shape)
    nb_points = points.shape[0]
    mat = np.diag([4]*nb_points)+np.diag([1]*(nb_points-1),1)+np.diag([1]*(nb_points-1),-1)+np.diag([1],nb_points-1)+np.diag([1],-nb_points+1)
    Ds[:,:]=np.linalg.solve(mat,3*(np.append(points[1:,:],points[:1,:],axis=0)-np.append(points[-1:,:],points[:-1,:],axis=0)))
    return Ds

def cree_spline(points,num=4):
    """Crée la spline à partir de ses points de contrôle"""


    #On commence par obtenir les polynômes qui définissent la spline sur chaque segment
    nb_points = points.shape[0]
    Ds=D(points)
    As=np.zeros((nb_points,3,4))
    As[:,:,0]=points
    As[:,:,1]=Ds
    As[:,:,2]=3*(np.append(points[1:,:],points[:1,:],axis=0)-points)-2*Ds-np.append(Ds[1:,:],Ds[:1,:],axis=0)
    As[:,:,3]=2*(points-np.append(points[1:,:],points[:1,:],axis=0))+Ds+np.append(Ds[1:,:],Ds[:1,:],axis=0)



    #On va mesurer approximativement la longueur de la spline
    longueur=0
    t=np.linspace(0,1,num) #On peut modifier num dans l'appel pour augmenter ou diminuer la précision de cette mesure
    f=np.zeros((t.shape[0],3))
    for k in range(nb_points):
        for i in range(3):
            f[:,i] = As[k,i,0]+As[k,i,1]*t+As[k,i,2]*np.power(t,2)+As[k,i,3]*np.power(t,3)
        longueur+=sum(np.sqrt(np.power((f[:-1,:]-f[1:,:])[:,0],2)+np.power((f[:-1,:]-f[1:,:])[:,1],2)+np.power((f[:-1,:]-f[1:,:])[:,2],2)))


    # On subdivise la longueur en intervalles plus petits
    step=longueur/500 # 1000 peut-être ?
    dt=0.001
    step_part=0
    t=0
    k=0

    #On va reparcourir la spline pour trouver des points à peu près équidistants
    spline=points[:1,:]
    point = points[0,:]
    while k < nb_points:
        t+=dt #On parcourt chaque polynôme entre deux points de contrôle par petits pas de temps
        nouveau_point = As[k,:,0]+As[k,:,1]*t+As[k,:,2]*np.power(t,2)+As[k,:,3]*np.power(t,3) #Le point au temps t est obtenu à partir des coefficients du polynôme
        distance = np.sqrt(np.power((nouveau_point-point)[0],2)+np.power((nouveau_point-point)[1],2)+np.power((nouveau_point-point)[2],2))
        point=nouveau_point
        step_part+=distance #On incrémente la distance parcourue depuis le dernier point accepté
        if step_part>=step: #Si on a dépassé la distance voulue entre deux points de l'approximation,
            spline = np.append(spline,point.reshape(1,3),axis=0) #on rajoute le point actuel à l'approximation et on recommence à compter notre distance
            step_part-=step #step_part = 0 réduirait légèrement la variance des écarts entre deux points consécutifs, mais augmenterait le décalage cumulé lors du parcours
        if t>=1: #On passe au point de contrôle suivant
            t=0
            k+=1
    return spline

import doctest
doctest.testmod()