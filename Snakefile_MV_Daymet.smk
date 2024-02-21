import os, shutil
from Python.SWBUtilities import run_swb, UpdateControlFile, SWB_daily_to_annual, SWB_daily_to_monthly, scratch, deleteDaily
configfile: "Config_MV.yaml"

activeModelDir = config['modelDir']
controlFile = config['ControlFile']
inputTable = config['InputTable']

start = config['startdate']
end = config['enddate']
ny = config['ny']
nx = config['nx']
variables = config['variables']


prefix = controlFile[0:-4]

rule all:
	input:
		#expand('{activeModelDir}/model/control_file/Daymet.ctl', activeModelDir = activeModelDir),
		#expand('{activeModelDir}/model/output/scratch_directories_made.txt', activeModelDir = activeModelDir),
		#expand('{activeModelDir}/model/output/scratch_Daymet/Daymet_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,  prefix = prefix, start=start, end=end, ny=ny, nx=nx),
		expand('{activeModelDir}/model/output/{prefix}_{variable}__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir, prefix = prefix, start=start, end=end, ny=ny, nx=nx, variable = variables),
		expand('{activeModelDir}/model/output/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir, prefix = prefix, start=start, end=end, ny=ny, nx=nx),
		#expand('{activeModelDir}/model/output/{prefix}_{variable}__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM_mean.tif', activeModelDir = activeModelDir, prefix = prefix, start=start, end=end, ny=ny, nx=nx, variable = variables),
		#expand('{activeModelDir}/model/output/{prefix}_deleted.txt', activeModelDir = activeModelDir, prefix=prefix),



rule RunSWB:
	input:
		expand('{activeModelDir}/model/control_file/{control_file}', activeModelDir = activeModelDir, control_file = controlFile)
	output:
		expand('{activeModelDir}/model/output/scratch_{prefix}/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir, prefix=prefix, start=start, end=end, ny=ny, nx=nx)
	run:
		run_swb(activeModelDir, input[0], output_subdir = prefix)
		

rule swbStatsAnnual:
	input: 
		expand('{activeModelDir}/model/output/scratch_{prefix}/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,   prefix=prefix, start=start, end=end, ny=ny, nx=nx)
	output:
		expand('{activeModelDir}/model/output/{prefix}_{variable}__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  prefix=prefix, start=start, end=end, ny=ny, nx=nx, variable = variables)
	run:
		SWB_daily_to_annual(input[0], output[0], variables)

rule swbStatsMonthly:
	input: 
		expand('{activeModelDir}/model/output/scratch_{prefix}/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,   prefix=prefix, start=start, end=end, ny=ny, nx=nx)
	output:
		expand('{activeModelDir}/model/output/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir,  prefix=prefix, start=start, end=end, ny=ny, nx=nx)
	run:
		SWB_daily_to_monthly(input[0], output[0], variables)


#rule deleteDaily:
	#input: 
	#	expand('{activeModelDir}/model/output/scratch_{prefix}/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir, prefix = prefix, start=start, end=end, ny=ny, nx=nx),
	#	expand('{activeModelDir}/model/output/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  prefix = prefix,  start=start, end=end, ny=ny, nx=nx),
	#	expand('{activeModelDir}/model/output/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_SUM.nc', activeModelDir = activeModelDir,   prefix = prefix, start=start, end=end, ny=ny, nx=nx)
	#output:
	#	expand('{activeModelDir}/model/output/{prefix}_deleted.txt', activeModelDir = activeModelDir, prefix = prefix)
	#run:
	#	deleteDaily(activeModelDir, prefix, output[0])


#rule toTIF:
#	input:
#		expand('{activeModelDir}/model/output/{prefix}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  prefix = prefix,   start=start, end=end, ny=ny, nx=nx),
#	output:
#		expand('{activeModelDir}/model/output/{prefix}_{variable}__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM_mean.tif', activeModelDir = activeModelDir,  prefix = prefix,  start=start, end=end, ny=ny, nx=nx, variable = variables),
#	run:
#		Annual_mean_tif(input[0], variables)

