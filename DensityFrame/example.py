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
for frame in test:
    frame.DensMap()
    frame.HighcontrastDensmap()
    print(frame.SurfaceArea())
