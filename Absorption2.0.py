#拟合BET数据中的吸附曲线并计算吸附焓
#Version 2.00
#以实现对数据的读取，转化单位和langmuir方程拟合并做图
#对BET软件直接生成的xls文件尚不能直接打开，需要另存为xlsx格式
#Author: lewisbase
#Date: 2019.04.08

import csv
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import rcParams
from scipy.optimize import leastsq

GRID=30000
R=8.314510e-3
###############################################################################################

def Langmuir(c):
    b=c
    return y-qmax*b*x/(1+b*x)
def Langmuirfit(x):
    return qmax*b*x/(1+b*x)
def Freundlich(f):
    k,l=f
    return y-k*x**(1/l)
def Freundlichfit(x):
    return k*x**(1/l)

###############################################################################################

print("Welcome to absorption calculator! Please follow the hinds and input the right message.")
ifheat=input("Would you like to caiculate the heat of absorption?(Y/N)")
if ifheat == "Y" or ifheat == "y":
    T1=input("Input the first temperature:\n")
    filename1=input("Input the filename of T1:\n")
    T2=input("Input the second temperature:\n")
    filename2=input("Input the filename of T2:\n")
    read1=pd.read_excel(filename1,usecols="L,M",header=None,convert_float=True,dtype=float,skiprows=28)
    read1=np.array(read1,dtype=float)
    x1=np.array([])
    for x in read1[:,0]:
        if not np.isnan(x):
            #print(x)
            x1=np.append(x1,x)
    y1=np.array([])
    for y in read1[:,1]:
        if not np.isnan(y):
            #print(y)
            y1=np.append(y1,y)
    read2=pd.read_excel(filename2,usecols="L,M",header=None,convert_float=True,dtype=float,skiprows=28)
    read2=np.array(read1,dtype=float)
    x2=np.array([])
    for xbuff in read2[:,0]:
        if not np.isnan(xbuff):
            #print(x)
            x2=np.append(x2,xbuff)
    y2=np.array([])
    for ybuff in read2[:,1]:
        if not np.isnan(ybuff):
            #print(y)
            y2=np.append(y2,ybuff)
    x1*=101.325
    x2*=101.325
else:
    T1=input("Input the temperature:\n")
    filename1=input("Input the filename:\n")
    read1=pd.read_excel(filename1,usecols="L,M",header=None,dtype=float,skiprows=28)
    read1=np.array(read1,dtype=float)
    x1=np.array([])
    for xbuff in read1[:,0]:
        if not np.isnan(xbuff):
            #print(x)
            x1=np.append(x1,xbuff)
    y1=np.array([])
    for ybuff in read1[:,1]:
        if not np.isnan(ybuff):
            #print(y)
            y1=np.append(y1,ybuff)
    x1*=101.325
print(x1)
print(y1)

#####################################################################################################

print("Please choose the absorption model you want to use: 1. Langmuir; 2. Freundlich\n")
model=int(input("Input the number: \n"))
while model!=1 and model!=2:
    print("Sorry, this program currently only supports the above two models. Please input 1 or 2.")
    model=int(input("Input the number: \n"))
if model==1:
    print("You choose the Langmuir model, mission start!\n")
    qmax=np.max(y1)
    x=x1
    y=y1
    result1=leastsq(Langmuir,[1])
    a1=result1[0]
    #aerr1,berr1=result1[1]
    xfit1=np.linspace(0,np.max(x1),GRID,endpoint=True)
    b=a1
    yfit1=np.array([])
    for x in xfit1:
        yfit1=np.append(yfit1,Langmuirfit(x))
    print("The fit coefficient at {0} is: ".format(T1),a1)#,aerr1,berr1)
    if ifheat == "Y" or ifheat == "y":
        qmax=np.max(y2)
        x=x2
        y=y2
        result2=leastsq(Langmuir,[1])
        a2=result1[0]
        #aerr2,berr2=result2[1]
        xfit2=np.linspace(0,np.max(x2),GRID,endpoint=True)
        b=a2
        yfit2=np.array([])
        for x in xfit2:
            yfit2=np.append(yfit2,Langmuirfit(x))
        print("The fit coefficient at {0} is: ".format(T2),a2)#,aerr2,berr2)
elif model==2:
    print("You choose the Freundlich model, mission start!\n")
    x=x1
    y=y1
    result1=leastsq(Freundlich,[1,1])
    a1,b1=result1[0]
    #aerr1,berr1=result1[1]
    xfit1=np.linspace(0,np.max(x1),GRID,endpoint=True)
    k=a1
    l=b1
    yfit1=np.array([])
    for x in xfit1:
        yfit1=np.append(yfit1,Freundlichfit(x))
    print("The fit coefficient at {0} is: ".format(T1),a1,b1)#,aerr1,berr1)
    if ifheat == "Y" or ifheat == "y":
        x=x2
        y=y2
        result2=leastsq(Freundlich,[1,1])
        a2,b2=result1[0]
        #aerr2,berr2=result2[1]
        xfit2=np.linspace(0,np.max(x2),GRID,endpoint=True)
        k=a2
        l=b2
        yfit2=np.array([])
        for x in xfit2:
            yfit2=np.append(yfit2,Freundlichfit(x))
        print("The fit coefficient at {0} is: ".format(T2),a2,b2)#,aerr2,berr2)
#################################################################################################
if ifheat == "Y" or ifheat == "y":
    DP=np.array([])
    Qfin=np.array([])

    length=0
    for i in range(GRID):
        for j in range(GRID):
            if abs(yfit1[i]-yfit2[j])<1E-6 and xfit2[j] != 0:
                DP=np.append(DP,xfit1[i]/xfit2[j])
                Qfin=np.append(Qfin,yfit1[i])
                length+=1
                continue
    
    DH=np.zeros([length])
    for k in range(length):
        DH[i]=R*math.log(DP[k])/(1/T2-1/T1)
    
    with open('Output.csv','w',newline='') as csvfile:
        Owriter=csv.writer(csvfile)
        Owriter.writerow('Q','DH')
        for k in range(length):
            Owriter.writerow([Qfin[k],DH[k]])
#################################################################################################
plt.figure(figsize=(10,5),dpi=80)
ax1=plt.subplot(1,2,1)
plt.sca(ax1)
plt.xlabel("Pressure (Pa)")
plt.ylabel(r"Q ($\frac{cm^{3}}{g}$)")
plt.scatter(x1,y1,label="{0}K experiment".format(T1))
plt.plot(xfit1,yfit1,label="{0}K fit".format(T1),linestyle="--")
plt.legend(loc="best")
if ifheat == "Y" or ifheat == "y":
    ax2=plt.subplot(1,2,2)
    plt.sca(ax1)
    plt.plot(x2,y2,label="{0}K experiment".format(T2))
    plt.plot(xfit2,yfit2,label="{0}K fit".format(T2),linestyle="--")
    plt.sca(ax2)
    #ax2.plt.xlabel()
    #ax2.plt.ylabel()
    plt.plot(DP,Qfin)
plt.savefig("Absorption.png",dpi=300)
plt.show()