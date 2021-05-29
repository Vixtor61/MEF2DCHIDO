from enum import Enum
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

class item:

       

    def setId(self , identifier):
        self.id = identifier

    def setX(self,x_coord):
        self.x = x_coord

    def setY(self, y_coord):
        self.y = y_coord

    def setNode1(self, node_1):
        self.node1 = node_1

    def setNode2(self,node_2):
        self.node2 = node_2;

    def setNode3(self,node_3):
        self.node3 = node_3;

    def setValue(self, value_to_assign):
        self.value = value_to_assign;

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNode1(self):
        return self.node1

    def getNode2(self):
        return self.node2

    def getNode3(self):
        return self.node3

    def getValue(self):
        return self.value

        def setValues(a,b,c,d,e,f,g):
            a=0
            b=0
            c=0
            d=0
            e=0
            f=0
            g=0


class node(item):

    def setValues(self,a,b,c,d,e,f,g):
        self.id = int(a)
        self.x = float(b)
        self.y = float(c)
        

class element(item):
    def setValues(self,a,b,c,d,e,f,g):
        self.id = int(a)
        self.node1 = int(d)
        self.node2 = int(e)
        self.node3 = int(f)


class condition(item):
    def setValues(self,a,b,c,d,e,f,g):
        self.node1 = int(d)
        self.value = float(g)


class mesh:
        

    def __init__(self):

        self.parameters = np.empty(2)
        self.sizes = [0] * 4
    def setParameters(self, k, Q):

        self.parameters[THERMAL_CONDUCTIVITY]=k
        self.parameters[HEAT_SOURCE]=Q

        #ints
    def setSizes(self, nnodes, neltos, ndirich, nneu):
        self.sizes[NODES] = nnodes
        self.sizes[ELEMENTS] = neltos
        self.sizes[DIRICHLET] = ndirich
        self.sizes[NEUMANN] = nneu

    def getSize(self,s):
        return self.sizes[s]

    def getParameter(self,p):
        return self.parameters[p]

    def createData(self):
        self.node_list = []
        for i in range(0,self.sizes[NODES] ):
            self.node_list.append(node())

        self.element_list = []
        for i in range(0,self.sizes[ELEMENTS] ):
            self.element_list.append(element())

        self.indices_dirich = [0] * self.sizes[DIRICHLET]


        self.dirichlet_list = [condition()] * self.sizes[DIRICHLET]

        for i in range(0,self.sizes[DIRICHLET] ):
            self.dirichlet_list.append(condition())

        self.neumann_list = []

        for i in range(0,self.sizes[NEUMANN] ):
            self.neumann_list.append(condition())

    def getNodes(self):
        return self.node_list

    def getElements(self):
        return self.element_list

    def getDirichletIndices(self):
        return self.indices_dirich
    
    def getDirichlet(self):
        return self.dirichlet_list

    def getNeumann(self):
        return self.neumann_list;

    def getNode(self, i):
        return self.node_list[i]

    def getElement(self, i):
        return self.element_list[i]

    def getCondition( self,i,  dtype):
        if(dtype == DIRICHLET):
            return self.dirichlet_list[i]
        else:
            return self.neumann_list[i]
