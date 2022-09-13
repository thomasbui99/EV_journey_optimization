from itertools import combinations_with_replacement
from xmlrpc.client import MAXINT

soc0 = 50       #Initial state of charge (%)
socL = 30       #Final state of charge (%)
L = 500         #Total length of the trip (km)
r = 1           #Charging rate (%/min)
c = 1           #Energy consumption of the car (%/km)
x = [150,450]   #List containing each power station's position
N = len(x)
v = 130         #Constant speed of the vehicle
tau = [45, 20]  #List containing each power station's waiting time


def temps(I):
    T = 0
    soc = soc0
    for k in range(1, N+1):
        T += (x[k] - x[k-1])/v
        if I[k] == 1:
            soc_obj = min(100, socL + (L-x[k])*c)
            T += (soc_obj - soc)/r
            soc = soc_obj
    return T

def acceptable(I):
    soc = soc0
    for k in range(1, N+1):
        soc -= (x[k] - x[k-1])*c
        if soc < 0:
            return False
        if I[k] == 1:
            soc = min(100, socL + (L-x[k])*c)
    soc -= (L - x[N])*c
    return soc - socL > 0

def generate():
    temp = combinations_with_replacement([0,1],N)
    return list(temp)

def optimize(x, tau):
    listI = generate()
    (minT, minI) = (MAXINT, None)
    for I in listI:
        if acceptable(I):
            newT = temps(I)
            if newT < minT:
                (minT, minI) = (newT, I)
    return (minT, minI)
