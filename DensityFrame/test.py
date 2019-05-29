import numpy as np 
import matplotlib.pyplot as plt 

def Potential(rho,sig,eps,R,x):
    return 16*np.pi/3*rho*R**3*eps* \
        (((5*R**6+45*R**4*x**2+63*R**2*x**4+15*x**6)*sig**12)/(15*(x**2-R**2)**9)-sig**6/(3*(x**2-R**2)**3))

def Potential_test(sig,x,R):
    return ((5*R**6+45*R**4*x**2+63*R**2*x**4+15*x**6)*sig**12)/(15*(x**2-R**2)**9)-sig**6/(3*(x**2-R**2)**3) 
#R = 5.0
#x = np.linspace(5.2,5.5,100)
sig = np.linspace(1,5,100)
#rho = 90/(4/3*np.pi*5**3)

plt.plot(sig,Potential_test(sig,14.2,10))
plt.show()
