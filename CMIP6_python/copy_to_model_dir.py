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
			if (m == 'FGOALS-g3' or m == 'INM-CM5-0') and s == 'ssp585' and v=='tasmin':
				old_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_rename.nc'.format(v=v, m=m, s=s)
			else:
				old_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_Celcius.nc'.format(v=v, m=m, s=s)
			new_path = '../../MarthasVineyardSWB/MV_SWB_Phase1/model/input/climate/CMIP6/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_Celcius_Final.nc'.format(v=v, m=m, s=s)

			command = 'cp {} {}'.format(old_path, new_path)			
			print(command)
			os.system(command)

		# pr
		old_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_LONminus360.nc'.format(v='pr', m=m, s=s)
		new_path = '../../MarthasVineyardSWB/MV_SWB_Phase1/model/input/climate/CMIP6/{v}.{m}.{s}.2015-2100.LOCA_16thdeg_Final.nc'.format(v='pr', m=m, s=s)
		command = 'cp {} {}'.format(old_path, new_path)
		print(command)
		os.system(command)
