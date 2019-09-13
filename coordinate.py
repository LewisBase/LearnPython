# THis script is designed to calculate the coordinate of Hg atom
# in FangyuanGuo's simulation system
# Author: lewisbase
# Date: 2019.07.22

import numpy as np 
from scipy.optimize import fsolve

def coordinate(p):
    x,y,z,d = p
    return [
            (x-Atom[0][0])**2+(y-Atom[0][1])**2+(z-Atom[0][2])**2-Atom[0][3]**2,
            (x-Atom[1][0])**2+(y-Atom[1][1])**2+(z-Atom[1][2])**2-Atom[1][3]**2,
            (x-Atom[2][0])**2+(y-Atom[2][1])**2+(z-Atom[2][2])**2-Atom[2][3]**2,
            (x-Atom[3][0])**2+(y-Atom[3][1])**2+(z-Atom[3][2])**2-Atom[3][3]**2
    ]

print('Input Other atoms\' coordinate and distance between hg: ')
Atom = np.zeros([4,4])
Para = ['X','Y','Z','Distance']
for num in range(4):
    print(f'No.{num+1}:')
    for parameter in range(4):
        Atom[num,parameter] = input(f'{Para[parameter]}:')

print(Atom)

HgAtom = fsolve(coordinate,[0,0,0,0])
print(HgAtom)