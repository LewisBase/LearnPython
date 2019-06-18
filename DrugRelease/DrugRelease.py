# This program is designed to analyze the drgu release data
# A series of release function are considered to fit the release data
# Author: lewisbase
# Date: 2019.06.08
# 

import numpy as np 
import pandas as pd 
from scipy.optimize import leastsq
import matplotlib.pyplot as plt 

def Zero_Dynamic_sq(p):
    q,k = p
    return y-q-k*x
def Zero_Dynamic_fit(Q,K):
    return Q+K*x

def One_Dynamic_sq(p):
    qw = np.max(y)
    m,k = p
    return y-qw*(1-m/qw*np.exp(-k*x))
def One_Dynamic_fit(M,K):
    Qw = np.max(y)
    return Qw*(1-M/Qw*np.exp(-K*x))

def Higuchi_sq(p):
    k = p
    return y-k*x**0.5
def Higuchi_fit(K):
    return K*x**0.5

def Hixson_Crowell_sq(p):
    k = p
    return 0**(1/3)-y**(1/3)-k*x
def Hixson_Crowell_fit(K):
    return (0**(1/3)-K*x)**3

def Korsmeyer_sq(p):
    n = p
    return np.log(y)-n*np.log(x)
def Korsmeyer_fit(N):
    return np.exp(N)*x

def Korsmeyer_Peppas_sq(p):
    k,n = p
    return y-k*x**n
def Korsmeyer_Peppas_fit(K,N):
    return K*x**N

def Weibull_sq(p):
    k = p
    return np.log(np.log(1/(1-y)))-k*np.log(x)
def Weibull_fit(K):
    return 1-(np.exp(np.exp(K)*x))**-1

def Two_phase_Dynamic_sq(p):
    a,A,b,B = p
    return y-A*np.exp(a*x)-B*np.exp(b*x)
def Two_phase_Dynamic_fit(a,A,b,B):
    return A*np.exp(a*x)-B*np.exp(b*x)


dfFunction = pd.DataFrame([[Zero_Dynamic_sq,One_Dynamic_sq, \
    Higuchi_sq,Hixson_Crowell_sq,Korsmeyer_sq,Korsmeyer_Peppas_sq, \
    Weibull_sq,Two_phase_Dynamic_sq], \
    [Zero_Dynamic_fit,One_Dynamic_fit,Higuchi_fit, \
    Hixson_Crowell_fit,Korsmeyer_fit,Korsmeyer_Peppas_fit, \
    Weibull_fit,Two_phase_Dynamic_fit]],columns=['Zero_Dynamic', \
    'One_Dynamic','Higuchi','Hixson_Crowell','Korsmeyer', \
    'Korsmeyer_Peppas','Weibull','Two_phase_Dynamic'],index=['sq','fit'])

def FitFunction(function):
    if function == 'Two_phase_Dynamic':
        result = leastsq(dfFunction.loc['sq',function],[1,1,1,1])
        a,A,b,B = result[0]
        yfit = dfFunction.loc['fit',function](a,A,b,B) 
        return yfit
    elif function in ['Higuchi','Hixson_Crowell','Weibull']:
        result = leastsq(dfFunction.loc['sq',function],[1])
        K = result[0]
        yfit = dfFunction.loc['fit',function](K)
        return yfit
    elif function == 'Zero_Dynamic':
        result = leastsq(dfFunction.loc['sq',function],[1,1])
        Q,K = result[0]
        yfit = dfFunction.loc['fit',function](Q,K)
        return yfit
    elif function == 'One_Dynamic':
        result = leastsq(dfFunction.loc['sq',function],[1,1])
        M,K = result[0]
        yfit = dfFunction.loc['fit',function](M,K)
        return yfit
    elif function == 'Korsmeyer':
        result = leastsq(dfFunction.loc['sq',function],[1])
        N = result[0]
        yfit = dfFunction.loc['fit',function](N)
        return yfit
    elif function == 'Korsmeyer_Peppas':
        result = leastsq(dfFunction.loc['sq',function],[1,1])
        K,N = result[0]
        yfit = dfFunction.loc['fit',function](K,N)
        return yfit
    else:
        raise Exception('No useful function found!')
        
x,y = np.loadtxt('Drug.txt',delimiter='\t',usecols=(0,5),unpack=True)
dfYvalue = pd.DataFrame(y,columns=['experiment'])
plt.figure(figsize=(12,12),dpi=100)
plt.scatter(x,y)
for function in dfFunction.columns:
    Yfit = FitFunction(function)
    dfYvalue[function] = Yfit
    plt.plot(x,Yfit,label=function)
plt.legend(loc='best',ncol=2)
plt.show()
dfYvalue.corr()