# test and debug DensityFrame.py
# Author: lewisbase
# Date: 2019.05.25

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from scipy.integrate import quad
from scipy import interpolate
import DensityFrame

test = DensityFrame.ReadDensFile('densyz.dat')
print(test[1].SurfaceArea())
#x = np.linspace(-1,1,1000)
#y = np.sqrt(1-x**2)

#area = DensityFrame.Surface(x,y)

