# Read the molecule information from .gro and .itp files
# Author: lewisbase
# Date: 2019.05.09

import numpy as np 
import pandas as pd

def ReadGroFile(filename):
    '''Read the gro file to get the coordinate information.
    Return four lists of index, x, y and z'''
    with open(filename,'r') as f:
        row = f.readlines()
    index,x,y,z=np.loadtxt(filename,usecols=(2,3,4,5),skiprows=2,max_rows=int(row[1]),unpack=True)
    for num in range(len(index)):
        print(index[num],x[num],y[num],z[num])
    return index,x,y,z

def ReadItpFile(filename):
    '''Read the itp file to get atom name information.
    Return a list of atom name.'''
    atomnames=np.array([])
    atomindex=np.array([])
    with open(filename,'r') as f:
        TotalMessage = f.readlines()
    for num in range(TotalMessage.index('[ atoms ]\n')+1,TotalMessage.index('[ bonds ]\n')):
        if TotalMessage[num].split():
            print(TotalMessage[num].split()[0],TotalMessage[num].split()[1])
            atomindex=np.append(atomindex,TotalMessage[num].split()[0])
            atomnames=np.append(atomnames,TotalMessage[num].split()[1])
        else:
            print('Attention! A blank line at the end was detected and will be ignored')
            break
    return atomnames




def main():
    pass

if __name__ == '__main__':
    main()