# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:14:17 2023
@author: stu

F9 for execute selection
shift enter for execute cell
references:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage


"""
#%%
# =======================
#    Required Packages
# =======================

import requests
import pandas as pd
import io
import numpy as np
import networkx as nx
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt


#%%
# =======================
#    Initialise parameters
# =======================

url = "https://outreach.mathstat.strath.ac.uk/outreach/nessie/datasets/" 
filename = "whiskies.txt"


#%%
# =======================
#    Extract + clean dataset
# =======================

response = requests.get(url+filename).content
df = pd.read_csv(io.StringIO(response.decode('utf-8')))

# examine data column labels
df_top = df.head(5) # limit to top x
list(df_top.columns) # just extract columns labels
list(df_top.index)   # just extract row labels

#prep the data for hierarchical analysis
cleaned_data = df.iloc[:,2:14]   # just retain the 12 scores with col labels
cleaned_data.index = df.iloc[:,1] # add in the row labels
cleaned_data_labels = list(df.iloc[:,1]) # row labels vector)
cleaned_data.to_csv('cleaned_data.csv')


#%%
# =======================
#    Run Analysis
# =======================

temp = hierarchy.linkage(cleaned_data,method='complete', metric='euclidean')
df_hierarchy = pd.DataFrame(temp, columns = ['Col1','Col2','Col3','Col4'])
df_hierarchy.to_csv('linkage_matrix.csv')
'''
 this df is an n x 4 df where each i is a parent cluster and
     [i,0] is child cluster id 1
     [i,1] is child cluster id 2
     [i,2] is distance between id 1 and id 2 at parent cluster level
     [i,3] is number of original clusters contained at parent cluster level
'''

# plot and save dendrogram

plt.rcParams["figure.figsize"] = [9, 9]
#plt.rcParams["figure.autolayout"] = True
plt.figure(dpi=1200)
plt.suptitle('Malt Whisky Chart',fontsize = 'large',
          fontweight='bold', family = 'monospace')
plt.title('Data science and tasting score clusters - Stu v0.1 May 2023'
             ,fontsize = 'medium', family = 'monospace')

dn = hierarchy.dendrogram(temp, above_threshold_color="green",
                          color_threshold=5, labels = cleaned_data_labels,
                          orientation = 'right', leaf_font_size=7)

plt.savefig('dendro_1.pdf', dpi = 1200, )
