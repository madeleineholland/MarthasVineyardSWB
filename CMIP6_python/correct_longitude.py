import os
import xarray as xr 

models =  ['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5', 
          'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg', 
          'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL',
          'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR', 
          'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

ssps = ['ssp585','ssp245']
variables = ['pr','tasmin', 'tasmax']

for m in models:
	for s in ssps:
		for v in variables:
			merged_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg.nc'.format(v=v, m=m, s=s) 
			correct_lon_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_LONminus360.nc'.format(v=v, m=m, s=s)

			data = xr.open_dataset(merged_path)
			data2 = data.assign_coords(lon = data.lon.values-360)

			data2.to_netcdf(path = correct_lon_path)
			print(correct_lon_path)
