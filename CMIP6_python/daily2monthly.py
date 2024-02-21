import os

models = ['ACCESS-ESM1-5', 'ACCESS-CM2', 'AWI-CM-1-1-MR', 'BCC-CSM2-MR', 'CanESM5',
          'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3-Veg',
          'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL',
          'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-HR',
          'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM']

ssps = ['ssp585','ssp245']
variables = ['pr','tasmin', 'tasmax']

for m in models:

	# most models have variant r1i1p1f1, but a few do not, so we select the next variant
	if m == 'CNRM-CM6-1' or m =='CNRM-ESM2-1':
		variant = 'r1i1p1f2'
	elif m == 'HadGEM3-GC31-LL' :
		variant = 'r1i1p1f3'
	else:
		variant = 'r1i1p1f1'


	for s in ssps:
		for v in variables:
			daily_path = '../clipped_MV/daily/{v}.{m}.{s}.2015-2100.LOCA_16thdeg.nc'.format(v=v, m=m, s=s)
			mmf = daily_path.replace('daily', 'monthly_mean')
			mf = daily_path.replace('daily', 'monthly')
			yf = daily_path.replace('daily', 'annual')

			if v == 'pr':
				f1 = 'monsum'
				f2 = 'ymonsum'
				f3 = 'yearsum'
			
			else:
				f1 = 'monmean'
				f2 = 'ymonmean'
				f3 = 'yearmean'
			command = 'cdo {func} {df} {mmf}'.format(func=f1, df=daily_path, mmf= mmf)
			print(command)
			os.system(command)
			command = 'cdo fldmean {mmf} {mmf_am}'.format(mmf=mmf, mmf_am = mmf.replace(".nc" , "_fldmean.nc"))
			print(command)
			os.system(command)

			command = 'cdo {func} {df} {mf}'.format(func=f2, df=daily_path, mf= daily_path.replace('daily', 'monthly'))
			print(command)
			os.system(command)
			command = 'cdo fldmean {mf} {mf_am}'.format(mf=mf, mf_am=mf.replace('.nc', '_fldmean.nc'))
			print(command)
			os.system(command)

			command = 'cdo {func} {df} {yf}'.format(func=f3, df=daily_path, yf = daily_path.replace('daily', 'annual'))
			print(command)
			os.system(command)
			command = 'cdo fldmean {yf} {yf_am}'.format(yf=yf, yf_am = yf.replace('.nc', '_fldmean.nc'))
			print(command)
			os.system(command)
