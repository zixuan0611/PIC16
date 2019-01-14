# import module
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# data set source: http://users.stat.ufl.edu/~winner/datasets.html
"""Dataset: infarct1.dat

Source: P. Schlattman and U. Dirnagl (2010). "Statistics in Experimental 
Cerebrovascular Research: Comparison of More then Two Groups with a 
Continuous Outcome Variable," Journal of Cerebral Blood Flow & Metabolism,
Vol. 30, pp. 1558-1563

Description: Infarct volumes measured histologically after experimental
cerebral artery occlusion in the mouse. Treatments: Vehicle (Control),
Compound X, Compound Y.

Variables/Columns
Treatment   8  /* 1=Vehicle, 2=Compound X, 3=Compound Y */
Infarct Volume    10-16"""

# read the data from the data set
cs = pd.read_table('infarct1.dat', '\s+')

# basic definitions for x-axis and y-axis
type1 = cs['Treatment'] == 1
type2 = cs['Treatment'] == 2
type3 = cs['Treatment'] == 3

# we divide the infarct volumes into three categories
high = cs['Infarct_Volume'] >= 100
mid = (cs['Infarct_Volume'] >= 50) & (cs['Infarct_Volume'] < 100)
low = cs['Infarct_Volume'] < 50
barwidth = .2

plt.axis([-1, 3, 0, 12])
plt.ylabel('Infarct Volume')
plt.xlabel('Treatment')
plt.title('Infarct Volumes of Mice after Cerebal Artery Occlusion ')
plt.xticks(np.arange(3)+1/2, ['Vehicle', 'Compound X', 'Compound Y'])

# draw the bars
plt.bar(np.arange(3), [len(cs[type1 & high].index),
                      len(cs[type2 & high].index),
                      len(cs[type3 & high].index)],
        barwidth, color='r', label='High Infarct Volume')
plt.bar(np.arange(3)+barwidth, [len(cs[type1 & mid].index),
                               len(cs[type2 & mid].index),
                               len(cs[type3 & mid].index)],
        barwidth, color='b', label='Mid Infarct Volume')
plt.bar(np.arange(3)+2*barwidth, [len(cs[type1 & low].index),
                                 len(cs[type2 & low].index),
                                 len(cs[type3 & low].index)],
        barwidth, color='g', label='Low Infarct Volume')

plt.legend()
plt.show()
