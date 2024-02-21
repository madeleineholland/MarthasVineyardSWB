# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:59:19 2022

@author: mholland
"""

import matplotlib as mpl 
import matplotlib.pyplot as plt
from shapely.geometry import mapping

import numpy as np 
import pandas as pd
import geopandas as gpd
import xarray as xr
import seaborn as sns

from Figures import ReportFigures
rf = ReportFigures()
rf.set_style()
rf.set_style(width='double', height='tall')

def clip(file):
    crs = '+proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs'
    watersheds = gpd.read_file(r"C:\Users\mholland\OneDrive - DOI\Projects\MV\GIS\Major_Watersheds_(With_Coastal_Watersheds)\Major_Watersheds_(With_Coastal_Watersheds).shp")
    data = xr.open_dataset(file)
    data.rio.write_crs(crs, inplace=True)
    data2 = data.rio.clip(watersheds.geometry.apply(mapping), watersheds.crs, drop=True)
    return data2

def summarize(data, variable):
    d = dict()
    alltime = data.sel(time=slice("1981-01-01", "2099-12-31")).mean(dim=['x', 'y']).to_array()
    timeseries  = data.sel(time=slice("1980-01-01", "2005-12-31")).mean(dim=['x', 'y']).to_array()
    print(timeseries)
    d['variable'] =variable
    d['mean']=float(timeseries.mean(dim='time'))
    d['median']=float(timeseries.median(dim='time'))
    d['min']=float(timeseries.min(dim='time'))
    d['max']=float(timeseries.max(dim='time'))
    d['stdev']=float(timeseries.std(dim='time'))
    return d, alltime

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

start='1999-01-01'
end = '2001-12-31'
nx=1182
ny=768

summary = pd.DataFrame(columns = ['variable', 'mean', 'median', 'max', 'min', 'stdev'])
variables = ['gross_precipitation', 'net_infiltration', 'actual_et',]
for RCP in ['RCP45', 'RCP85'][1:2]:
    for model in ['cnrm-cm5', 'csiro-mk3-6-0', 'gfdl-esm2g', 'mpi-esm-mr', 'mri-cgcm3'][0:1]:
        
        fig, ax = plt.subplots()
        i=0
        for var in variables:
            file =  r"C:\Users\mholland\OneDrive - DOI\Projects\MV\SWB\MV_SWB_Phase1/model/output/{model}_{RCP}_{variable}__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_SUM.nc".format(model = model, RCP=RCP, start=start, end= end, nx=nx, ny=ny, variable = var)  
            data = clip(file)  
            d, timeseries = summarize(data,var)
            summary =  summary.append(d, ignore_index=True) 
            window_size = 5
            arr=timeseries.values[0]
            moving_avg = moving_average(arr,5)
            print(arr, moving_avg)
            ax.plot(timeseries.time,arr,  color=sns.color_palette("tab20", 14)[i+1])
            ax.plot(timeseries.time[2:-2], moving_avg, label = var, color=sns.color_palette("tab20", 14)[i])
            i+=2
        ax.set_title(model + ' ' + RCP)
        ax.set_ylabel('(inches)')
        ax.set_ylim([0,10])
        handles, labels = ax.get_legend_handles_labels()
        rf.legend(ax, handles, labels, bbox_to_anchor=(0.15,0.03))




import cartopy.feature as cfeature
import cartopy.crs as ccrs
extent=[-70, -71, 41.1, 41.5

map_proj=ccrs.LambertConformal(central_longitude=-70.5, central_latitude=41, false_easting=500000.0001016, false_northing=0, secant_latitudes=None, standard_parallels=(41.2833333333333, 41.4833333333333), globe=None, cutoff=-30)


plt.figure(figsize=(15,20))
ax = plt.axes(projection=map_proj)
ax.set_extent(extent)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.add_feature(cfeature.BORDERS, edgecolor='black')
ax.add_feature(cfeature.NaturalEarthFeature(
    'cultural', 'admin_1_states_provinces_lines', '50m',
    edgecolor='black', facecolor='none'))
ax.add_feature(cfeature.OCEAN)
m =  ax.pcolormesh(xlc, ylc, LCarr, cmap=cmap, norm=norm)
BasinShapes.boundary.plot(ax=ax,color='black', linestyle = ':',  transform=basin_proj)
studyarea.boundary.plot(ax=ax,color='black', linestyle = '-',  transform=data_proj)
ax.legend(handles=patches, title='Land Use Class', loc='center', bbox_to_anchor=(.85,0.28), fontsize='small', frameon=True, title_fontsize='medium', facecolor='white', framealpha= 1, edgecolor= '0')
plt.savefig(os.path.join(modelDir, 'ancillary', 'post_process', 'figures', 'NLCD_Land_Cover.png'))





path = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_CompareNLCD2019and2001\model\input\nlcd19.asc"
lc2019 = xr.open_dataset(path).band_data.values[0]
plt.imshow(lc2001)


path = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_CompareNLCD2019and2001\model\input\nlcd01.asc"
lc2001 = xr.open_dataset(path).band_data.values[0]
plt.imshow(lc2001)


start='1980-01-01'
end = '2005-12-31'
nx=591
ny=384

summary = pd.DataFrame(columns = ['variable', 'mean', 'median', 'max', 'min', 'stdev'])
var = 'net_infiltration'
RCP = 'RCP45'
model = 'cnrm-cm51'
file1 =  r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_CompareNLCD2019and2001/model/output/{model}_{RCP}_{year}_{variable}__{start}_to_{end}__{ny}_by_{nx}_SUM.nc".format(model = model, RCP=RCP, start=start, end= end, nx=nx, ny=ny, variable = var, year = 2001)  
data = clip(file1)  
d, timeseries = summarize(data,var)
arr1=timeseries.values[0]
file2 =  r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_CompareNLCD2019and2001/model/output/{model}_{RCP}_{year}_{variable}__{start}_to_{end}__{ny}_by_{nx}_SUM.nc".format(model = model, RCP=RCP, start=start, end= end, nx=nx, ny=ny, variable = var, year = 2019)  
data = clip(file2)
d, timeseries = summarize(data,var)
arr2=timeseries.values[0]

diff = (arr2-arr1)/arr2 * 100

fig, ax = plt.subplots()
ax.bar(x=timeseries.time.dt.year, height = diff,  label = 'percent change in net infiltration calculated using NLCD2001 and NLCD2019')
ax.set_ylabel('(% change)')
handles, labels = ax.get_legend_handles_labels()
rf.legend(ax, handles, labels, bbox_to_anchor=(0.35,0.9), title = '')


for RCP in ['RCP45', 'RCP85'][0:1]:
    for model in ['cnrm-cm51', 'csiro-mk3-6-01', 'gfdl-esm2g1', 'mpi-esm-mr1', 'mri-cgcm31'][0:1]:
        
        i=0
        for year in [2001,2019]:
            fig, ax = plt.subplots()
            file =  r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_CompareNLCD2019and2001/model/output/{model}_{RCP}_{year}_{variable}__{start}_to_{end}__{ny}_by_{nx}_SUM.nc".format(model = model, RCP=RCP, start=start, end= end, nx=nx, ny=ny, variable = var, year = year)  
            print(file)
            data = clip(file)  
            d, timeseries = summarize(data,var)
            arr=timeseries.values[0]
            summary =  summary.append(d, ignore_index=True) 
            ax.plot(timeseries.time, arr,  label = year, color=sns.color_palette("tab20", 14)[i+1])
            ax.set_ylim([0,55])

            i+=2
        ax.set_title(model + ' ' + RCP)
        ax.set_ylabel('(inches)')
        handles, labels = ax.get_legend_handles_labels()
        rf.legend(ax, handles, labels, bbox_to_anchor=(0.15,0.03))
