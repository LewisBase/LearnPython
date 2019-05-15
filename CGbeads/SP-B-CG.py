#Program to test Atom class
#Generate the input file of coarse_grain program
#Author: lewisbase
#Date: 2019.05.15

import CGbeads,dfATOM,ReadFile

#'''Read the pdb file as lines.
#Return a tuple of atom coordinate(A) and name.'''
filename = '1rg3-back.pdb'
atomsall = []
atom_to_molecule = []
moleculesall = []
with open(filename,'r') as f:
    TotalMessage = f.readlines()
resd_ini = TotalMessage[1].split()[3]
for num in range(len(TotalMessage[1:-1])):
    x = float(TotalMessage[num+1].split()[6])
    y = float(TotalMessage[num+1].split()[7])
    z = float(TotalMessage[num+1].split()[8])
    name = TotalMessage[num+1].split()[-1]
    atom = CGbeads.Atom(x,y,z,name)
    atomsall.append(atom)
    resd = TotalMessage[num+1].split()[3]
    if resd == resd_ini:
        atom_to_molecule.append(atom)
    else:
        molecule = CGbeads.Molecule().MoleculeFromAtom(atom_to_molecule)
        atom_to_molecule = []
        moleculesall.append(molecule)
        resd_ini = resd
        atom_to_molecule.append(atom)
    if num == len(TotalMessage[1:-1])-1:
        molecule = CGbeads.Molecule().MoleculeFromAtom(atom_to_molecule)
        moleculesall.append(molecule)

moleculetotal=CGbeads.Molecule().MoleculeFromAtom(atomsall)
mx,my,mz=moleculetotal.MassCenter()
vector=[35-mx,35-my,35-mz]

for atom in atomsall:
    atom.MoveAtom(vector)
    atom.PrintAtom()
file = 1
for molecule in moleculesall:
    molecule.MoveMolecule(vector)
    molecule.PrintMolecule()
    with open(f'SP_B_{file}-CGinput.dat','w') as f:
        f.write('Temperature  Start    End    Deta    \n')
        f.write('298.0         4.0      12.0   0.01  \n')
        f.write('Number_of_atoms_in_1  Dangle\n')
        f.write('7                      5\n')
        f.write('ID x y z sig epsilon/kB(K) charge(e)  mass\n')
        for num in range(molecule.AtomNumber):
            f.write(str(num+1)+'   '+str('%.2f'%(molecule.x[num]))+'   '+
                str('%.2f'%(molecule.y[num]))+'   '+str('%.2f'%(molecule.z[num]))+
                '   '+str(molecule.sig[num])+'   '+str(molecule.eps[num])+'   '+str(molecule.cha[num])+
                '   '+str(molecule.mass[num])+'\n')
        f.write('Number_of_atoms_in_1  Dangle\n')
        f.write('7                      5\n')
        f.write('ID x y z sig epsilon/kB(K) charge(e)  mass\n')
        for num in range(molecule.AtomNumber):
            f.write(str(num+1)+'   '+str('%.2f'%(molecule.x[num]))+'   '+
                str('%.2f'%(molecule.y[num]))+'   '+str('%.2f'%(molecule.z[num]))+
                '   '+str(molecule.sig[num])+'   '+str(molecule.eps[num])+'   '+str(molecule.cha[num])+
                '   '+str(molecule.mass[num])+'\n')
    file += 1
        

