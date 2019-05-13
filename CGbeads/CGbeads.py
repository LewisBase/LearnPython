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
    def __init__(self,X=0.0,Y=0.0,Z=0.0,S=0.0,E=0.0,C=0.0,M=0.0,Name='Null'):
        '''Define a new atom with coordinate, LJ, charge, atom mass
        and atom name'''
        self.x = X
        self.y = Y
        self.z = Z
        self.sig = S
        self.eps = E
        self.cha = C
        self.mass = M
        self.AtomName = Name

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


class Molecule(object):
    # Main Construct
    def __init__(self,X=[],Y=[],Z=[],atomsname=[],Name='Null'):
        '''Define a new molecule from a series of coordinate
        , atomsname and molecule name'''
        if not(len(X) == len(Y) and len(X) == len(Z) and len(X) == len(atomsname)):
            raise Exception('The elements in x, y, z and atomsname must be equal!')
        self.AtomNumber = len(X)
        self.x = X
        self.y = Y
        self.z = Z
        self.MoleculeName = Name
        self.AtomsName = atomsname
        self.MoleculeMass = 0.0
        for name in self.AtomsName:
            self.MoleculeMass += dfATOM.dfAtoms.loc['mass',name]

    # Minor Construct
    @classmethod
    def MoleculeFromAtom(cls,Atoms,Name='Null'):
        '''Define a new molecule from a series of atoms'''
        X=[]
        Y=[]
        Z=[]
        atomsname=[]
        MoleculeName=Name
        for atom in Atoms:
            X.append(atom.x)
            Y.append(atom.y)
            Z.append(atom.z)
            atomsname.append(atom.AtomName)
        return cls(X,Y,Z,atomsname,MoleculeName)

    
    def MassCenter(self):
        '''Calculate the mass center of molecule.
        Return the coordinate of mass center.'''
        CenterX = 0.0
        CenterY = 0.0
        CenterZ = 0.0
        for num in range(self.AtomNumber):
            CenterX += self.x[num] * dfATOM.dfAtoms.loc['mass',self.AtomsName[num]]
            CenterY += self.y[num] * dfATOM.dfAtoms.loc['mass',self.AtomsName[num]]
            CenterZ += self.z[num] * dfATOM.dfAtoms.loc['mass',self.AtomsName[num]]
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
        Max_x=np.max(self.x)-np.min(self.x)
        Max_y=np.max(self.y)-np.min(self.y)
        Max_z=np.max(self.z)-np.min(self.z)
        return Max_x,Max_y,Max_z

    def MassCenterDistance(self,SecondMolecule):
        '''Calculate the distance between two molecules,
        return total distance and distance in x, y and z'''
        firstx,firsty,firstz = self.MassCenter()
        secondx,secondy,secondz = SecondMolecule.MassCenter()
        distance_x=abs(firstx-secondx)
        distance_y=abs(firsty-secondy)
        distance_z=abs(firstz-secondz)
        distance = math.sqrt((distance_x)**2+(distance_y)**2+(distance_z)**2)
        return distance,distance_x,distance_y,distance_z
    
    def ShowMolecule(self):
        '''Show molecule in a 3D scatter figure'''
        fig=plt.figure()
        ax=Axes3D(fig)
        for num in range(self.AtomNumber):
            if num % 2 == 0:
                ScatterColor = 'r'
            else:
                ScatterColor = 'b'
            ax.scatter(xs=self.x[num],ys=self.y[num],zs=self.z[num], \
                s=4500*dfATOM.dfAtoms.loc['sigma',self.AtomsName[num]], \
                c=ScatterColor)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
    
    def PrintMolecule(self):
        '''Print the name and cordinate information of molecule'''
        print('NO. AtomName sig(nm) eps(kJ/mol) X(nm) Y(nm) Z(nm)')
        for num in range(self.AtomNumber):
            print('%d\t%s\t%2.2f\t%2.2f\t%2.2f\t%2.2f\t%2.2f' \
                %(num+1,self.AtomsName[num], \
                dfATOM.dfAtoms.loc['sigma',self.AtomsName[num]], \
                dfATOM.dfAtoms.loc['epsilon',self.AtomsName[num]], \
                self.x[num],self.y[num],self.z[num]))



def main():
    pass

if __name__ == '__main__':
    main()