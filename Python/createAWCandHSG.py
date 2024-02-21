# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 15:03:32 2022

@author: mholland
"""
import numpy as np 
import pandas as pd 
import rasterio

fn=r"C:\Users\mholland\OneDrive - DOI\Projects\SACO_SWB\ancillary_data\gssurgoMUKEY.asc"
raster=rasterio.open(fn)
mukey=raster.read(1)


fn=r"C:\Users\mholland\OneDrive - DOI\Projects\SACO_SWB\ancillary_data\gssurgoKey.csv"
key=pd.read_csv(fn)
fn=r"C:\Users\mholland\OneDrive - DOI\Projects\SACO_SWB\ancillary_data\HydrologicSoilGroupKey.csv"
soilkey=pd.read_csv(fn)
df=pd.DataFrame({'mukey':mukey.ravel()}, dtype='int')

for x in key['ID']:
     awc=key.loc[key['ID']==x, 'awc_r']
     awc=float(awc)
     soil=key.loc[key['ID']==x, 'hydgrp'].iloc[0]
     df.loc[df['mukey']==x, 'awc'] = awc
     df.loc[df['mukey']==x, 'soil'] = soil

soildict={soilkey['HydrologicSoilGroup'][i]:int(soilkey['HydrologicSoilNum'][i]) for i in range(len(soilkey))}

df.replace(soildict, inplace=True)


soil_array=np.asarray(df['soil']).reshape(np.shape(mukey))
awc_array=np.asarray(df['awc']).reshape(np.shape(mukey))*12 # convert to in/in to in/ft


awc_array_2 = np.nan_to_num(awc_array, nan=-9999)
soilpath=r"C:\Users\mholland\OneDrive - DOI\Projects\SACO_SWB\model\input\hydsoilgrp.asc"
with rasterio.open(soilpath, 'w', **raster.profile) as dst:
    dst.write(soil_array.astype(rasterio.uint8), 1)


profile = raster.profile    
profile.update({ 
    'dtype':rasterio.float32, 'count':1, 'no_data':-9999})

awcpath=r"C:\Users\mholland\OneDrive - DOI\Projects\SACO_SWB\model\input\awc.asc"
with rasterio.open(awcpath, 'w', **profile) as dst:
    dst.write(awc_array_2.astype(rasterio.float64), 1)
   
    
plt.imshow(soil_array)
