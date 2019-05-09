# Program to deal with SP-B molecule
# Author: Lewisbase
# Date: 2019.05.09

import CGbeads,ReadFile,dfATOM
import numpy as np 
import pandas as pd 

index,x,y,z=ReadFile.ReadGroFile('em-va.gro')
atomsname=ReadFile.ReadItpFile('Protein_A.itp')

SP_B=CGbeads.Molecule(x,y,z,atomsname,'SP-B')
TargetLocation=[35.0,35.0,35.0]
SP_B.MoveMolecule(TargetLocation[0]-SP_B.MassCenter()[0],TargetLocation[1]-SP_B.MassCenter()[1],TargetLocation[2]-SP_B.MassCenter()[2])
for num in range(SP_B.AtomNumber):
    print(num+1,SP_B.x[num],SP_B.y[num],SP_B.z[num])



print(SP_B.MaxLength())
SP_B.MassCenter()