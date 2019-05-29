# test and debug DensityFrame.py
# Author: lewisbase
# Date: 2019.05.25

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
#from scipy.integrate import quad
#from scipy import interpolate
import DensityFrame

test = DensityFrame.ReadDensFile('dens_yz.dat')

Surface = []
with open('surfacearea.dat','w') as f:
    f.write('')
for frame in test:
    #frame.DensMap()
    #frame.HighcontrastDensmap()
    surface = frame.SurfaceArea()
    print(surface)
    with open('surfacearea.dat','a') as f:
        f.write(str(surface)+'\n')
    Surface.append(surface)

plt.plot(range(len(Surface)),Surface)
plt.show()
