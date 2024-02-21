# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:39:26 2022

@author: mholland
"""

## convert land use shapefile to raster
import geopandas as gpd
import pandas as pd
from dbfread import DBF
import rasterio
import rasterio.features as features
import numpy as np 
import shutil 

gridfn = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\grid\grid\grid\grid.asc"
grid=rasterio.open(gridfn, 'r')

gridshpfn=r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\grid\grid\MV200grid83ft.shp"
gridshp = gpd.read_file(gridshpfn)



fn2005 = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\landuse2005_poly\LANDUSE2005_POLY.shp"
fnhist = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\landuse_poly\LANDUSE_POLY.shp"
dbfn = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\LandUse\LANDUSE_POLY_HISTORY\LANDUSE_POLY_HISTORY.dbf"

# deal with 2005 LU data
shp2005 = gpd.read_file(fn2005)
shp2005crs = shp2005.to_crs(gridshp.crs)
shp2005clipped = shp2005crs.clip(gridshp)
#reclassificationOLD = {23:21, 24:6, 25:9, 26:7, 27:14, 28:14, 29:9, 31:17, 32:18, 33:17,34:17, 35:21, 36:21, 37:3, 38:13, 39:19, 40:21, 20:-9999}

#1,  Cropland 
#2,  Pasture
#3,  Forest
#4,  Wetland:    includes 14) Salt Wetland
#5,  Mining
#6,  Open Land
#7,  Participation Recreation  
#8,  Spectator Recreation  --> 100) urban
#9,  Water Based Recreation
#10, Residential, multifamily
#11, Residential, <1/4 acre
#12, Residential, 1/4 to 1/2 acre
#13, Residential, >1/2 acre
#14, Salt Wetland
#15, Commercial  ---> 100) urban
#16, Industrial  ---> 100) urban
#17, Urban Open
#18, Transportation  ---> 100) urban
#19, Waste Disposal  --> 17) urban open
#20, Water
#21, Woody Perennial
#23, Cranberry bog  --> 21
#24, Powerlines  --> 6) open land
#25, Saltwater sandy beach --> 9) water based recreation
#26, golf course  --> 7, particpation recreation
#29, marina --> 9) water based recreation
#31, Urban Public/Institutional --> 17) Urban Open 
#33, Heath --> 17) Urban Open
#34, Cemetery --> 17) Urban Open
#36, Orchard --> 21) Woody Perennial 
#37, Forested Wetland --> 3) Forest
#38, Very low density residential 
#39, junkyard --> 17)urban open
#40, Brushland/Successional --> 17) open 

###new categories:
    #100: urban, includes 15, 16, 18, 8
reclassification = {8:100, 15:100, 16:100, 18:100, 19:17, 39:17, 23:21, 24:6, 25:9, 26:7, 29:9, 31:17, 33:17, 34:17, 36:21, 37:3, 38:13, 40:17}

shp2005clip_reclass = shp2005clipped.replace(reclassification)


shphist = gpd.read_file(fnhist)
shphist = shphist.to_crs(gridshp.crs)
shphistclipped=shphist.clip(gridshp)
shphistclipped['RELATEID']=shphistclipped['RELATEID'].astype(str)

dbf = DBF(dbfn)
frame = pd.DataFrame(iter(dbf))
frame['RELATEID']=frame['RELATEID'].astype(str)

shpjoined = shphistclipped.merge(frame, on = 'RELATEID', how='left')
shpjoined_reclass = shpjoined.replace(reclassification)
geom_value_1985 = ((geom,value) for geom, value in zip(shpjoined_reclass.geometry, shpjoined_reclass['LU21_1985']))
geom_value_1999 = ((geom,value) for geom, value in zip(shpjoined_reclass.geometry, shpjoined_reclass['LU21_1999']))
geom_value_2005 = ((geom,value) for geom, value in zip(shp2005clip_reclass.geometry, shp2005clip_reclass['LUCODE']))



# Rasterize vector using the shape and coordinate system of the raster
rasterized_2005 = features.rasterize(geom_value_2005,
                                out_shape = grid.shape,
                                transform = grid.transform,
                                all_touched = True,
                                fill = -9999,   # background value
                              #  merge_alg = MergeAlg.replace,
                                dtype = np.int16)

with rasterio.open(
        r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/GIS/LandUse/rasters/LU21_2005.asc", "w",
        driver = "AAIGrid",
        transform = grid.transform,
        dtype = rasterio.int16,
        crs = grid.crs,
        count = 1,
        width = grid.width,
        height = grid.height, 
        nodata = -9999) as dst:
    dst.write(rasterized_2005, indexes = 1)

rasterized_1985 = features.rasterize(geom_value_1985,
                                out_shape = grid.shape,
                                transform = grid.transform,
                                all_touched = True,
                                fill = -9999,   # background value
                              #  merge_alg = MergeAlg.replace,
                                dtype = np.int16)


with rasterio.open(
        r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/GIS/LandUse/rasters/LU21_1985.asc", "w",
        driver = "AAIGrid",
        transform = grid.transform,
        dtype = rasterio.int16,
        crs = grid.crs,
        count = 1,
        width = grid.width,
        height = grid.height,
        nodata = -9999) as dst:
    dst.write(rasterized_1985, indexes = 1)
    
    
rasterized_1999 = features.rasterize(geom_value_1999,
                                out_shape = grid.shape,
                                transform = grid.transform,
                                all_touched = True,
                                fill = -9999,   # background value
                              #  merge_alg = MergeAlg.replace,
                                dtype = np.int16)


with rasterio.open(
        r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/GIS/LandUse/rasters/LU21_1999.asc", "w",
        driver = "AAIGrid",
        transform = grid.transform,
        dtype = rasterio.int16,
        crs = grid.crs,
        count = 1,
        width = grid.width,
        height = grid.height,
        nodata = -9999) as dst:
    dst.write(rasterized_1999, indexes = 1)
    
    
    
# replicate LULC files to cover all years

years = np.asarray([1985,1999,2005])
breaks0 = (years[1:] + years[:-1]) / 2 +1
breaks = [1980, int(breaks0[0]), int(breaks0[1]), 2100]
chunks = 3

for c in range(0,chunks):
    LUyear = years[c]
    source = r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/GIS/LandUse/rasters/LU21_{}.asc".format(LUyear) 
    source2 = r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/GIS/LandUse/rasters/LU21_{}.prj".format(LUyear) 

    for b in range(breaks[c], breaks[c+1]):
            target = r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/SWB/MV_SWB_Phase1/model/input/LU21_{}.asc".format(b) 
            target2 = r"C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard/SWB/MV_SWB_Phase1/model/input/LU21_{}.prj".format(b) 

            shutil.copy(source, target)
            shutil.copy(source2, target2)
    

