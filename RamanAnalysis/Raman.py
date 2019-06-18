# This program is designed to analysis the Raman data
# Author: lewisbase
# Date: 2019.06.17


import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import leastsq
from scipy import interpolate
from sys import argv,exit


def CalculateR_2(y1,y2):
    '''calculate the R^2 of regession'''
    Sy1 = np.sum((y1-np.mean(y1))**2)
    Sy2 = np.sum((y2-np.mean(y2))**2)
    Sy1y2 = np.sum((y1-np.mean(y1))*(y2-np.mean(y2)))
    return (Sy1y2/np.sqrt(Sy1*Sy2))**2

if len(argv) < 2:
    print('No Action specified.')
    exit()
elif len(argv) == 2:
    if argv[1].startswith('--'):
        option = argv[1][2:]
        if option == 'version':
            print('''
            RamanSplit version 1.1.0
            Author: lewisbase
            Date: 2019.06.18''')
            exit()
        elif option == 'help':
            print('''
            This script is used to calculate the abundance
            of each component from the split Raman spectrum
            data.
            Options include:
            --version: Prints the version information
            --help:    Prints the help information
            Usage:
            python Raman.py Totaldata.txt Splitdata1.txt Splitdata2.txt
            There should have 2 or 3 splitdatas.''')
            exit()
        else:
            print('Unknow option!')
            exit()
    else:
        print('a --option or some filenames are needed!')
elif len(argv) == 4:
    def RamanCombine(p):
        a,aa,b0,b1,b2,b3,b4,b5 = p
        return y-(a)*x1-(aa)*x2-b0-b1*xw-b2*xw**2-b3*xw**3-b4*xw**4-b5*xw**5

    def RamanFit(A,AA,B0,B1,B2,B3,B4,B5):
        return (A)*x1+(AA)*x2+B0+B1*xw+B2*xw**2+B3*xw**3+B4*xw**4+B5*xw**5
    script,fileS,fileA,fileB = argv
elif len(argv) == 5:
    def RamanCombine(p):
        a,aa,aaa,b0,b1,b2,b3,b4,b5 = p
        return y-(a)*x1-(aa)*x2-(aaa)*x3-b0-b1*xw-b2*xw**2-b3*xw**3-b4*xw**4-b5*xw**5

    def RamanFit(A,AA,AAA,B0,B1,B2,B3,B4,B5):
        return (A)*x1+(AA)*x2+(AAA)*x3+B0+B1*xw+B2*xw**2+B3*xw**3+B4*xw**4+B5*xw**5
    script,fileS,fileA,fileB,fileC = argv
else:
    print('Too many parameters!')
    exit()

xs,ys = np.loadtxt(fileS,dtype=float,usecols=(0,1),unpack=True)
xa,ya = np.loadtxt(fileA,dtype=float,usecols=(0,1),unpack=True)
xb,yb = np.loadtxt(fileB,dtype=float,usecols=(0,1),unpack=True)

ys = (ys-ys.min())/(ys.max()-ys.min())
ya = (ya-ya.min())/(ya.max()-ya.min())
yb = (yb-yb.min())/(yb.max()-yb.min())

xs_new = np.linspace(xs.min(),xs.max(),1000)
xa_new = np.linspace(xa.min(),xa.max(),1000)
xb_new = np.linspace(xb.min(),xb.max(),1000)

fs = interpolate.interp1d(xs,ys)
fa = interpolate.interp1d(xa,ya)
fb = interpolate.interp1d(xb,yb)

if 'fileC' in dir():
    xc,yc = np.loadtxt(fileC,dtype=float,usecols=(0,1),unpack=True)
    yc = (yc-yc.min())/(yc.max()-yc.min())
    xc_new = np.linspace(xc.min(),xc.max(),1000)
    fc = interpolate.interp1d(xc,yc)
    x3 = fc(xc_new)
    
x1 = fa(xa_new)
x2 = fb(xb_new)
xw = xs_new
y = fs(xs_new)

plt.figure(figsize=(12,12),dpi=100)
ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3)
plt.sca(ax1)
plt.plot(xs,ys,'r-',xs_new,fs(xs_new),'b--')
plt.legend(['dataS','dataS-interpolate'],loc='best',frameon=False,fontsize=15)
plt.sca(ax2)
plt.plot(xa,ya,'r-',xa_new,fa(xa_new),'b--')
plt.legend(['dataA','dataA-interpolate'],loc='best',frameon=False,fontsize=15)
plt.sca(ax3)
plt.plot(xb,yb,'r-',xb_new,fb(xb_new),'b--')
plt.legend(['dataB','dataB-interpolate'],loc='best',frameon=False,fontsize=15)
if 'fileC' in dir():
    ax4 = plt.subplot(2,2,4)
    plt.sca(ax4)
    plt.plot(xc,yc,'r-',xc_new,fc(xc_new),'b--')
    plt.legend(['dataC','dataC-interpolate'],loc='best',frameon=False,fontsize=15)
    plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
    plt.ylabel('Intensity (a.u.)',fontsize=15)
for name in [ax1,ax2,ax3]:
    plt.sca(name)
    plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
    plt.ylabel('Intensity (a.u.)',fontsize=15)
plt.show()

if 'fileC' in dir():
    result = leastsq(RamanCombine,[1,1,1,1,1,1,1,1,1])
    A,AA,AAA,B0,B1,B2,B3,B4,B5 = result[0]
    yfit = RamanFit(A,AA,AAA,B0,B1,B2,B3,B4,B5)
    print(f'A = {A}\nA\' = {AA}\nA\" = {AAA}\nB0 = {B0}\n\
B1 = {B1}\nB2 = {B2}\nB3 = {B3}\nB4 = {B4}\n\
B5 = {B5}\nR^2 = {CalculateR_2(y,yfit)}')
else:
    result = leastsq(RamanCombine,[1,1,1,1,1,1,1,1])
    A,AA,B0,B1,B2,B3,B4,B5 = result[0]
    yfit = RamanFit(A,AA,B0,B1,B2,B3,B4,B5)
    print(f'A = {A}\nA\' = {AA}\nB0 = {B0}\n\
B1 = {B1}\nB2 = {B2}\nB3 = {B3}\nB4 = {B4}\n\
B5 = {B5}\nR^2 = {CalculateR_2(y,yfit)}')


plt.figure(figsize=(12,12),dpi=100)
plt.plot(xs_new,y,'r-',xs_new,yfit,'b--')
plt.legend(['origin','fit'],loc='best',frameon=False,fontsize=15)
plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
plt.ylabel('Intensity (a.u.)',fontsize=15)
plt.show()