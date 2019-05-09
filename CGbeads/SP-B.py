# Program to deal with SP-B molecule
# Author: Lewisbase
# Date: 2019.05.09

import CGbeads,ReadFile,dfATOM
import numpy as np 
import pandas as pd 

index,x,y,z=ReadFile.ReadGroFile('em-va.gro')
atomsname=ReadFile.ReadItpFile('Protein_A.itp')

SP_B=CGbeads.Molecule(x,y,z,atomsname,'SP-B')
# coordinate unit is nm
TargetLocation=[3.5,3.5,3.5]
SP_B.MoveMolecule(TargetLocation[0]-SP_B.MassCenter()[0],TargetLocation[1]-SP_B.MassCenter()[1],TargetLocation[2]-SP_B.MassCenter()[2])

# Unit convert to A and K
with open('SP_B-coordinate.dat','w') as f:
    f.write(f'{SP_B.AtomNumber}\n')
with open('SP_B-LJ.dat','w') as f:
    f.write(f'{SP_B.AtomNumber}\n')

for num in range(SP_B.AtomNumber):
    print('%d\t%2.2f\t%2.2f\t%2.2f'%(num+1,10*SP_B.x[num],10*SP_B.y[num],10*SP_B.z[num]))
    with open('SP_B-coordinate.dat','a') as f:
        f.write('%d\t%2.2f\t%2.2f\t%2.2f\n'%(num+1,10*SP_B.x[num],10*SP_B.y[num],10*SP_B.z[num]))
for num in range(SP_B.AtomNumber):
    print('%d\t%2.2f\t%2.2f'%(num+1,10*dfATOM.dfAtoms.loc['sigma',SP_B.AtomsName[num]],120*dfATOM.dfAtoms.loc['epsilon',SP_B.AtomsName[num]]))
    with open('SP_B-LJ.dat','a') as f:
        f.write('%d\t%2.2f\t%2.2f\n' \
            %(num+1,10*dfATOM.dfAtoms.loc['sigma',SP_B.AtomsName[num]],120*dfATOM.dfAtoms.loc['epsilon',SP_B.AtomsName[num]]))
