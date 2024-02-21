import xarray as xr
import geopandas as gpd
import pandas as pd
from shapely.geometry import mapping
import os

print('start') 

crs = "+proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs"
grid = gpd.read_file(r"../Ancillary/grid/MV100grid83ft_clean.shp")
lc = xr.open_dataset(r"../Ancillary/Landuse_land_cover__as_read_into_SWB.asc")
grid['LC']=lc.band_data.values.ravel()

print('opened grid')


####Future
y1=2023
y2=2100+1
pond_recharge = pd.read_csv(r"../Ancillary/PondRecharge_byModel.csv")
#pond_recharge = pond_recharge.loc[(pond_recharge['year']>=y1)&(pond_recharge['year']<=y2)]

print('opened PondRecharge_byModel.csv')


models = ['ACCESS-CM2'] #['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5', 
         #'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg', 
          #'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL', 
         # 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR', 
          #'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

ssps=['245'] # , '585']


for model in models:
	for ssp in ssps:
		output_path = r"../Summary_Output_csv/MV_transient_recharge_2023-2100_ssp{ssp}_{model}.csv".format(ssp=ssp, model=model)
		if os.path.exists(output_path):
			print('exists {}'.format(output_path))
		else: 
			path = r"../SWB/model/output/{model}_ssp{ssp}_net_infiltration__2015-01-01_to_2100-12-31__768_by_1182_MONTHLY_MEAN.nc".format(model = model, ssp=ssp)
			data = xr.open_dataset(path)

			print('opened {model} {ssp}'.format(model=model, ssp=ssp))
	
			for year in range(y1,y2):
				for month in range(1,13):
					rech_mon = data.sel(time = '{month}-{year}'.format(month = month, year = year))
					col_name = '{month}-{year}_{model}'.format(month = month, year = year, model = model)
					grid[col_name]=rech_mon.net_infiltration.values.ravel()/12  #ft/day

			print('assigned SWB values to grid')
        	
			for year in range(y1,y2):
				for month in range(1,13):
					col_name = '{month}-{year}_{model}'.format(month = month, year = year, model = model)
					pond = pond_recharge.loc[(pond_recharge['year']==year)&(pond_recharge['month']==month), 'pond_recharge_{model}_ssp{ssp}'.format(ssp=ssp, model=model)]
					grid.loc[grid['LC']==-11,col_name] = float(pond)/30.4/12

			print('assigned pond values to grid')
        	
			grid.to_csv(output_path)


###Daymet

y1=2000
y2=2022+1
pond_recharge = pd.read_csv(r"../Ancillary/PondRecharge_daymet.csv")

output_path = r"../Summary_Output_csv/MV_transient_recharge_2000-2022.csv"
if os.path.exists(output_path):
    print('exists {}'.format(output_path))

else: 
    path = r"../SWB/model/output/Daymet_net_infiltration__1999-01-01_to_2022-12-31__768_by_1182_MONTHLY_MEAN.nc"
    data = xr.open_dataset(path)

    for year in range(y1,y2):
        for month in range(1,13):
            rech_mon = data.sel(time = '{month}-{year}'.format(month = month, year = year))
            col_name = '{month}-{year}'.format(month = month, year = year)
            grid[col_name]=rech_mon.net_infiltration.values.ravel()/12  #ft/day
            print('assigned SWB values to grid')

    for year in range(y1,y2):
        for month in range(1,13):
            col_name = '{month}-{year}'.format(month = month, year = year)
            pond = pond_recharge.loc[(pond_recharge['year']==year)&(pond_recharge['month']==month), 'pond_recharge_daymet']
            grid.loc[grid['LC']==-11,col_name] = float(pond)/30.4/12      #convert to ft/day averaged over month (assume month is 30.4 days)
    
    grid.to_csv(output_path)