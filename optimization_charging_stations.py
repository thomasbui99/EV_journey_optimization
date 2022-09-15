from cmath import inf
from itertools import product
from xmlrpc.client import MAXINT
import random


# Part1: Data of the problem

soc0 = 100                          # Initial state of charge (%)
socL = 30                           # Final state of charge (%)
L = 750                             # Total length of the trip (km)
r = 40                              # Charging rate (%/h)
c = 0.25                            # Energy consumption of the car (%/km)
v = 100                             # Constant speed of the vehicle (km/h)
# List containing each power station's position (km)
x = [0, 150, 200, 330, 450, 520, 600, 620, 730, L]
# List containing each power station's waiting time (h)
tau = [0, 0.5, 0.9, 0.33, 0.2, 0.4, 1, 0.6, 0.45, 0]
# By construction, the starting point and the ending point are included in x and tau with waiting time = 0
N = len(x)-2

# The solution of the problem is given with the following format:
# a list such that I[k] = 1 if the car stops at the station k, I[k] = 0 otherwise


# Part 2: Brute force resolution for constant waiting times


# Compute the time of the journey for a given candidate (objective function)
def time(I):
    T = 0
    soc = soc0 - (x[1] - x[0])*c
    for k in range(1, N+1):
        T += (x[k] - x[k-1])/v
        if I[k-1] == 1:
            soc_obj = max(soc, min(100, socL + (L-x[k])*c))
            T += (soc_obj - soc)/r + tau[k]  # Attention
            soc = soc_obj
    T += (x[N+1]-x[N])/v
    return T

# Check the satisfiability of a candidate
def acceptable(I):
    soc = soc0
    for k in range(1, N+1):
        soc -= (x[k] - x[k-1])*c
        if soc < 0:
            return False
        if I[k-1] == 1:
            soc = max(soc, min(100, socL + (L-x[k])*c))
    soc -= (L - x[N])*c
    return soc - socL >= 0

# Generate all the possible combinations
def generate():
    temp = product([0, 1], repeat=N)
    return list(temp)

# Find the optimal solution by brute force
def optimize(x, tau):
    listI = generate()
    (minT, minI) = (inf, None)
    for I in listI:
        if acceptable(I):
            newT = time(I)
            if newT < minT:
                (minT, minI) = (newT, I)
    #print("Stations where to stop: {} \nTotal time: {} h".format(convert(minI), minT))
    return (minI, minT)

# Convert format I to a list of stations where to stop
def convert(I):
    l = []
    for i in range(len(I)):
        if I[i] == 1:
            l.append(i+1)
    return l


# Part 3: Simulated annealing

# Compute the penalty of a candidate-solution (if some constraints are not satisfied)
def penalty(I):
    soc = soc0
    pen = 0
    for k in range(1, N+1):
        soc -= (x[k]-x[k-1])*c
        if soc < 0:
            pen -= soc
        if I[k-1] == 1:
            soc = max(soc, min(100, socL + (L-x[k])*c))
    soc -= (L-x[N])*c
    pen += socL-soc
    return pen

# Create an initial choice of stations:
# We stop when we are going to be out of battery and cannot reach the next station
def initial():
    I = []
    soc = soc0
    for k in range(1, N):
        soc -= (x[k]-x[k-1])*c
        if soc-(x[k+1]-x[k])*c > 0:
            I.append(0)
        else:
            I.append(1)
            soc = max(soc, min(100, socL + (L-x[k])*c))
    soc -= (x[N]-x[N-1])*c
    if soc - (L-x[N])*c >= socL:
        I.append(0)
    else:
        I.append(1)
    return I

# Modify the choice of stations randomly
def modif(I, p):
    val = random.random()
    if val <= p:
        k = random.randint(0, N-1)
        I[k] = 1-I[k]
    return I

# Algorithm of the simulated annealing
def annealing(x, tau):
    I = initial()
    minI = list(I)
    min_score = time(I)+100*penalty(I)
    p = 1
    while p > 1e-3:
        I = modif(I, p)
        score = time(I)+100*penalty(I)
        if score < min_score:
            minI = list(I)
            min_score = score
        p *= 0.99
    return (minI, time(minI), acceptable(minI))


# Tests

print("Optimal")
print(optimize(x, tau))
print("Simulated annealing")
print(annealing(x, tau))
