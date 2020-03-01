# This script is design to plot the mmpbsa calculate results
# from Jerkwin's gmx_mmpbsa script
# Author: Lewisbase
# Date: 2020.02.29

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib import font_manager as fm
from matplotlib import cm

def readindata(filename):
    with open(filename) as f:
        text = f.readlines()
    index = []
    data = np.zeros([len(text)-1,len(text[0].split())-1])
    for i in range(1,len(text)):
        index.append(text[i].split()[0])
        for j in range(1,len(text[i].split())):
            if text[i].split()[j] == '|':
                data[i-1][j-1] = np.nan
            else:
                data[i-1][j-1]=float(text[i].split()[j])
    columns = text[0].split()[1:]
    dataframe = pd.DataFrame(data=data,index=index,columns=columns)
    return dataframe

def plot_binding_bar(dataframe):
    '''Plot the bar figure from total MMPBSA data'''
    names = [('Binding Free Energy\nBinding = MM + PB + SA',
             ['Binding','MM','PB','SA']),
             ('Molecule Mechanics\nMM = COU + VDW',
             ['MM','COU','VDW']),
             ('Poisson Boltzman\nPB = PBcom - PBpro - PBlig',
             ['PB','PBcom','PBpro','PBlig']),
             ('Surface Area\nSA = SAcom - SApro - SAlig',
             ['SA','SAcom','SApro','SAlig'])]
    fig,axs = plt.subplots(2,2,figsize=(8,8),dpi=72)
    axs = np.ravel(axs)

    for ax,(title,name) in zip(axs,names):
        ax.bar(name,dataframe[name].mean(),width=0.5,
               yerr=dataframe[name].std(),color='rgby')
        for i in range(len(dataframe[name].mean())):
            ax.text(name[i],dataframe[name].mean()[i],
                    '%.3f'%dataframe[name].mean()[i],
                    ha='center',va='center')
        ax.grid(b=True,axis='y')
        ax.set_xlabel('Energy Decomposition Term')
        ax.set_ylabel('Free energy (kJ/mol)')
        ax.set_title(title)
    plt.suptitle('MMPBSA Results')
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('MMPBSA_Results.png')
    plt.show()



def plot_plot_pie(datas):
    '''Plot the composition curve and pie figure'''
    fig,axs = plt.subplots(2,2,figsize=(8,8),dpi=72)
    axs = np.ravel(axs)

    names = [('Composition of MMPBSA',[0,1,4]),
             ('Composition of MM',[1,2,3]),
             ('Composition of PBSA',[4,5,6])]
    labels = ['res_MMPBSA','resMM','resMM_COU','resMM_VDW',
             'resPBSA','resPBSA_PB','resPBSA_SA']
    colors = ['black','blue','red']
    linestyles = ['-','--',':']
    alphas = [1,0.4,0.4]
    for ax,(title,name) in zip(axs[:-1],names):
        for i in range(len(name)):
            ax.plot(range(datas[name[i]].shape[1]),datas[name[i]].mean(),
                    color=colors[i],alpha=alphas[i],label=labels[name[i]],
                    linestyle=linestyles[i],linewidth=2.5)
        ax.grid(b=True,axis='y')
        ax.set_xlabel('Residues No.')
        ax.set_ylabel('Free Energy Contribution (kJ/mol)')
        ax.legend(loc='best')
        ax.set_title(title)
    
    explode = np.zeros([datas[0].shape[1]])
    maxposition = np.where(datas[0].mean() == datas[0].mean().abs().max())
    maxposition = np.append(maxposition,np.where(datas[0].mean() == 
                            -1 * datas[0].mean().abs().max()))
    explode[maxposition] = 0.4
    colors = cm.rainbow(np.arange(datas[0].shape[1])/datas[0].shape[1])
    patches, texts, autotexts = axs[-1].pie(datas[0].mean()/datas[0].mean().sum()*100,
                explode=explode,labels=datas[0].columns,autopct='%1.1f%%',
                colors=colors,shadow=True,startangle=90,labeldistance=1.1,
                pctdistance=0.8)
    axs[-1].axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
    axs[-1].set_title('Composition of MMPBSA')
    # set font size
    proptease = fm.FontProperties()
    proptease.set_size('xx-small')
    # font size include: xx-small,x-small,small,medium,large,x-large.xx-large or numbers
    plt.setp(autotexts,fontproperties=proptease)
    plt.setp(texts,fontproperties=proptease)
    
    plt.suptitle('MMPBSA Energy Composition')
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('MMPBSA_Energy_Composition.png')
    plt.show()



if __name__ == '__main__':
    pass
    prefix = input('Input the prefix of the calculate results: \n')
    files = ['MMPBSA','res_MMPBSA','resMM','resMM_COU','resMM_VDW',
             'resPBSA','resPBSA_PB','resPBSA_SA']
    datas = []
    for file in files:
        filename = prefix + '~' + file + '.dat'
        datas.append(readindata(filename))
    plot_binding_bar(datas[0])
    plot_plot_pie(datas[1:])