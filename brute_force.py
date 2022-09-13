from itertools import product
from xmlrpc.client import MAXINT

soc0 = 100                  #Initial state of charge (%)
socL = 30                   #Final state of charge (%)
L = 500                     #Total length of the trip (km)
r = 40                      #Charging rate (%/h)
c = 0.25                    #Energy consumption of the car (%/km)
x = [0, 150, 450, L]        #List containing each power station's position (km)
N = len(x)-2
v = 100                     #Constant speed of the vehicle (km/h)
tau = [0, 0.75, 0.33, 0]    #List containing each power station's waiting time (h)


def temps(I):
    T = 0
    soc = soc0
    for k in range(1, N+1):
        T += (x[k] - x[k-1])/v
        if I[k] == 1:
            soc_obj = min(100, socL + (L-x[k])*c)
            T += (soc_obj - soc)/r + tau[k]
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
    temp = product([0,1], repeat = N)
    print(list(temp))
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


print(optimize(x, tau))
