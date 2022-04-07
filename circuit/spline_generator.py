import numpy as np

def D(points):
    Ds=np.zeros(points.shape)
    nb_points = points.shape[0]
    mat = np.diag([4]*nb_points)+np.diag([1]*(nb_points-1),1)+np.diag([1]*(nb_points-1),-1)+np.diag([1],nb_points-1)+np.diag([1],-nb_points+1)
    mat_inv = np.linalg.inv(mat)
    Ds[:,:]=np.linalg.solve(mat,(np.append(points[1:,:],points[:1,:],axis=0)-np.append(points[-1:,:],points[:-1,:],axis=0)))
    return Ds

def cree_spline(points,num=4): #Donner une valeur par défaut à step
    nb_points = points.shape[0]
    Ds=D(points)
    As=np.zeros((nb_points,3,4))
    As[:,:,0]=points
    As[:,:,1]=Ds
    As[:,:,2]=3*(np.append(points[1:,:],points[:1,:],axis=0)-points)-2*Ds-np.append(Ds[1:,:],Ds[:1,:],axis=0)
    As[:,:,3]=2*(points-np.append(points[1:,:],points[:1,:],axis=0))+Ds+np.append(Ds[1:,:],Ds[:1,:],axis=0)

    #On va mesurer approximativement la longueur de la spline
    longueur=0
    t=np.linspace(0,1,num)
    f=np.zeros((t.shape[0],3))
    for k in range(nb_points):
        for i in range(3):
            f[:,i] = As[k,i,0]+As[k,i,1]*t+As[k,i,2]*np.power(t,2)+As[k,i,3]*np.power(t,3) #À corriger probablement
        longueur+=sum(np.sqrt(np.power((f[:-1,:]-f[1:,:])[:,0],2)+np.power((f[:-1,:]-f[1:,:])[:,1],2)+np.power((f[:-1,:]-f[1:,:])[:,2],2))) #Douteux ici aussi
    step=longueur/100 # 1000 peut-être ?
    dt=0.001
    step_part=0
    spline=points[:1,:]
    t=0
    k=0
    point = points[0,:]
    while k < nb_points:
        t+=dt
        nouveau_point = As[k,:,0]+As[k,:,1]*t+As[k,:,2]*np.power(t,2)+As[k,:,3]*np.power(t,3)
        distance = np.sqrt(np.power((nouveau_point-point)[0],2)+np.power((nouveau_point-point)[1],2)+np.power((nouveau_point-point)[2],2))
        point=nouveau_point
        step_part+=distance
        if step_part>step:
            spline = np.append(spline,point.reshape(1,3),axis=0)
            step_part-=step
        if t>=1:
            t=0
            k+=1
    return spline

