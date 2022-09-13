import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint

soc0 = 50       #Initial state of charge (%)
socL = 30       #Final state of charge (%)
L = 500         #Total length of the trip (km)
r = 1           #Charging rate (%/min)
c = 1           #Energy consumption of the car (%/km)
x = [150,450]   #List containing each power station's position
tau = [45, 20]  #List containing each power station's waiting time

a = soc0 - socL - c*L
b = [soc0 - c*x[k] for k in range(len(x))]

def traveltime(alpha):
    s = 0
    N = len(alpha)//2
    for i in range(N):
        s += alpha[i] * (tau[i] + alpha[i+N])
    return s

def const1(alpha):
    return [alpha[k] - alpha[k]**2 for k in range(len(alpha))]

def const2(alpha):
    N = len(alpha)//2
    return a + r*sum([alpha[i]*alpha[i+N] for i in range(N)])

def const3(alpha):
    N = len(alpha)//2
    s = 0
    res = []
    for k in range(N):
        s += alpha[k]*alpha[k+N]
        res += b[k] + r*s
    return res




