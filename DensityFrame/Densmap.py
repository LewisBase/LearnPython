# Draw a two-dimensional density map from densxz.dat file
# Author: lewisbase
# Date: 2019.05.16
# Update: 2020.03.24
# Update Message: Use argparse to replace sys

import argparse
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

####################################################################################################

def get_parser():
    parser = argparse.ArgumentParser(description='This script is used to draw a two-domensional density map from densxz.dat.')
    parser.add_argument('filename',metavar='FILENAME',type=str,nargs=1,help='string, density file\'s name')
    parser.add_argument('outputname',metavar='OUTPUTNAME',type=str,nargs=1,help='string, output picture\'s name')
    parser.add_argument('colorbar',metavar='COLORBAR',type=bool,nargs=1,help='bool, with or without colorbar')
    return parser

def draw_densmap(filename,outputname,colorbar):
    with open(filename,'r') as f:
        text = f.readline().split()

    if len(text) < 3:
        raise Exception('The input densxz.dat file is corrupted!')
    elif len(text) >= 3:
        xo,zo = np.loadtxt(filename,usecols=(0,1),unpack=True)
        do = np.zeros(len(xo))
        for column in range(2,len(text)):
            dc = np.loadtxt(filename,usecols=(column))
            do += dc
    xo /= 10
    zo /= 10
    do *= 1661.129

    xn = np.unique(xo)
    zn = np.unique(zo)
    xm,zm = np.meshgrid(xn,zn)

    Dm = []
    for j in zn:
        dm = []
        for i in xn:
            do_index=np.intersect1d(np.argwhere(xo == i),np.argwhere(zo == j))
            dm.append(float(do[do_index]))
        Dm.append(dm)

    #######################################################################################################

    plt.figure(figsize=(12,12),dpi=100,frameon=True)
    # set the grids density
    levels = MaxNLocator(nbins=100).tick_values(np.min(Dm),np.max(Dm))
    cm = plt.cm.get_cmap('jet')
    #nm = BoundaryNorm(levels,ncolors=cm.N,clip=True)

    #plt.pcolormesh(xm,zm,Dm,cmap=cm,norm=nm)
    # contourf method is much smoother than pcolormesh!
    plt.contourf(xm,zm,Dm,levels=levels,cmap=cm)
    if colorbar == True:
        cbar = plt.colorbar()
        cbar.set_label('Unit: mol/L',rotation=-90,va='bottom',fontsize=40)
        cbar.set_ticks([0,2,4,6,8,10])
        # set the font size of colorbar
        cbar.ax.tick_params(labelsize=32) 

    plt.xlabel('X (nm)',fontsize=40)
    plt.ylabel('Z (nm)',fontsize=40)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)
    plt.tight_layout()
    plt.savefig(outputname,dpi=300)
    plt.show()

def main():
    """
    This will be called if the script is directly invoked
    """
    # adding command line argument
    parser = get_parser()
    args = vars(parser.parse_args())

    # Set the varibles
    filename = args['filename'][0]
    outputname = args['outputname'][0]
    colorbar = args['colorbar']
    draw_densmap(filename,outputname,colorbar)

if __name__ == '__main__':
    main()

#############################################################################################
#if len(sys.argv) < 2:
#    print('No Action specified.')
#    sys.exit()
#elif len(sys.argv) == 2:
#    if sys.argv[1].startswith('--'):
#        option = sys.argv[1][2:]
#        if option == 'version':
#            print('''
#            Densmap version 1.0.0
#            Author: lewisbase
#            Date: 2019.05.16''')
#            sys.exit()
#        elif option == 'help':
#            print('''
#            This script is used to draw a two-domensional density map from densxz.dat.
#            Options include:
#            --version: Prints the version information
#            --help:    Prints the help information
#            Usage:
#            python Densmap.py filename outputname bar
#            bar is an alternative parameter, input it will generate the colorbar''')
#            sys.exit()
#        else:
#            print('Unknow option!')
#            sys.exit()
#    else:
#        print('We need a --option or two filenames at least!')
#        sys.exit()
#elif len(sys.argv) == 3:
#    script,filename,outputname = sys.argv
#elif len(sys.argv) == 4:
#    script,filename,outputname,bar = sys.argv
#else:
#    print('Too many parameters!')
#    sys.exit()
#
######################################################################################################

