# This program is designed to analysis the Raman data
# Author: lewisbase
# Date: 2019.06.17


import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import leastsq
from scipy import interpolate
from scipy.signal import savgol_filter
from sys import argv,exit


def CalculateR_2(y1,y2):
    '''calculate the R^2 of regession'''
    Sy1 = np.sum((y1-np.mean(y1))**2)
    Sy2 = np.sum((y2-np.mean(y2))**2)
    Sy1y2 = np.sum((y1-np.mean(y1))*(y2-np.mean(y2)))
    return (Sy1y2/np.sqrt(Sy1*Sy2))**2

def AverageDate(filename):
    filename1 = filename+'-1.txt'
    filename2 = filename+'-2.txt'
    filename3 = filename+'-3.txt'
    x1,y1 = np.loadtxt(filename1,usecols=(0,1),unpack=True)
    x2,y2 = np.loadtxt(filename2,usecols=(0,1),unpack=True)
    x3,y3 = np.loadtxt(filename3,usecols=(0,1),unpack=True)
    x = (x1+x2+x3)/3
    y = (y1+y2+y3)/3
    return x,y

figcolumn = 2

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
            python Raman.py Totaldata SplitdataA SplitdataB ...
            For average the data, each series of data files should be
            named as xxx-1.txt, xxx-2.txt, xxx-3.txt
            There should have 2, 3 or 4 splitdatas.''')
            exit()
        else:
            print('Unknow option!')
            exit()
    else:
        print('a --option or some filenames are needed!')
elif len(argv) == 4:
    def RamanCombine(p):
        a1,a2,b0,b1,b2,b3,b4,b5 = p
        return y-np.abs(a1)*x1-np.abs(a2)*x2-b0-b1*xw-b2*xw**2-b3*xw**3-b4*xw**4-b5*xw**5

    def RamanFit(A1,A2,B0,B1,B2,B3,B4,B5):
        return np.abs(A1)*x1+np.abs(A2)*x2+B0+B1*xw+B2*xw**2+B3*xw**3+B4*xw**4+B5*xw**5
    script,fileS,fileA,fileB = argv
elif len(argv) == 5:
    def RamanCombine(p):
        a1,a2,a3,b0,b1,b2,b3,b4,b5 = p
        return y-np.abs(a1)*x1-np.abs(a2)*x2-np.abs(a3)*x3-b0-b1*xw-b2*xw**2-b3*xw**3-b4*xw**4-b5*xw**5

    def RamanFit(A1,A2,A3,B0,B1,B2,B3,B4,B5):
        return np.abs(A1)*x1+np.abs(A2)*x2+np.abs(A3)*x3+B0+B1*xw+B2*xw**2+B3*xw**3+B4*xw**4+B5*xw**5
    script,fileS,fileA,fileB,fileC = argv
elif len(argv) == 6:
    figcolumn = 3
    def RamanCombine(p):
        a1,a2,a3,a4,b0,b1,b2,b3,b4,b5 = p
        return y-np.abs(a1)*x1-np.abs(a2)*x2-np.abs(a3)*x3-np.abs(a4)*x4-b0-b1*xw-b2*xw**2-b3*xw**3-b4*xw**4-b5*xw**5

    def RamanFit(A1,A2,A3,A4,B0,B1,B2,B3,B4,B5):
        return np.abs(A1)*x1+np.abs(A2)*x2+np.abs(A3)*x3+np.abs(A4)*x4+B0+B1*xw+B2*xw**2+B3*xw**3+B4*xw**4+B5*xw**5
    script,fileS,fileA,fileB,fileC,fileD = argv
else:
    print('Too many parameters!')
    exit()

fileS = fileS+'.txt'
xs,ys = np.loadtxt(fileS,usecols=(0,1),unpack=True)
xa,ya = AverageDate(fileA)
xb,yb = AverageDate(fileB)

ys = (ys-ys.min())/(ys.max()-ys.min())
ya = (ya-ya.min())/(ya.max()-ya.min())
yb = (yb-yb.min())/(yb.max()-yb.min())

xs_new = np.linspace(xs.min(),xs.max(),1000)
xa_new = np.linspace(xa.min(),xa.max(),1000)
xb_new = np.linspace(xb.min(),xb.max(),1000)

fs = interpolate.interp1d(xs,ys)
fa = interpolate.interp1d(xa,ya)
fb = interpolate.interp1d(xb,yb)

x1 = savgol_filter(tuple(fa(xa_new)),7,5)
x2 = savgol_filter(tuple(fb(xb_new)),7,5)
xw = xs_new
y = savgol_filter(tuple(fs(xs_new)),7,5)

if 'fileC' in dir():
    xc,yc = AverageDate(fileC)
    yc = (yc-yc.min())/(yc.max()-yc.min())
    xc_new = np.linspace(xc.min(),xc.max(),1000)
    fc = interpolate.interp1d(xc,yc)
    x3 = savgol_filter(tuple(fc(xc_new)),7,5)
if 'fileD' in dir():
    xd,yd = AverageDate(fileD)
    yd = (yd-yd.min())/(yd.max()-yd.min())
    xd_new = np.linspace(xd.min(),xd.max(),1000)
    fd = interpolate.interp1d(xd,yd)
    x4 = savgol_filter(tuple(fd(xd_new)),7,5)
    

plt.figure(figsize=(12,12),dpi=100)
ax1 = plt.subplot(2,figcolumn,1)
ax2 = plt.subplot(2,figcolumn,2)
ax3 = plt.subplot(2,figcolumn,3)
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
    ax4 = plt.subplot(2,figcolumn,4)
    plt.sca(ax4)
    plt.plot(xc,yc,'r-',xc_new,fc(xc_new),'b--')
    plt.legend(['dataC','dataC-interpolate'],loc='best',frameon=False,fontsize=15)
    plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
    plt.ylabel('Intensity (a.u.)',fontsize=15)
if 'fileD' in dir():
    ax5 = plt.subplot(2,figcolumn,5)
    plt.sca(ax5)
    plt.plot(xd,yd,'r-',xd_new,fd(xc_new),'b--')
    plt.legend(['dataD','dataD-interpolate'],loc='best',frameon=False,fontsize=15)
    plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
    plt.ylabel('Intensity (a.u.)',fontsize=15)
for name in [ax1,ax2,ax3]:
    plt.sca(name)
    plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
    plt.ylabel('Intensity (a.u.)',fontsize=15)
plt.tight_layout()
plt.show()

if ('fileC' in dir()) and not ('fileD' in dir()):
    result = leastsq(RamanCombine,[1,1,1,1,1,1,1,1,1])
    A1,A2,A3,B0,B1,B2,B3,B4,B5 = result[0]
    yfit = RamanFit(A1,A2,A3,B0,B1,B2,B3,B4,B5)
    print(f'''
    A1 = {np.abs(A1)}
    A2 = {np.abs(A2)}
    A3 = {np.abs(A3)}
    B0 = {B0}
    B1 = {B1}
    B2 = {B2}
    B3 = {B3}
    B4 = {B4}
    B5 = {B5}
    R^2 = {CalculateR_2(y,yfit)}''')
elif ('fileC' in dir()) and ('fileD' in dir()):
    result = leastsq(RamanCombine,[1,1,1,1,1,1,1,1,1,1])
    A1,A2,A3,A4,B0,B1,B2,B3,B4,B5 = result[0]
    yfit = RamanFit(A1,A2,A3,A4,B0,B1,B2,B3,B4,B5)
    print(f'''
    A1 = {np.abs(A1)}
    A2 = {np.abs(A2)}
    A3 = {np.abs(A3)}
    A4 = {np.abs(A4)}
    B0 = {B0}
    B1 = {B1}
    B2 = {B2}
    B3 = {B3}
    B4 = {B4}
    B5 = {B5}
    R^2 = {CalculateR_2(y,yfit)}''')
else:
    result = leastsq(RamanCombine,[1,1,1,1,1,1,1,1])
    A1,A2,B0,B1,B2,B3,B4,B5 = result[0]
    yfit = RamanFit(A1,A2,B0,B1,B2,B3,B4,B5)
    print(f'''
    A1 = {np.abs(A1)}
    A2 = {np.abs(A2)}
    B0 = {B0}
    B1 = {B1}
    B2 = {B2}
    B3 = {B3}
    B4 = {B4}
    B5 = {B5}
    R^2 = {CalculateR_2(y,yfit)}''')


plt.figure(figsize=(12,12),dpi=100)
plt.plot(xs_new,y,'r-',xs_new,yfit,'b--')
plt.legend(['origin','fit'],loc='best',frameon=False,fontsize=15)
plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=15)
plt.ylabel('Intensity (a.u.)',fontsize=15)
plt.show()