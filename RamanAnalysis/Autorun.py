# Autorun Raman.py program in a directionary
# Author: lewisbase
# Date: 2019.07.08

import os
import csv

filenum = input('Please input the number of files: \n')
with open('Summary.csv','w',newline='') as csvfile:
    Swriter = csv.writer(csvfile)
    Swriter.writerow(['Name','Skin','Component A','Component B','Component C','R^2',
                    'Precent A','Precent B','Precent C'])
while (int(filenum) != 0):
    filename0 = input('Total data filename: \n')
    filename1 = input('Skin data filename (for average): \n')
    filename2 = input('Component A data filename: \n')
    if int(filenum) == 2:
        os.system(f'python Raman.py {filename0} {filename1} {filename2}')
        # read txt and write into summary csv file
        with open('RamanAnalyse.txt','r') as fi:
            line = fi.readlines()
        with open('Summary.csv','a',newline='') as csvfile:
            Swriter = csv.writer(csvfile)
            Swriter.writerow([filename0,line[0],line[1],'-','-',line[2],
                            str(float(line[1])/float(line[0])),'-','-'])
    elif int(filenum) == 3:
        filename3 = input('Component B data filename: \n')
        os.system(f'python Raman.py {filename0} {filename1} {filename2} {filename3}')
        # read csv and write into summary csv file
        with open('RamanAnalyse.txt','r') as fi:
            line = fi.readlines()
        with open('Summary.csv','a',newline='') as csvfile:
            Swriter = csv.writer(csvfile)
            Swriter.writerow([filename0,line[0],line[1],line[2],'-',line[3],
                            str(float(line[1])/float(line[0])),str(float(line[2])/float(line[0])),'-'])
    elif int(filenum) == 4:
        filename3 = input('Component B data filename: \n')
        filename4 = input('Component C data filename: \n')
        os.system(f'python Raman.py {filename0} {filename1} {filename2} {filename3} {filename4}')
        # read csv and write into summary csv file
        with open('RamanAnalyse.txt','r') as fi:
            line = fi.readlines()
        with open('Summary.csv','a',newline='') as csvfile:
            Swriter = csv.writer(csvfile)
            Swriter.writerow([filename0,line[0],line[1],line[2],line[3],line[4],
                            str(float(line[1])/float(line[0])),str(float(line[2])/float(line[0])),
                            str(float(line[3])/float(line[0]))])
    elif int(filenum) == 0:
        break
    filenum = input('Please input the number of files: \n')