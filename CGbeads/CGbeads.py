# This project was designed to practice how to use class
# The purpose of the project is to read the coordinate 
# of a molecule and move to other coordinate.
# Author: lewisbase
# Date: 2019.05.09

import numpy as np
import pandas as pd

import dfATOM

class Atom(object):
    def __init__(self,X=0.0,Y=0.0,Z=0.0,M=0.0,Name='Null'):
        '''Define a new atom with coordinate, atom mass
        and atom name'''
        self.x = X
        self.y = Y
        self.z = Z
        self.mass = M
        self.AtomName = Name

class Molecule(object):
    def __init__(self,X=[],Y=[],Z=[],atomsname=[],Name='Null'):
        '''Define a new molecule from a series of coordinate
        , atomsname and molecule name'''
        self.AtomNumber = len(X)
        self.x=np.array(X)
        self.y=np.array(Y)
        self.z=np.array(Z)
        self.MoleculeName = Name
        self.AtomsName = np.array(atomsname)

    def MoleculeMass(self):
        self.MoleculeMass = 0.0
        for name in self.AtomsName:
            self.MoleculeMass += dfATOM.dfAtoms.loc['mass',name]
    
    def MassCenter(self):
        


test1=Atom(1,1,1,12,'C')
test2=Atom(3,3,3,12,'C')
test3=Atom(5,5,5,12,'C')
atoms=np.array([test1,test2,test3])
test4=Molecule(atoms,'C3')
print(test4.AtomNumber,test4.MoleculeMass,test4.MoleculeName)
print(test4.x)
print(test4.y)
print(test4.z)