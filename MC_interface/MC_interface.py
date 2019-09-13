# The program is designed to calculate the interface compose 
# Author: lewisbase
# Date: 2019.07.26

import numpy as np 
import matplotlib.pyplot as plt 

class Atom(object):
    '''Hard sphere model is used to described
       the atom, only x, y plane are considered.
    '''
    def __init__(self,sig=0.0,x=0.0,y=0.0):
        self.sig = sig
        self.x = x
        self.y = y