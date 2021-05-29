from sel import *
from tools import *
from classes import *
import numpy as np

NOTHING = 0
NOLINE = 0
SINGLELINE = 1
DOUBLELINE = 2
THERMAL_CONDUCTIVITY=0
HEAT_SOURCE=1
NODES=0
ELEMENTS=1
DIRICHLET=2
NEUMANN=3


def main():

    m = mesh();
    filename="test2.dat"
    leerMallayCondiciones(m,filename)

    localKs = []
    localbs = []
    crearSistemasLocales(m,localKs,localbs);
    

    K = np.zeros((m.getSize(NODES),m.getSize(NODES)))
    b = np.zeros(m.getSize(NODES))

    ensamblaje(m,localKs,localbs,K,b)
    print(localbs)

    applyNeumann(m,b);

    applyDirichlet(m,K,b);

    calculate(K,b,T);


    #writeResults(m,T,filename);

    return 0

main()
