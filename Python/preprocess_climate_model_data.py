# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:50:28 2022

@author: mholland
"""

import xarray as xr
import numpy as np 


projections = ['cnrm-cm5', 'csiro-mk3-6-0', 'gfdl-esm2g', 'mpi-esm-mr', 'mri-cgcm3']
for variable in ['pr', 'tasmin', 'tasmax', 'pet_natveg']:
    print(variable)
    for RCP in ['RCP45', 'RCP85']:
       
        
        obs_path = r"C:\Users\mholland\OneDrive - DOI\Projects\MV\AncillaryData\GCM\OBS\1_16obs\Extraction_{variable}.nc".format(variable = variable)
        o = xr.open_dataset(obs_path)
        # remove projection dimension
        o3d = o.sel(projection=0)
        if variable == 'pet_natveg':
            o3d = o3d.rename({'Time':'time', 'Lat':'lat', 'Lon':'lon'})

        oo=o3d.resample(time='1D').first()

        
        print(RCP)
        future_path = r"C:\Users\mholland\OneDrive - DOI\Projects\MV\AncillaryData\GCM\{RCP}\loca5\Extraction_{variable}.nc".format(RCP = RCP, variable = variable)
        f = xr.open_dataset(future_path)  
        if variable == 'pet_natveg':

            f = f.rename({'Time':'time', 'Lat':'lat', 'Lon':'lon'})

        f = f.assign_coords(lon= f.lon-360)
        
        for p in range(0,5):
            projection = projections[p]
            mp = f.sel(projection = p) 
            mp_2006_2099 = mp.where(mp['time.year']>=2006, drop = True)
            # merge datasets (for each RCP)
            #write out
            full = xr.concat([oo, mp_2006_2099], dim='time')
            full = full.rename({'lat':'y', 'lon':'x'})
            if variable == 'pr':
                full = full.rename({'pr':'precipitation'})
            if variable == 'tasmin':
                full = full.rename({'tasmin':'tmin'})
            if variable == 'tasmax':
                full = full.rename({'tasmax':'tmax'})
            if variable == 'pet_natveg':
                full = full.rename({'pet_natveg':'et'})
            
            full2 = full.assign_coords(time = np.arange(0,43830))
            full2.time.attrs = {'standard_name': 'time', 'bounds': 'time_bnds', 'long_name': '24-hour day based on local time', 'CoordinateAxisType': 'Time', 'units': "days since 1980-01-01"}
             
            new_path = r"C:\Users\mholland\OneDrive - DOI\Projects\MV\SWB\MV_SWB_Phase1\model\input\climate\{variable}_{projection}_{RCP}.nc".format(variable = variable, projection = projection, RCP = RCP)
            full2.to_netcdf(path = new_path)


pr =xr.open_dataset("C:\\Users\\mholland\\OneDrive - DOI\\Projects\\SACO_SWB\\model\\input\\climate\\pr_csiro-mk3-6-01_RCP85.nc")
pr=pr.where(pr['time.year']>=2006, drop = True)
prA = pr['precipitation'].resample(time = "1AS", restore_coord_dims=True).sum(dim='time')
PRmean = prA.mean(dim='time')*0.0393701
PRmean.rio.to_raster("C:\\Users\\mholland\\OneDrive - DOI\\Projects\\SACO_SWB\\model\\input\\climate\\PRmean_future.tif")


def moving_average(arr, window_size):
    i = 0
    # Initialize an empty list to store moving averages
    moving_averages = []

    # Loop through the array to consider
    # every window of size 3
    while i < len(arr) - window_size + 1:

        # Store elements from i to i+window_size
        # in list to get the current window
        window = arr[i : i + window_size]

        # Calculate the average of current window
        window_average = sum(window) / window_size

        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
          
        # Shift window to right by one position
        i += 1
    return moving_averages


import xarray as xr
import matplotlib.pyplot as plt
from Figures import ReportFigures
import matplotlib as mpl
import seaborn as sns
rf = ReportFigures()
rf.set_style()
rf.set_style(width='double', height='tall')
mpl.rcParams['figure.dpi'] = 300    
colors = ['orange', 'red' ]
fig,ax = plt.subplots(2, 1, figsize = (5,5))
i=18
for RCP in ['RCP45', 'RCP85']:
    path = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_SWB_Phase1\model\input\climate\tasmax_gfdl-esm2g1_{}.nc".format(RCP)    
    f = xr.open_dataset(path)  
    ts = f.tmax.resample(time = "1AS", restore_coord_dims=True).mean(dim='time').mean(dim=('x','y'))    
    ts10=moving_average(ts, 10)
    ax[0].plot(ts.time.dt.year, ts, color=sns.color_palette("tab20", 20)[i+1], alpha=0.5)
    ax[0].plot(ts.time[4:-5].dt.year, ts10, label=RCP, color=sns.color_palette("tab20", 20)[i])

    ax[0].set_ylabel('maximum temperature (deg C)')
    ax[0].set_xlim([1982, 2095])
    ax[0].set_title("gfdl-esm2g1")
    path = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_SWB_Phase1\model\input\climate\pr_gfdl-esm2g1_{}.nc".format(RCP)    
    f = xr.open_dataset(path)  
    ps = f.precipitation.resample(time = "1AS", restore_coord_dims=True).sum(dim='time').mean(dim=('x','y'))
    ps10=moving_average(ps, 10)
    ax[1].plot(ps.time.dt.year, ps, color=sns.color_palette("tab20", 20)[i+1], alpha=0.5)
    ax[1].plot(ps.time[4:-5].dt.year, ps10, label=RCP, color=sns.color_palette("tab20", 20)[i])
    ax[1].set_ylabel('annual precipitation (mm)')
    ax[1].set_xlim([1982, 2095])
    i-=16
    

ax[0].plot(ts.time[4:21].dt.year, ts10[0:17], color='k', label='historical')
ax[0].plot(ts.time[0:21].dt.year, ts[0:21], color='grey', alpha=0.5)

handles, labels = ax[0].get_legend_handles_labels()
rf.legend(ax[0], handles, labels, bbox_to_anchor=(0.15,0.6), title='')


ax[1].plot(ps.time[4:21].dt.year, ps10[0:17], color='k', label='historical')
ax[1].plot(ps.time[0:21].dt.year, ps[0:21], color='grey', alpha=0.5)
