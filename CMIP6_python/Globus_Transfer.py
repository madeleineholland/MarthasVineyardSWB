import os

source_ep="b6534bbc-5bb1-11e9-bf33-0edbf3a4e7ee"
dest_ep="a44287bd-f679-4fe0-a2f2-848688e75996"

variables = ['pr', 'tasmin', 'tasmax']
ssps = ['ssp585', 'ssp245']
times = ['2015-2044', '2045-2074', '2074-2100']
models = ['ACCESS-ESM1-5']

for m in models:
	for s in ssps:
		for v in variables:
			for t in times:
				path = "{v}.{m}.{s}.r1i1p1f1.{t}.LOCA_16thdeg_v20220519.nc".format(s=s,v=v,m=m,t=t)
				#if path.exists()
				command = "globus transfer {source_ep}:/~/loca2-gdo/{m}/0p0625deg/r1i1p1f1/{s}/{v}/{path} {dest_ep}:/caldera/projects/usgs/water/nhvtwsc/mholland/CMIP6/full_domain/{path}".format(source_ep=source_ep, dest_ep=dest_ep, s=s, m=m, v=v, t=t, path = path)    
				print(command)
				os.system(command)
