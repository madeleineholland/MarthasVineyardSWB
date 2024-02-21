import os, shutil
from Python.SWBUtilities import run_swb, UpdateControlFile, SWB_daily_to_annual, SWB_daily_to_monthly, scratch, deleteDaily, EnsembleMedian

configfile: "Config_MV_future.yaml"

activeModelDir = config['modelDir']
controlFile = config['ControlFile']
inputTable = config['InputTable']

start = config['startdate']
end = config['enddate']
ny = config['ny']
nx = config['nx']
RCPs = config['RCP']
models = config['models']
variables = config['variables']


#wildcard_constraints:
#	mod='[]+'
	

rule all:
	input:
		expand('{activeModelDir}/model/control_file/{model}_{scenario}.ctl', activeModelDir = activeModelDir,  model=models, scenario=RCPs),
		expand('{activeModelDir}/model/output/scratch_directories_made.txt', activeModelDir = activeModelDir),
		#expand('{activeModelDir}/model/output/scratch_{model}_{scenario}/{model}_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, model=models, scenario=RCPs),
		expand('{activeModelDir}/model/output/{model}_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, model=models, scenario=RCPs),
		expand('{activeModelDir}/model/output/{model}_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, model=models, scenario=RCPs),
		expand('{activeModelDir}/model/output/{model}_{scenario}_deleted.txt', activeModelDir = activeModelDir, model=models, scenario=RCPs),
#		expand('{activeModelDir}/model/output/EnsembleMedian_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, scenario=RCPs),
#		expand('{activeModelDir}/model/output/EnsembleMedian_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, scenario=RCPs)


rule UpdateControlFile:
	input:
		expand('{activeModelDir}/model/control_file/{control_file}', activeModelDir = activeModelDir, control_file = controlFile)
	output:
		expand('{activeModelDir}/model/control_file/{model}_{scenario}.ctl', activeModelDir = activeModelDir, model=models, scenario=RCPs)
	run:
		UpdateControlFile(input[0], config['InputTable'], start, end, nx, ny, models, RCPs)


rule makeSrcDir:
	input:
		expand('{activeModelDir}/model/control_file/{control_file}', activeModelDir = activeModelDir, control_file = controlFile)
	output:
		expand('{activeModelDir}/model/output/scratch_directories_made.txt', activeModelDir = activeModelDir)
	run:
		scratch(activeModelDir, models, RCPs)

rule RunSWB:
	input:
		expand('{activeModelDir}/model/control_file/{{mod}}.ctl', activeModelDir = activeModelDir),
		expand('{activeModelDir}/model/output/scratch_directories_made.txt', activeModelDir = activeModelDir)
	output:
		expand('{activeModelDir}/model/output/scratch_{{mod}}/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx)
	run:
		run_swb(activeModelDir, input[0], output_subdir = wildcards.mod)
		

rule swbStatsAnnual:
	input: 
		expand('{activeModelDir}/model/output/scratch_{{mod}}/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx)
	output:
		expand('{activeModelDir}/model/output/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx)
	run:
		SWB_daily_to_annual(input[0], output[0], variables)

rule swbStatsMonthly:
	input: 
		expand('{activeModelDir}/model/output/scratch_{{mod}}/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx)
	output:
		expand('{activeModelDir}/model/output/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx)
	run:
		SWB_daily_to_monthly(input[0], output[0], variables)


rule deleteDaily:
	input: 
		expand('{activeModelDir}/model/output/scratch_{{mod}}/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx),
		expand('{activeModelDir}/model/output/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx),
		expand('{activeModelDir}/model/output/{{mod}}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx)
	output:
		expand('{activeModelDir}/model/output/{{mod}}_deleted.txt', activeModelDir = activeModelDir)
	run:
		deleteDaily(activeModelDir, wildcards.mod, output[0])

rule ensembleMedian:
	input:
		expand('{activeModelDir}/model/output/{model}_{scenario}_deleted.txt', activeModelDir = activeModelDir, model=models, scenario=RCPs)
	output:
		expand('{activeModelDir}/model/output/EnsembleMedian_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_YEARLY_SUM.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, scenario=RCPs),
		expand('{activeModelDir}/model/output/EnsembleMedian_{scenario}_net_infiltration__{start}_to_{end}__{ny}_by_{nx}_MONTHLY_MEAN.nc', activeModelDir = activeModelDir,  start=start, end=end, ny=ny, nx=nx, scenario=RCPs)
	run:
		EnsembleMedian(output[0], models, variables)




