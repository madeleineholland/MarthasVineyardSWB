# -*- coding: utf-8 -*-
"""
Created on Fri May  6 09:15:40 2022

@author: mholland
"""

# download Daymet from 

def downloadDaymet(extent_path, variables, startyear, endyear):

    from pyproj import CRS
    import geopandas as gpd
    import os
    import requests
    
    box=gpd.read_file(extent_path)
    box_prj=box.to_crs(CRS('EPSG:4326'))
    west,south,east,north=box_prj.geometry.total_bounds
    region='na'

    for var in variables:
        for yr in range(startyear, endyear+1):  
            if yr % 4 == 0:  #if leap year
            	  url="http://thredds.daac.ornl.gov/thredds/ncss/grid/ornldaac/1840/daymet_v4_daily_{region}_{var}_{yr}.nc?var=lat&var=lon&var={var}&north={north}&west={west}&east={east}&south={south}&horizStride=1&time_start={yr}-01-01T12:00:00Z&time_end={yr}-12-30T12:00:00Z&timeStride=1&accept=netcdf".format(var=var, yr=yr, region=region, north=north, south=south, east=east, west=west)
            else:
            	  url="http://thredds.daac.ornl.gov/thredds/ncss/grid/ornldaac/1840/daymet_v4_daily_{region}_{var}_{yr}.nc?var=lat&var=lon&var={var}&north={north}&west={west}&east={east}&south={south}&horizStride=1&time_start={yr}-01-01T12:00:00Z&time_end={yr}-12-31T12:00:00Z&timeStride=1&accept=netcdf".format(var=var, yr=yr, region=region, north=north, south=south, east=east, west=west)      
            print(url)
            req = requests.get(url, stream=True)
            destination=os.path.join('SWB','MV_SWB_Phase1', 'model', 'input',  'daymet', '{var}_{yr}.nc'.format(var=var, yr=yr))
            
            with open(destination,'wb') as output_file:
                for chunk in req.iter_content(chunk_size=1025):
                    if chunk:
                        output_file.write(chunk)
                print(chunk)
                
    

extent_path = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\GIS\grid\grid\MV200grid83ft.shp"
variables=['prcp', 'tmax', 'tmin'] 
startyear=1980
endyear=2022


import os
os.chdir(r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard")
downloadDaymet(extent_path, variables, startyear, endyear)
    