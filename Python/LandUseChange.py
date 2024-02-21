# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 16:17:44 2022

@author: mholland
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib as mpl
# analyze land use changes MV 1985, 1999, 2005 

LU1971_99 = gpd.read_file(r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\LU_MV_1971-1999.shp")
LU2005 = gpd.read_file(r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\LU_MV_2005.shp")
#reclassification = {7:17, 8:100, 10:100, 15;100,16:100,18:100, 19:100, 39:100, 23:21, 24:6, 25:9, 26:7, 27:14, 28:14, 29:9, 30:20, 31:17, 32:100, 33:17,34:17, 35:21, 36:21, 37:3, 38:13, 40:21}
#LU2005 = LU2005.replace(reclassification)

LU99 = LU1971_99[['LU21_1999','SHAPE_AREA']].groupby(by = 'LU21_1999').sum().rename(columns = {'LU37_1999':'LUCODE', 'SHAPE_AREA':'AREA_1999'})
LU85 = LU1971_99[['LU21_1985','SHAPE_AREA']].groupby(by = 'LU21_1985').sum().rename(columns = {'LU37_1985':'LUCODE', 'SHAPE_AREA':'AREA_1985'})
LU05 = LU2005[['LUCODE', 'AREA']].groupby(by = 'LUCODE').sum().rename(columns = {'AREA':'AREA_2005'})
#LU99.rename(columns = {'LU37_1999':'LU', 'SHAPE_AREA':'AREA_1999'})
#LU85.rename(columns = {'LU37_1985':'LU', 'SHAPE_AREA':'AREA_1985'})
#LU05.rename(columns = {'LUCODE':'LU', 'AREA':'AREA_1985'})


LUall = pd.DataFrame()
LUall['LUCODE'] = LU2005['LUCODE'].drop_duplicates()
LUall = LUall.join(LU99, on = 'LUCODE')
LUall = LUall.join(LU85, on = 'LUCODE')
LUall = LUall.join(LU05, on = 'LUCODE')


#LUall  = LUall.loc[LUall['LU05_DESC']!='Water']
#LUall = LUall.dropna()
LUall['2005 %']=LUall['AREA_2005']/np.sum(LUall['AREA_2005'])
LUall['1999 %']=LUall['AREA_1999']/np.sum(LUall['AREA_1999'])
LUall['1985 %']=LUall['AREA_1985']/np.sum(LUall['AREA_1985'])

LUall = LUall.sort_values(by = 'AREA_2005', ascending = False)
x=np.arange(0,len(LUall))

mpl.rcParams['figure.dpi'] = 300    

fig, ax = plt.subplots()
ax.bar(x-0.25, LUall['1985 %'], width  = 0.25, label='1985')
ax.bar(x, LUall['1999 %'], width  = 0.25, label='1999')
ax.bar(x+0.25, LUall['2005 %'], width  = 0.25, label='2005')

ax.legend(loc = 'upper center', ncol = 3, bbox_to_anchor = [0.5, 1.2])
ax.set_ylabel('% area')
ax.set_xlabel('Land Use')
ax.set_xticks(x)
#ax.set_xticklabels(LUall['LU05_DESC'], rotation = 90)