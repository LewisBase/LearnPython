# a DataFrame to save atoms information

import pandas as pd 
# sigma nm, epsilon kJ/mol
dfAtoms=pd.DataFrame(
            {
            'AC1':[0.47,3.5,72.0],
            'AC2':[0.47,3.5,72.0],
            'C3':[0.47,3.5,72.0],
            'C5':[0.47,3.5,72.0],
            'N0':[0.47,3.5,72.0],
            'Na':[0.47,2.7,72.0],
            'Nd':[0.47,2.7,72.0],
            'P1':[0.47,4.5,72.0],
            'P4':[0.47,5.0,72.0],
            'P5':[0.62,2.0,72.0],
            'Qa':[0.47,5.0,72.0],
            'Qd':[0.47,5.0,72.0],
            },
            index=['sigma','epsilon','mass'])


def main():
    pass

if __name__ == '__main__':
    main()