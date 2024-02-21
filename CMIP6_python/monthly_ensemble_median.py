import os

models = ['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5',
          'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg',
          'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL',
          'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR',
          'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

ssps = ['ssp585','ssp245']
variables = ['pr','tasmin', 'tasmax']

for p in ['monthly', 'monthly_mean', 'annual']:
	for s in ssps:
		for v in variables:
			model_path = '../clipped_MV/{p}/{v}.*.{s}.2015-2100.LOCA_16thdeg_fldmean.nc'.format(v=v, s=s, p=p)
			ensemble_path = '../clipped_MV/{p}/{v}.ensemble_median.{s}.2015-2100.LOCA_16thdeg_fldmean.nc'.format(v=v, s=s, p=p)

			if os.path.isfile(ensemble_path):
				print('Exists: {}'.format(ensemble_path))
			else:
				command = 'cdo enspctl,50 {mf} {ef}'.format(mf=model_path, ef=ensemble_path)
				print(command)
				os.system(command)
	
				command = 'cdo ensmax {mf} {ef}'.format(mf=model_path, ef=ensemble_path.replace('median', 'max'))
				print(command)
				os.system(command)

				command = 'cdo ensmin {mf} {ef}'.format(mf=model_path, ef=ensemble_path.replace('median', 'min'))
				print(command)
				os.system(command)


				command = 'cdo enspctl,10 {mf} {ef}'.format(mf=model_path, ef=ensemble_path.replace('median', '10th'))
				print(command)
				os.system(command)

				command = 'cdo enspctl,90 {mf} {ef}'.format(mf=model_path, ef=ensemble_path.replace('median', '90th'))
				print(command)
				os.system(command)


				command = 'cdo ensstd {mf} {ef}'.format(mf=model_path, ef=ensemble_path.replace('median', 'stdev'))
				print(command)
				os.system(command)

