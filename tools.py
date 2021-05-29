import itertools
#include <fstream>
#include "string.h"

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


#int n , condition list , int indices
def correctConditions(n,list, indices):
    for i in  range(0,n):
        
        indices[i] = list[i].getNode1()
    for i in  range(0,n-1):
        pivot = list[i].getNode1()
        for j in  range(i,n):
            if(list[j].getNode1()>pivot):
                list[j].setNode1(list[j].getNode1()-1)



def leerMallayCondiciones( m,filename):



    conditionsarray = 0
    nnodes=0
    neltos=0
    ndirich=0
    nneu=0
    k=0
    Q=0
    with open('test2.dat') as f:
        for line in itertools.islice(f, 0,1):  # start=17, stop=None
            conditionsarray =line.split()
            k=float(conditionsarray[0])
            Q=float(conditionsarray[1])

        for line in itertools.islice(f, 0,1):  # start=17, stop=None
            conditionsarray =line.split()
            nnodes=int(conditionsarray[0])
            neltos=int(conditionsarray[1])
            ndirich=int(conditionsarray[2])
            nneu=int(conditionsarray[3])

        
        m.setParameters(k,Q)
        m.setSizes(nnodes,neltos,ndirich,nneu)
        m.createData()
        item_list = m.getNodes()
        i=0
        for line in itertools.islice(f, 2, nnodes+2):  # start=17, stop=None
            array= line.split()
            #print(array)
            item_list[i].setValues(array[0],array[1],array[2],NOTHING,NOTHING,NOTHING,NOTHING);
            i+=1
            # process lines

        i=0
        element_list = m.getElements()
        for line in itertools.islice(f, 3,   neltos+3):  # start=17, stop=None

            array= line.split()

            #print(array)

            element_list[i].setValues(array[0],NOTHING,NOTHING,array[1],array[2],array[3],NOTHING);
            i+=1
            # process lines
            
        direchlet_list = m.getDirichlet()
        i=0
        for line in itertools.islice(f, 3, 3 + ndirich):  # start=17, stop=None

            array= line.split()

            #print(array)
            direchlet_list[i].setValues(NOTHING,NOTHING,NOTHING,array[0],NOTHING,NOTHING,array[1]);
            i+=1
            # process lines


        i=0
        neuman_list = m.getNeumann()
        for line in itertools.islice(f, 3, 3 + nneu):  # start=17, stop=None

            array= line.split()

            #print(array)
            neuman_list[i].setValues(NOTHING,NOTHING,NOTHING,array[0],NOTHING,NOTHING,array[1]);
            i+=1
            # process lines
    f.close()





    print(m.getDirichletIndices())
    correctConditions(ndirich,m.getDirichlet(),m.getDirichletIndices())
    print(m.getDirichletIndices())

