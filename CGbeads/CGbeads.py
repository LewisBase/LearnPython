# This project was designed to practice how to use class
# The purpose of the project is to read the coordinate 
# of a molecule and move to other coordinate.
# Author: lewisbase
# Date: 2019.05.09

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import dfATOM

class Atom(object):
    def __init__(self,X=0.0,Y=0.0,Z=0.0,NAME='Null',CHARGE=0.0):
        '''Define a new atom with coordinate, LJ, charge, atom mass
        and atom name, the units should be A and K'''
        self.x = X
        self.y = Y
        self.z = Z
        self.sig = dfATOM.dfAtoms.loc['sigma',NAME]
        self.eps = dfATOM.dfAtoms.loc['epsilon',NAME]
        self.mass = dfATOM.dfAtoms.loc['mass',NAME]
        self.AtomName = NAME
        self.cha = CHARGE

    def MoveAtom(self,*args):
        '''Move the atom along the vector input, 3 floats 
        or a 1-d vector with 3 element are allowed to input.'''
        if len(args) == 3:
            xm,ym,zm = args
            self.x += xm
            self.y += ym
            self.z += zm
        elif len(args) == 1:
            xm,ym,zm = args[0][0],args[0][1],args[0][2]
            self.x += xm
            self.y += ym
            self.z += zm
        else:
            raise Exception('The input parameter must be a 3-d vector or 3 floats!')

    def PrintAtom(self,HEADER='n'):
        '''Print the atom information, set Header as y/yes to print the and units'''
        if HEADER.lower() == 'y' or HEADER.lower() == 'yes':
            print('name    X(A)    Y(A)    Z(A)    sigma(A)    epsilon(K)    charge    mass(g/mol)')
        print('%4s    %4.2f    %4.2f    %4.2f    %8.2f    %10.2f    %6.2f    %11.2f'
            %(self.AtomName,self.x,self.y,self.z,self.sig,self.eps,self.cha,self.mass))



class Molecule(object):
    # Main Construct
    def __init__(self,X=[],Y=[],Z=[],ATOMSNAME=[],NAME='Null',CHARGE=[0.0]):
        '''Define a new molecule from a series of coordinate
        , atomsname and molecule name'''
        if not(len(X) == len(Y) and len(X) == len(Z) and len(X) == len(ATOMSNAME)):
            raise Exception('The elements in x, y, z and atomsname must be equal!')
        self.AtomNumber = len(X)
        self.x = X
        self.y = Y
        self.z = Z
        self.MoleculeName = NAME
        self.AtomsName = ATOMSNAME
        self.sig = []
        self.eps = []
        self.mass = []
        for name in self.AtomsName:
            self.sig.append(dfATOM.dfAtoms.loc['sigma',name])
            self.eps.append(dfATOM.dfAtoms.loc['epsilon',name])
            self.mass.append(dfATOM.dfAtoms.loc['mass',name])
        self.MoleculeMass = np.sum(self.mass)
        if len(CHARGE) == 1:
            self.cha = CHARGE*len(X)
        elif len(CHARGE) == len(X):
            self.cha = CHARGE
        else:
            raise Exception('The length of CHARGE list should be equal to other parameter list \
                or set to default zero!')

    # Minor Construct
    @classmethod
    def MoleculeFromAtom(cls,ATOMS,Name='Null'):
        '''Define a new molecule from a series of atoms'''
        X = []
        Y = []
        Z = []
        atomsname = []
        charge = []
        MoleculeName = Name
        for atom in ATOMS:
            X.append(atom.x)
            Y.append(atom.y)
            Z.append(atom.z)
            atomsname.append(atom.AtomName)
            charge.append(atom.cha)
        return cls(X,Y,Z,atomsname,MoleculeName,charge)

    
    def MassCenter(self):
        '''Calculate the mass center of molecule.
        Return the coordinate of mass center.'''
        CenterX = 0.0
        CenterY = 0.0
        CenterZ = 0.0
        for num in range(self.AtomNumber):
            CenterX += self.x[num] * self.mass[num] 
            CenterY += self.y[num] * self.mass[num] 
            CenterZ += self.z[num] * self.mass[num] 
        CenterX /= self.MoleculeMass
        CenterY /= self.MoleculeMass
        CenterZ /= self.MoleculeMass
        return CenterX,CenterY,CenterZ

    def MoveMolecule(self,*args):
        '''Move the molecule along a vector.
        Change the original coordiante.'''
        if len(args) == 3:
            xm,ym,zm = args
            self.x += xm
            self.y += ym
            self.z += zm
        elif len(args) == 1:
            xm,ym,zm = args[0][0],args[0][1],args[0][2]
            self.x += xm
            self.y += ym
            self.z += zm
        else:
            raise Exception('The input parameter must be a 3-d vector or 3 floats!')
    
    def MaxLength(self):
        '''Calculate the max length in x, y, z dimension.
        Return three length.'''
        Max_x = np.max(self.x)-np.min(self.x)
        Max_y = np.max(self.y)-np.min(self.y)
        Max_z = np.max(self.z)-np.min(self.z)
        return Max_x,Max_y,Max_z

    def MassCenterDistance(self,SecondMolecule):
        '''Calculate the distance between two molecules,
        return total distance and distance in x, y and z'''
        firstx,firsty,firstz = self.MassCenter()
        secondx,secondy,secondz = SecondMolecule.MassCenter()
        distance_x = abs(firstx-secondx)
        distance_y = abs(firsty-secondy)
        distance_z = abs(firstz-secondz)
        distance = math.sqrt((distance_x)**2+(distance_y)**2+(distance_z)**2)
        return distance,distance_x,distance_y,distance_z
    
    def ShowMolecule(self):
        '''Show molecule in a 3D scatter figure'''
        fig = plt.figure()
        ax = Axes3D(fig)
        for num in range(self.AtomNumber):
            if num % 2 == 0:
                ScatterColor = 'r'
            else:
                ScatterColor = 'b'
            ax.scatter(xs=self.x[num],ys=self.y[num],zs=self.z[num], \
                s = 4500*dfATOM.dfAtoms.loc['sigma',self.AtomsName[num]], \
                c = ScatterColor)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xlim(np.min([np.min(self.x),np.min(self.y)])-25,np.max([np.max(self.x),np.max(self.y)])+25)
        ax.set_ylim(np.min([np.min(self.x),np.min(self.y)])-25,np.max([np.max(self.x),np.max(self.y)])+25)
        ax.set_zlabel('Z')
        plt.show()
    
    def PrintMolecule(self):
        '''Print the name and cordinate information of molecule'''
        print('NO. AtomName sigma(A) epsilon(K) x(A) y(A) z(A)')
        for num in range(self.AtomNumber):
            print('%3d %8s %8.2f %10.2f %4.2f %4.2f %4.2f' \
                %(num+1,self.AtomsName[num], \
                dfATOM.dfAtoms.loc['sigma',self.AtomsName[num]], \
                dfATOM.dfAtoms.loc['epsilon',self.AtomsName[num]], \
                self.x[num],self.y[num],self.z[num]))



def main():
    pass

if __name__ == '__main__':
    main()