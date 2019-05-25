# The program was designed to analysis the density profile output
# from the DFT program. The main funtion may read the data file,
# create a colormap from data and calculate the surface area
# Author: lewisbase
# Start Date: 2019.05.24
# Version: 1.0.0
# Finish Date: 2019.05.25

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d
from scipy.integrate import quad

def TransformData(X,Y,DENSITY):
    '''This function is used to transform the x and y to
    vectors and density to 2d martix.'''
    xnew = np.unique(X)
    ynew = np.unique(Y)
    xvector,yvector = np.meshgrid(xnew,ynew)
    DMartix = []
    for j in ynew:
        dmartix = []
        for i in xnew:
            DEN_index = np.intersect1d(np.argwhere(X == i),np.argwhere(Y == j))
            dmartix.append(float(DENSITY[DEN_index]))
        DMartix.append(dmartix)
    return xvector,yvector,DMartix

def ReadDensFile(filename,type='multi'):
    '''This function is used to read the density data file,
    transform the x and y to vectors and density to 2d martix.
    set type as 'single' to read single frame data file'''

    if type == 'single':
        with open(filename,'r') as f:
            text = f.readline().split()
        if len(text) < 3:
            raise Exception('ERROR! The input densxz.dat file is corrupted!')
        else:
            xinitial,yinitial = np.loadtxt(filename,usecols=(0,1),unpack=True)
            dinitial = np.zeros(len(xinitial))
            for column in range(2,len(text)):
                dc = np.loadtxt(filename,usecols=(column))
                dinitial += dc
        X,Y,DENSITY = TransformData(xinitial,yinitial,dinitial)
        TotalFrames = DensityFrame(X,Y,DENSITY)
        

    elif type == 'multi':
        TotalFrames = []
        with open(filename,'r') as f:
            text = f.readlines()
            if len(text) < 3:
                raise Exception('ERROR! The input densxz.dat file is corrupted!')
        framenum = 1
        for word in text:
            if len(word.split()) == 4:
                if framenum != 1:
                    print(f'No.{framenum-1} frame reading complete.')
                    X,Y,DENSITY = TransformData(xinitial,yinitial,dinitial)
                    Frame = DensityFrame(X,Y,DENSITY,frametime)
                    TotalFrames.append(Frame)
                frametime = word.split()[-2]
                print(f'No.{framenum} frame start reading...')
                framenum += 1
                xinitial = np.array([])
                yinitial = np.array([])
                dinitial = np.array([])
            else:
                xinitial = np.append(xinitial,float(word.split()[0]))
                yinitial = np.append(yinitial,float(word.split()[1]))
                dinitial = np.append(dinitial,float(word.split()[2]))
                print(float(word.split()[0]),float(word.split()[1]),float(word.split()[2]))
        print(f'No.{framenum-1} frame reading complete.')
        X,Y,DENSITY = TransformData(xinitial,yinitial,dinitial)
        Frame = DensityFrame(X,Y,DENSITY,frametime)
        TotalFrames.append(Frame)
    else:
        raise Exception('ERROR! type parameter must be set as single or multi!')
    return TotalFrames

class DensityFrame(object):
    '''This class is used to create the density frame object
    the main function contain:
    '''
    def __init__(self,X,Y,DENSITY,TIME=0.0):
        '''The construct function must read three parameters: X, Y and DENSITY.
        X and Y must be a vector, and DENSITY must be a 2d martix.'''
        self.x = X
        self.y = Y
        self.d = np.array(DENSITY)
        self.t = TIME
        #convert the density profile to a high contrast form
        self.hcd = self.d.copy()
        index,column = self.hcd.shape
        for i in range(index):
            for j in range(column):
                if self.hcd[i][j] < 2E-2:
                    self.hcd[i][j] = 0
                else:
                    self.hcd[i][j] = 1

    def DensMap(self,bar='bar',savepicture='no'):
        '''Draw a colormap of density profile.
        Set bar to any other string than 'bar'
        will not show the colorbar, set savepicture
        to picture name will save picture with
        dpi = 300'''
        plt.figure(figsize=(12,12),dpi=100)
        levels = MaxNLocator(nbins=100).tick_values(np.min(self.d),np.max(self.d))
        cm = plt.cm.get_cmap('jet')
        plt.contourf(self.x,self.y,self.d,levels=levels,cmap=cm)
        if bar == 'bar':
            cbar = plt.colorbar()
            cbar.set_label(r'Unit: $\AA^{-3}$',rotation=-90,va='bottom',fontsize=40)
            cbar.ax.tick_params(labelsize=32)
            #cbar.set_ticks([0,2,4,6,8,10])
        plt.legend([f'Time={self.t}ns'],loc='upper left',fontsize=32,frameon=False)
        plt.xlabel(r'X ($\AA$)',fontsize=40)
        plt.ylabel(r'Y ($\AA$)',fontsize=40)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        plt.tight_layout()
        if savepicture != 'no':
            plt.savefig(savepicture,dpi=300)
        plt.show()

    def HighcontrastDensmap(self,bar='nobar',savepicture='no'):
        '''Draw a high contrast map of density profile.
        Set bar to 'bar' will show the colorbar, set 
        savepicture to picture name will save picture 
        with dpi = 300'''
        plt.figure(figsize=(12,12),dpi=100)
        levels = MaxNLocator(nbins=100).tick_values(np.min(self.hcd),np.max(self.hcd))
        cm = plt.cm.get_cmap('Greys')
        plt.contourf(self.x,self.y,self.hcd,levels=levels,cmap=cm)
        if bar == 'bar':
            cbar = plt.colorbar()
            cbar.set_label(r'Unit: $\AA^{-3}$',rotation=-90,va='bottom',fontsize=40)
            cbar.ax.tick_params(labelsize=32)
            #cbar.set_ticks([0,2,4,6,8,10])
        plt.legend([f'Time={self.t}ns'],loc='upper left',fontsize=32,frameon=False)
        plt.xlabel(r'X ($\AA$)',fontsize=40)
        plt.ylabel(r'Y ($\AA$)',fontsize=40)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        plt.tight_layout()
        if savepicture != 'no':
            plt.savefig(savepicture,dpi=300)
        plt.show()

    def SurfaceArea(self):
        '''Calculate the surface area from density profile'''
        fitx = np.array([])
        fity = np.array([])
        index,column = self.hcd.shape
        for i in range(1,int(index/2)):
            for j in range(int(column/2),column-1):
                up    = (i+1,j)
                down  = (i-1,j)
                right = (i,j+1)
                left  = (i,j-1)
                if self.hcd[i][j] == 1 and (self.hcd[up] == 0 or \
                                            self.hcd[down] == 0 or \
                                            self.hcd[right] == 0 or \
                                            self.hcd[left]  == 0):
                    fity = np.append(fity,j*0.5)
                    fitx = np.append(fitx,i*0.5)
        fitxnew = np.unique(fitx)
        fitynew = np.array([])
        for element in fitxnew:
            fitynew = np.append(fitynew, \
                fity[int(np.argwhere(fitx == element)[0])])
        curve = interp1d(fitxnew,fitynew,kind='cubic')
        xfinal = np.linspace(fitxnew.min(),fitxnew.max(),1000,endpoint=True)
        yfinal = curve(xfinal)
        plt.scatter(fitx,fity,c='r')
        plt.scatter(fitxnew,fitynew,c='b')
        plt.plot(xfinal,yfinal)
        plt.show()
        TotalSurfaceArea = Surface(xfinal,yfinal)
        return 2*TotalSurfaceArea


def Der(X,Y):
    '''Calculate the derivative of two array'''
    if len(X) != len(Y):
        raise Exception('ERROR! The length of X and Y must be equal!')
    DerY = np.array([])
    for num in range(1,len(X)):
        Der = (Y[num]-Y[num-1])/(X[num]-X[num-1])
        DerY = np.append(DerY,Der)
    #print('DerY: ',DerY)
    return DerY

def Int(X,Y):
    '''Calculate the integrate of two array'''
    if len(X) != len(Y):
        raise Exception('ERROR! The length of X and Y must be equal!')
    Int = 0
    # The function should be moved on the x axis
    Y = Y-Y.min()
    for num in range(len(Y)-1):
        Int += (Y[num+1]+Y[num])/2*(X[num+1]-X[num])
    #print('Int: ',Int)
    return Int

def Surface(X,Y):
    '''Calculate the surface area of two array'''
    if len(X) != len(Y):
        raise Exception('ERROR! The length of X and Y must be equal!')
    dY = Der(X,Y)
    Surf = Y[1:]*np.sqrt(1+dY**2)
    TotalArea = 2*np.pi*Int(X[1:],Surf)
    #print('dY: ',dY)
    #print('Surf: ',Surf)
    #print('TotalArea: ',TotalArea)
    return TotalArea

if __name__ == 'main':
    main()

def main():
    pass