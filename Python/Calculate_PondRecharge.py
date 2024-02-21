# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 15:26:19 2023

@author: mholland
"""

import geopandas as gpd
import pandas as pd 
import xarray as xr
import numpy as np 
import os 
import matplotlib.pyplot as plt 
import matplotlib as mpl
import random
from Figures import ReportFigures
import glob
rf = ReportFigures()
rf.set_style()
rf.set_style(width='double', height='tall')
mpl.rcParams['figure.dpi'] = 300    

models = ['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5', 
         'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg', 
          'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL', 
          'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR', 
          'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

conversion = 86400 * 0.0393701  #kg/m2/s (summed over month) to inches/day
path2 = r"C:\Users\mholland\Projects\MV\CMIP6\monthly_mean\{var}.{model}.ssp{ssp}.*.2015-2100.LOCA_16thdeg_fldmean.nc"
var = 'pr'
ssp = '245'

df = pd.DataFrame()
df['ET'] = [0,0,0.5,1.2,2.6, 4, 4.3,4.5,3.6,2,1,0]*78       # in inches per month 

for model in models:
    for ssp in ['245', '585']:
        data=xr.open_mfdataset(path2.format(var=var, model=model, ssp=ssp)).sel(time= slice('2023', '2100'))
        col_name_pr = 'precip_{model}_ssp{ssp}'.format(model = model, ssp=ssp)
        df[col_name_pr]  = data.pr.values.ravel()*conversion
        col_name_rech = 'pond_recharge_{model}_ssp{ssp}'.format(model = model, ssp=ssp)
        df[col_name_rech]=df[col_name_pr]-df['ET']


## add in ensemble median 
for ssp in ['245', '585']:
    columns  = ['pond_recharge_{model}_ssp{ssp}'.format(ssp=ssp, model = m) for m in models]
    df['pond_recharge_EnsembleMedian_ssp{ssp}'.format(ssp=ssp)] = df[columns].median(axis=1)
    
df['month']=data.time.dt.month
df['year']=data.time.dt.year
df.to_csv(r"C:\Users\mholland\Projects\MV\AncillaryData\PondRecharge_byModel.csv")



### repeat for Daymet

df = pd.DataFrame()
path = r"C:\Users\mholland\Projects\MV\SWB\MV_SWB_Phase1\model\output\scratch_Daymet\Daymet_gross_precipitation__1999-01-01_to_2022-12-31__768_by_1182.nc"
data = xr.open_dataset(path).sel(time = slice('2000', '2022')).resample(time = "1MS", restore_coord_dims=True).sum(dim='time')
data.gross_precipitation.values[data.gross_precipitation.values==0]=np.nan   #remove inactivate cells from calculation
data2 = data.mean(dim=('x','y')) # mm/month
df['month']=data2.time.dt.month
df['year']=data2.time.dt.year
df['precip_daymet'] = data2.gross_precipitation.values.ravel() # already in inches 
df['ET'] = [0,0,0.5,1.2,2.6, 4, 4.3,4.5,3.6,2,1,0]*23
df['pond_recharge_daymet'] = df['precip_daymet']-df['ET']
df.to_csv(r"C:\Users\mholland\OneDrive - DOI\Desktop\TO_SHAREPOINT\MV\Ancillary\PondRecharge_daymet.csv")
