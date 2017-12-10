"""
Vertrekt van de tijdreeksen van de features van het teamleader ecosysteem.
Input:
    - Feature 
    - Specifiek bedrijf in het teamleader ecosysteem
Output:

    - Boxplot voor het bedrijf en de feature
"""

import sys

if sys.argv[1] == '-h':
    print("<pivot_table.py -feature -firm(s) >")
    quit()
    
import pandas as pd
import numpy as np
import pickle  
import matplotlib.pyplot as plt
import seaborn as sns




feature = sys.argv[1]
firm = sys.argv[2]
firms = sys.argv[2:]
print(firms)

pivot_tables = pickle.load(open('pivot_tables.p', 'rb'))


try:
    if len(sys.argv) > 3:
        print(pivot_tables[feature][firms].describe())
        pivot_tables[feature][firms].plot(kind='box')
    else:
        print(pivot_tables[feature][[firm]].describe())
        pivot_tables[feature][[firm]].plot(kind='box')
    plt.title('Boxplot of feature '+ feature)
    plt.ylabel(feature)
    plt.show()
except:
    print('Feature or Firm not recognized')
    quit()

quit()

