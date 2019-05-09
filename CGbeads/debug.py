# Use for debug


import CGbeads,ReadFile,dfATOM

a1=CGbeads.Atom(1,1,1,'AC1')
a2=CGbeads.Atom(3,3,3,'C3')
a3=CGbeads.Atom(5,5,5,'AC2')

m1=CGbeads.Molecule.MoleculeFromAtom([a1,a2,a3])
m2=CGbeads.Molecule([1,1,1],[3,3,3],[5,5,5],['AC1','C3','AC2'])

index,x,y,z=ReadFile.ReadGroFile('em-va.gro')
atomsname=ReadFile.ReadItpFile('Protein_A.itp')

SP_B=CGbeads.Molecule(x,y,z,atomsname,'SP-B')
SP_B.ShowMolecule()
SP_B.PrintMolecule()