import os

models =  ['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5', 
          'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg', 
          'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL',
          'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR', 
          'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

ssps = ['ssp585','ssp245']
variables = ['pr','tasmin', 'tasmax']
time = ['2015-2044', '2045-2074', '2075-2100']

for m in models:
	if m == 'CNRM-CM6-1' or m == 'CNRM-CM6-1-HR' or m =='CNRM-ESM2-1':
		variant = 'r1i1p1f2'
	elif m == 'HadGEM3-GC31-LL' or m == 'HadGEM3-GC31-MM':
		variant = 'r1i1p1f3'
	else:
		variant = 'r1i1p1f1'
	for s in ssps:
		for v in variables:
			for t in time:
	
				clipped_path = '../temp/{v}.{m}.{s}.{variant}.{t}.LOCA_16thdeg_clipped_MV.nc'.format(v=v, m=m, s=s, variant = variant, t=t)
				if os.path.isfile(clipped_path):
					print('Exists: {}'.format(clipped_path))
				else: 
					command  = 'cdo sellonlatbox,-71,-70.3,41.1,41.6  ../full_domain/{v}.{m}.{s}.{variant}.{t}.LOCA_16thdeg_v202*****.nc {path}'.format(v=v, m=m, s=s, variant = variant, t=t, path = clipped_path)
					print(command)
					os.system(command)

			merged_path =  '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg.nc'.format(v=v, m=m, s=s)
			if os.path.isfile(merged_path):
				print('Exists: {}'.format(merged_path))
			else: 	
				command = 'cdo mergetime ../temp/{v}.{m}.{s}.{variant}.*.LOCA_16thdeg_clipped_MV.nc {path}'.format(v=v, m=m, s=s, variant = variant, path = merged_path)
				print(command)
				os.system(command)


