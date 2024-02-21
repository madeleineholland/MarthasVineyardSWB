# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:23:00 2022

@author: mholland
"""

# plot LC, AWC, and HSG maps 


import os
import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
import numpy as np 
import pylab as pl
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import pygeohydro 
import pandas as pd
import xarray as xr
import geopandas as gpd 
from shapely.geometry import mapping

from Figures import ReportFigures

rf = ReportFigures()
rf.set_style()
rf.set_style(width='double', height='tall')
mpl.rcParams['figure.dpi'] = 300    



studyarea  = xr.open_dataset(r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\grid\active.tif")
studyshp = gpd.read_file(r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\grid\grid\MV200grid83ft.shp")

map_proj=ccrs.LambertConformal(central_longitude=-70.5, central_latitude=41, false_easting=1640416.667, false_northing=0, standard_parallels=(41.4833333333333333330,41.28333333333), globe=None, cutoff=-30)
map_proj = ccrs.epsg(6490)
map_proj = '+proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs'
modelDir=r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_SWB_Phase1"

fn=r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\AncillaryData\LandUseKey.csv"
keys=pd.read_csv(fn)

fn=r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_CompareNLCD2019and2001\model\output\daily\Landuse_land_cover__as_read_into_SWB.asc"
LC = xr.open_dataset(fn)
LC.rio.write_crs('+proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs', inplace = True)
LCarr = LC.band_data.values[0,:,:]

LCarr = np.where(studyarea.band_data.values[0,:,:] == 0, 0, LCarr)
xlc=LC.x.values
ylc=LC.y.values

######## 
#plotting settings
mpl.rcParams['figure.dpi'] = 500   
extent=[-70.5, -70.9, 41.25, 41.55]

# plot Land Cover 
cmap, norm, levels_gen = pygeohydro.plot.cover_legends()
cmap.set_under(alpha=0)
cmap.set_bad(alpha=0)
cmap.set_over(alpha=0)

color_list=list(cmap(np.linspace(0, 1, len(levels_gen))))
color_dict={levels_gen[i]: color_list[i] for i in range(len(levels_gen))}
levels=np.unique(LCarr)
levs=levels[1:-1]
labels=[list(keys.loc[keys['Landuse_Code']==x, 'Description'])[0] for x in levs]
label_dict={int(levs[i]):labels[i] for i in range(len(levs))}
patches=[mpl.patches.Patch(color = color_dict[n], label = label_dict[n]) for n in levs]
#lines = [Line2D([0], [0], color='b', linestyle = ':', label = 'Calibration Basins' )]
#patches.append(Line2D([0], [0], color='black', linestyle = ':', label = 'Calibration Basins'))
#patches.append(Line2D([0], [0], color='black', linestyle = '-', label = 'Study Area'))

mpl.rcParams['figure.dpi'] = 1000   
plt.figure(figsize=(15,20))
ax = plt.axes(projection=map_proj)
#ax.set_extent(extent)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.add_feature(cfeature.BORDERS, edgecolor='black')
ax.add_feature(cfeature.NaturalEarthFeature(
   'cultural', 'admin_1_states_provinces_lines', '50m',
    edgecolor='black', facecolor='none'))
ax.add_feature(cfeature.OCEAN)
m =  ax.pcolormesh(xlc, ylc, LCarr, cmap=cmap, norm=norm)
ax.legend(handles=patches, title='Land Use Class', loc='center', bbox_to_anchor=(.14,0.73), fontsize='x-large', frameon=True, title_fontsize='x-large', facecolor='white', framealpha= 1, edgecolor= '0')



# plot hydrologic soil group 
#ST=deepcopy(ST0)
#ST=ST*active_mask
#ST=np.where(ST==-9999, 0, ST)
levels=np.unique(STarr)
cmap=pl.cm.get_cmap('Accent') 
color_list=cmap(np.linspace(0, 1, 8))
color_list[0]=[0,0,0,0]
labels=['No data, inactive cells', 'A Soils', 'A/D Soils', 'B Soils', 'B/D Soils', 'C Soils', 'C/D Soils', 'D Soils']
patches=[mpl.patches.Patch(color = color_list[int(n)], label = labels[int(n)]) for n in levels]
patches.append(Line2D([0], [0], color='black', linestyle = ':', label = 'Calibration Basins'))
patches.append(Line2D([0], [0], color='black', linestyle = '-', label = 'Study Area'))

plt.figure(figsize = (15,20))
ax = plt.axes(projection=map_proj)
ax.set_extent(extent)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.add_feature(cfeature.BORDERS, edgecolor='black')
ax.add_feature(cfeature.NaturalEarthFeature(
    'cultural', 'admin_1_states_provinces_lines', '50m',
    edgecolor='black', facecolor='none'))
ax.add_feature(cfeature.OCEAN)
ax.contourf(x,y,STarr, colors=color_list, levels=levels)
BasinShapes.boundary.plot(ax=ax,color='black', linestyle = ':',  transform=basin_proj)
studyarea.boundary.plot(ax=ax,color='black', linestyle = '-',  transform=data_proj)
ax.legend(handles=patches, title='Hydrologic Soil Group', loc='center', bbox_to_anchor=(.85,0.28), fontsize='small', frameon=True, title_fontsize='medium', facecolor='white', framealpha= 1, edgecolor= '0')
plt.savefig(os.path.join(modelDir, 'ancillary', 'post_process',  'figures', 'HydrologicSoilGroups.png'))



# plot available water capacity 
levels=np.arange(0,5.5,0.5)
levs = np.arange(0,11)
cmap=pl.cm.get_cmap('gnuplot2_r') 
color_list=cmap(np.linspace(0, 1,12))
color_list[0]=[0,0,0,0]
labels = ['No data, inactive cells', '0.01 to 0.5', '0.51 to 1', '1.01 to 1.5', '1.51 to 2', '2.01 to 2.5', '2.51 to 3', '3.01 to 3.5', '3.51 to 4', '4.01 to 4.5', '4.51 to 5', 'greater than 5']
patches=[mpl.patches.Patch(color = color_list[int(n)], label = labels[int(n)]) for n in levs]
patches.append(Line2D([0], [0], color='black', linestyle = ':', label = 'Calibration Basins'))
patches.append(Line2D([0], [0], color='black', linestyle = '-', label = 'Study Area'))

plt.figure(figsize=(15,20))
ax = plt.axes(projection=map_proj)
ax.set_extent(extent)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.add_feature(cfeature.OCEAN, zorder = 1)

m=ax.contourf(x, y, AWCarr, cmap=cmap, levels=levels, zorder = 4)
#cb = pl.colorbar(m, pad=0.05, shrink = 0.4, orientation='vertical', ax=ax)
#cb.ax.set_ylabel('Available Water Content, in inches per foot', fontsize = 15)
#cb.ax.tick_params(labelsize=15)

ax.add_feature(cfeature.BORDERS, edgecolor='black')
ax.add_feature(cfeature.NaturalEarthFeature(
    'cultural', 'admin_1_states_provinces_lines', '50m',
    edgecolor='black', facecolor='none'))
ax.legend(handles=patches, title='Available water capacity,\n in inches per foot of soil thickness', loc='center', bbox_to_anchor=(.85,0.28), fontsize='small', frameon=True, title_fontsize='medium', facecolor='white', framealpha= 1, edgecolor= '0')
BasinShapes.boundary.plot(ax=ax,color='black', linestyle = ':',  transform=basin_proj, zorder = 6)
studyarea.boundary.plot(ax=ax,color='black', linestyle = '-',  transform=data_proj, zorder = 5)
plt.savefig(os.path.join(modelDir, 'ancillary', 'post_process', 'figures', 'AvailableWaterContent.png'))
 
    