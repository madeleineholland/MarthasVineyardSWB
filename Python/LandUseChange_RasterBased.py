# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 09:21:33 2022

@author: mholland
"""
import pandas as pd
import rasterio 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


years = ['1985', '1999', '2005']
dfall = pd.DataFrame()
dfall['LUCODE']=[ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8., 9., 10., 11., 12., 13., 14.,
       15., 16., 17., 18., 19., 20, 21., np.nan]
dfall['Description'] = ['Cropland', 'Pasture', 'Forest', 'Wetland', 'Mining', 
                        'Open Land', 'Participation Recreation', 'Spectator Recreation', 
                        'Water Based Recreation', 'Residential, Multi-family', 'Residential, <1/4 acre', 
                        'Residential, 1/4-1/2 acre', 'Residential, >1/2 acre', 'Salt Wetland', 
                        'Commercial', 'Industrial', 'Urban Open', 'Transportation', 'Waste Disposal', 
                        'Water', 'Woody Perennial','none']
dfall=dfall.set_index("LUCODE")

woody_perennial = pd.DataFrame()

for y in years:
        df = pd.DataFrame() 
        fn = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\rasters\LU21_{}.asc".format(y)
        array = rasterio.open(fn).read()
        array2 = np.where(array==241, np.nan, array)
        df['LUCODE'], df['counts_'+y] = np.unique(array2, return_counts=True)
        df_indexed = df.set_index("LUCODE")
        dfall = dfall.merge(df_indexed, how ="outer", on = 'LUCODE')
        

fn = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\rasters\LU21_{}.asc".format("2005")
a2005 = rasterio.open(fn).read()
fn = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\rasters\LU21_{}.asc".format("1999")
a1999 = rasterio.open(fn).read()
fn = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\rasters\LU21_{}.asc".format("1985")
a1985 = rasterio.open(fn).read()
change = np.where((a2005 == a1985) & (a1985 == 20), 100, np.nan)
plt.imshow(change[0])

#drop water LU
dfall=dfall.drop(index = 20)
dfall=dfall.drop(index = np.nan)

dfsort = dfall.sort_values(by = 'counts_2005', ascending = False)
df_reind = dfsort.set_index(np.arange(0,len(dfsort)))
df_reind = df_reind.iloc[0:10]

mpl.rcParams['figure.dpi'] = 300    

x=np.arange(0,len(df_reind))
fig, ax = plt.subplots()
ax.bar(x-0.25, df_reind['counts_1985'], width  = 0.25, label='1985')
ax.bar(x, df_reind['counts_1999'], width  = 0.25, label='1999')
ax.bar(x+0.25, df_reind['counts_2005'], width  = 0.25, label='2005')

ax.legend(loc = 'upper center', ncol = 3, bbox_to_anchor = [0.5, 1.2])
ax.set_ylabel('# pixels')
ax.set_xlabel('Land Use')
ax.set_xticks(np.arange(0,10))
ax.set_xticklabels(df_reind.Description, rotation = 90)
