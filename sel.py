#show fuctions at last

import numpy as np
NOTHING = 0
NOLINE = 0
SINGLELINE = 1
DOUBLELINE = 2
#eModes=Enum('NOMODE','INT_FLOAT','INT_FLOAT_FLOAT','INT_INT_INT_INT')
THERMAL_CONDUCTIVITY=0
HEAT_SOURCE=1
NODES=0
ELEMENTS=1
DIRICHLET=2
NEUMANN=3


#int i, mesh m
def calculateLocalD( i, m):
   # float D,a,b,c,d;

    #element e
    e = m.getElement(i);

    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)

    a=n2.getX()-n1.getX()
    b=n2.getY()-n1.getY()
    c=n3.getX()-n1.getX()
    d=n3.getY()-n1.getY()
    D = a*d - b*c

    return D;

def calculateMagnitude( v1,  v2): #dos flotantes calcula la magnitud
    return np.sqrt(v1**2 + v2**2)

#mesh m
def calculateLocalArea( i, m):
    e = m.getElement(i);
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)

    a= calculateMagnitude(n2.getX()-n1.getX(),n2.getY()-n1.getY())
    b= calculateMagnitude(n3.getX()-n2.getX(),n3.getY()-n2.getY())
    c= calculateMagnitude(n3.getX()-n1.getX(),n3.getY()-n1.getY())
    s= (a+b+c)/2

    A= np.sqrt(s*(s-a)*(s-b)*(s-c)) #buscar reemplazo para sqrt
    return A

#Int i, Matrix A, mesh m
def calculateLocalA( i, A, m):
    e = m.getElement(i)
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)
    A[0,0] = n3.getY()-n1.getY() 
    A[0,1] = n1.getY()-n2.getY()
    A[1,0] = n1.getX()-n3.getX()
    A[1,1] = n2.getX()-n1.getX()

#matrix B
def calculateB(B):
    B[0,0] = -1
    B[0,1] = 1
    B[0,2] = 0
    B[1,0] = -1
    B[1,1] = 0
    B[1,2] = 1

#int element, mesh M
def createLocalK( element, m):
    # K = (k*Ae/D^2)Bt*At*A*B := K_3x3 Codigo no usado no tocar
    k = m.getParameter(THERMAL_CONDUCTIVITY)
    #Matrix K,A,B,Bt,At  Declarar A, B, Bt,At abajo

    D = calculateLocalD(element,m)
    Ae = calculateLocalArea(element,m)

    A=np.zeros((2,2))
    B=np.zeros((2,3))
    calculateLocalA(element,A,m) #A local
    calculateB(B) #B local
    #print(A)
    #print(B)
    At=np.matrix.transpose(A) #transponer necesito una funcion para transponer, tambien llena A transpuesta

    Bt=np.matrix.transpose(B) #transponer necesito una funcion para transponer, tambien llena A transpuesta

    #Ojo
    #K=np.matmul(k*Ae/(D*D),np.matmul(Bt,np.matmul(At,np.matmul(A,B))))
    K= np.matmul(Bt,np.matmul(At,np.matmul(A,B)))
    return K

    #int i, mesh m
def calculateLocalJ(i, m):
    e = m.getElement(i)
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)

    a=n2.getX()-n1.getX()
    b=n3.getX()-n1.getX()
    c=n2.getY()-n1.getY()
    d=n3.getY()-n1.getY()
    J = a*d - b*c

    return J

#int element,mesh m
def createLocalb(element, m):
   # b;

    Q = m.getParameter(HEAT_SOURCE)
    J = calculateLocalJ(element,m)
    b_i = Q*J/6
    b=np.empty(3)
    b[0]=b_i
    b[1]=b_i
    b[2]=b_i
    #np.append(b,3)
    #np.append(b,4)
    #np.append(b,55)

    return b

#mesh m, vector of matrix local Ks, vector of vectors local Bs
def crearSistemasLocales( m,localKs,localbs):
    for i in range(0,m.getSize(ELEMENTS)):
        #np.append(localKs,createLocalK(i,m))
        #np.append(localbs,createLocalb(i,m))

        localKs.append(createLocalK(i,m))
        localbs.append(createLocalb(i,m))
        #print(localbs)
        #np.append(localKs,createLocalK(i,m))
        #np.append(localbs,createLocalb(i,m))
def assemblyK( e,localK, K):
    index1 = e.getNode1() - 1
    index2 = e.getNode2() - 1
    index3 = e.getNode3() - 1

    K[index1,index1] += localK[0,0]
    K[index1,index2] += localK[0,1]
    K[index1,index3] += localK[0,2]
    K[index2,index1] += localK[1,0]
    K[index2,index2] += localK[1,1]
    K[index2,index3] += localK[1,2]
    K[index3,index1] += localK[2,0]
    K[index3,index2] += localK[2,1]
    K[index3,index3] += localK[2,2]

#element e, vector localb, reference vector b
def assemblyb( e, localb, b):
    index1 = e.getNode1() - 1
    index2 = e.getNode2() - 1
    index3 = e.getNode3() - 1

    b[index1] += localb[0]
    b[index2] += localb[1]
    b[index3] += localb[2]

#mesh m, vector of matrix localKs, vector of vectors localbs, matrix K, vector b
def ensamblaje( m, localKs, localbs,K, b):
    for i in range(0,m.getSize(ELEMENTS)):
        e = m.getElement(i)
        assemblyK(e,localKs[i],K)
        assemblyb(e,localbs[i],b)

#mesh m, vector b
def applyNeumann( m, b):
    for i in range(0,m.getSize(NEUMANN)):
        #condition c
        c = m.getCondition(i,NEUMANN)
        b[c.getNode1()-1] += c.getValue()

#mesh m , matrix K, vector b
def applyDirichlet( m, K, b):
    for i in range (0,m.getSize(DIRICHLET)):
        #condition c
        c = m.getCondition(i,DIRICHLET)
        index = c.getNode1()-1


        print("index")
        print(index) 
        #Ojo con esto
        np.delete(K,index)
        np.delete(b,index)
        #b.delete(b[0]+index)

        print(K)
        print(type(K))
        
        for row in range(0,K.size):
            cell = K[row,index]
            
            np.delete(K[row],0+index)
            #K[row].erase(K[row,0]+index)
            b[row] += -1*c.getValue()*cell

def calculate( K, b,  T):
    print("Iniciando calculo de respuesta...\n")

    print("Calculo de inversa...\n")
    Kinv = np.linalg.inv(K) 

    print("Calculo de respuesta...\n")
    np.matmul(np.matmul(Kinv,b),T)

