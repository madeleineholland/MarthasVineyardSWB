import os

models =  ['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5',
          'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg',
          'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL',
          'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR',
          'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

ssps = ['ssp585','ssp245']
variables = ['tasmin', 'tasmax']

for m in models:
	for s in ssps:
		for v in variables:
			correct_lon_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_LONminus360.nc'.format(v=v, m=m, s=s)
			celcius_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_Celcius.nc'.format(v=v, m=m, s=s)
			if not os.path.exists(celcius_path):
				command = 'cdo addc,-273.15 {} {}'.format(correct_lon_path, celcius_path)
				print(command)	
				os.system(command)		


for m in ['FGOALS-g3', 'INM-CM5-0']:	
	rename_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_rename.nc'.format(v='tasmin', m=m, s='ssp585')
	celcius_path =  '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_Celcius.nc'.format(v='tasmin', m=m, s='ssp585')
	command = 'cdo chname,tasmax_minus_tasmax_minus_tasmin,tasmin {} {}'.format(celcius_path, rename_path)
	print(command)
	os.system(command)
						
