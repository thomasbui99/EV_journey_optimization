import scipy.optimize as opt
import numpy as np 

### variables
c = 20/100 # EV consumption (%/km), 20% per 100km
L = 650 # distance on highway (km)
r = 100/20 # charging rate (%/min), 100% in 20 min
v = 2 # EV speed, km/min (120 km/h)

X = np.array([50, 250, 350, 400, 550]) # charging points location on highway (km)
T = np.array([100, 0, 100, 100, 0]) # waiting time at CP (min)

soc_0 = 75 # initial state of charge
soc_L = 70 # final state of charge

### notations
a = soc_0 - c*L - soc_L
b = np.array([soc_0 - c*x for x in X])

### objective function
def time_taken(alpha):
    # alpha length : 2*len(X)
    theta = alpha[len(X):] # charging time at CP
    delta = alpha[:len(X)] # decide if stop
    res = np.sum((T+theta)*delta)

    grad = np.concatenate([T+theta, delta], axis=None)
    return res, grad

### constraints
f_binary = lambda alpha: alpha[:len(X)]*(1 - alpha[:len(X)])
binary_cons = opt.NonlinearConstraint(f_binary, 0, 0)

f_soc_L = lambda alpha: a + r * np.sum(alpha[len(X):] * alpha[:len(X)])
soc_L_cons = opt.NonlinearConstraint(f_soc_L, 0, 0)

def f_soc_xk(alpha):
    res = np.zeros(len(X))
    for k in range(1,len(X)):
        res[k] = b[k] + r * np.sum(alpha[len(X):len(X)+k] * alpha[:k])
    return res
soc_xk_cons = opt.NonlinearConstraint(f_soc_xk, 0, 100)

### function that describes the journey in function of the decisions taken
def describe_journey(alpha):
    print('solution:', alpha)

    print('')
    print('----------  JOURNEY DESCRIPTION  -----------')
    print('enter highway with {}%'.format(soc_0))
    soc_i = soc_0 - c*X[0]
    theta_i = alpha[len(X)]
    print('CP 1, {}km made, {}% consumed (soc before CP = {}%), charge={}, {}min charge to reach {}%'.format(
        X[0], c*X[0], soc_i, alpha[0], theta_i, soc_i+theta_i*r))

    for i in range(1,len(X)):
        d = X[i]-X[i-1]
        soc_i = soc_i - c*d + r*(alpha[i-1]*alpha[len(X)+i-1])
        theta_i = alpha[len(X)+i]
        if i==len(X)-1:
            consumption_km_left = c*(L-X[-1])
            theta_i = (soc_L + consumption_km_left - soc_i)/r

        print('CP {}, {}km made, {}% consumed (soc before CP = {}%), charge={}, {}min charge to reach {}%'.format(
            i+1, d, c*d, soc_i, alpha[i], theta_i, theta_i*r+soc_i))

    print('{}km to exit, {}% consumed'.format(
        L-X[-1], c*(L-X[-1])))
    soc_last_cp = theta_i*r+soc_i
    consumption = c*(L-X[-1])
    print('exit highway with {}% (aim was soc_L = {}%)'.format(soc_last_cp - consumption, soc_L))
    print('')
    print('time taken in minutes:', time_taken(alpha)[0])
    print('-------------------------------------------')
    print('')

### example with stops at every CP
delta_0 = np.ones(len(X))
theta_00 = [(100 - (soc_0 - c*X[0]))/r]
theta_1N = [c*(X[i]-X[i-1])/r for i in range(1, len(X)-1)]
theta_0L = [(soc_L + c*(L - X[-1]) - 100 + c*(X[-1] - X[-2]))/r]
alpha_0 = np.concatenate([delta_0, theta_00, theta_1N, theta_0L], axis=None)

print('\n__________________________________')
print('basic journey')
describe_journey(alpha_0)


### optimization
print('-----------JOURNEY OPTIMIZATION------------')

#alpha_0 = [0, 1, 0, 0, 1, 0, 15, 0, 0, 10]
#describe_journey(alpha_0)
print('initialization x:', alpha_0)
res = opt.minimize(
    time_taken, 
    alpha_0, 
    method='SLSQP', 
    jac=True, 
    constraints=[binary_cons, soc_L_cons, soc_xk_cons], 
    bounds=((0,1),(0,1),(0,1),(0,1),(0,1), (0,20),(0,20),(0,20),(0,20),(0,20)))
print(res)

print('\n__________________________________')
print('optimal journey')
describe_journey(res.x)