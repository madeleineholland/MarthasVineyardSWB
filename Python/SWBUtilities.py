# -*- coding: utf-8 -*-
"""
Created on Fri May  6 09:15:40 2022

@author: mholland
"""

import numpy as np
import xarray as xr
import xrspatial as xrs
import os
import geopandas as gpd
import pandas as pd 
from shapely.geometry import mapping
import shutil

#controlFileTemplate =  r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_SWB_Phase1/model/control_file/SWB_MV_original.ctl"
#newLookupTable = r"C:\Users\mholland\OneDrive - DOI\Projects\MarthasVineyard\SWB\MV_SWB_Phase1\model\std_input\MVLookup_NLCD.txt"
#nx= 591
#ny= 384
#startDT= "1980-01-01"
#endDT= "2099-12-31"
#RCPs= ["RCP45", "RCP85"]
#models= ['cnrm-cm51', 'csiro-mk3-6-01', 'gfdl-esm2g1', 'mpi-esm-mr1', 'mri-cgcm31']
#modelDir = 'MV_SWB_Phase1'

def UpdateControlFile(controlFileTemplate,newLookupTable,startDT,endDT,nx,ny, models, RCPs, NLCDyear='19'):
    with open(controlFileTemplate, 'r', encoding= 'unicode_escape') as file :
        filedata = file.read()
    
    # Replace the target string
    filedata = filedata.replace('{{PATH_TO_CALIBRATION_LOOKUP_TABLE}}', newLookupTable)
    filedata = filedata.replace('START_DATE start date','START_DATE {}/{}/{}'.format(startDT.split("-")[1],startDT.split("-")[2],startDT.split("-")[0]))
    filedata = filedata.replace('END_DATE end date', 'END_DATE {}/{}/{}'.format(endDT.split("-")[1],endDT.split("-")[2],endDT.split("-")[0]))
    filedata = filedata.replace('GRID 591 384','GRID {} {}'.format(str(nx),str(ny)))
    if NLCDyear:
        filedata = filedata.replace('{{LANDUSE FILE}}','nlcd{}.asc'.format(NLCDyear))

    for p in models:
        for s in RCPs:
            filedata2 = filedata.replace('{{RCP}}',s)
            filedata2 = filedata2.replace('{{projection}}', p)
            newControlFile = os.path.join(os.path.dirname(controlFileTemplate), '{}_{}.ctl'.format(p, s))
            with open(newControlFile, 'w') as file:
                file.write(filedata2)
                

def scratch(modelDir, models, RCPs):
    dirs=[]
    txtfile = os.path.join(modelDir, 'model', 'output', 'scratch_directories_made.txt')
    for m in models:
        for r in RCPs:
                new_dir =  os.path.join(modelDir, 'model', 'output', 'scratch_{}_{}'.format(m,r))
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                dirs.append(new_dir)
    if not os.path.exists(txtfile):
        with open(txtfile, 'w') as file:
            for row in dirs:
                file.write(str(row) + '\n')
              
def run_swb(modelDir, control_file, output_subdir=None):
    import os 
    print(control_file)
    #output_subdir = os.path.basename(control_file)[:-4]
    prefix = os.path.basename(control_file)[:-4] + '_'
    output_dir = os.path.join(modelDir, 'model', 'output')
    if output_subdir:
        output_dir = os.path.join(output_dir,'scratch_'+output_subdir)
    lookup_dir =  os.path.join(modelDir, 'model', 'std_input')
    weather_data_dir = os.path.join(modelDir, 'model', 'input', 'climate')
    data_dir = os.path.join(modelDir, 'model', 'input')

    cmd = 'swb2 "{control_file}" --output_prefix="{output_prefix}" --output_dir="{output_dir}" --data_dir="{data_dir}" --lookup_dir="{lookup_dir}" --weather_data_dir="{weather_data_dir}"'.format(
        control_file = control_file, output_prefix = prefix, output_dir = output_dir, data_dir=data_dir, lookup_dir=lookup_dir, weather_data_dir = weather_data_dir) 
    print(cmd)
    os.system(cmd)
    

def SWB_daily_to_annual(infile, outfile, variables):
    for variable in variables:
     infile2 = infile.replace('net_infiltration', variable)
     outfile2 = outfile.replace('net_infiltration', variable)
     data = xr.open_dataset(infile2)
     data_sum = data[variable].resample(time = "1AS", restore_coord_dims=True).sum(dim='time')
     data_sum.to_netcdf(outfile2)

def SWB_daily_to_monthly(infile, outfile, variables):
    for variable in variables:
     infile2 = infile.replace('net_infiltration', variable)
     outfile2 = outfile.replace('net_infiltration', variable)
     data = xr.open_dataset(infile2)
     data_sum = data[variable].resample(time = "1MS", restore_coord_dims=True).mean(dim='time')
     data_sum.to_netcdf(outfile2)


def deleteDaily(modelDir, mod, txt):
    output_dir = os.path.join(modelDir, 'model', 'output', 'scratch_'+mod)
    shutil.rmtree(output_dir, ignore_errors=True)
    with open(txt, 'w') as f:
        f.write(output_dir)
        f.write('deleted')

def EnsembleMedian(outfile, models, variables):
    for ts in ['YEARLY', 'MONTHLY']:
        for variable in variables:
            outfile1=outfile.replace('net_infiltration', variable)
            outfile2=outfile1.replace('YEARLY', ts)
            if ts =='MONTHLY':
            	outfile2=outfile2.replace('SUM', 'MEAN')
            print(outfile2)
            paths = outfile2.replace('EnsembleMedian', '*')
            print(paths)
            ds = xr.open_mfdataset(paths, concat_dim='ensemble', combine='nested', decode_times=True)
            ds_median = ds.median(dim='ensemble')
            ds_median.to_netcdf(outfile2)



#outfile = r"C:\Users\mholland\OneDrive - DOI\Projects\MV\SWB\MV_SWB_Phase1/model/output/EnsembleMedian_net_infiltration__1999-01-01_to_2001-12-31__768_by_1182_YEARLY_SUM.nc"
#models =  ['cnrm-cm5', 'csiro-mk3-6-0', 'gfdl-esm2g', 'mpi-esm-mr', 'mri-cgcm3']
#variables  = ['net_infiltration', 'actual_et', 'gross_precipitation', 'rejected_net_infiltration', 'interception', 'runon', 'runoff_outside']
#EnsembleMedian(outfile, models, variables)




def zonal_stats(datapath, zone_raster, data_nc, dataframe_path):
    zones = xr.open_rasterio(os.path.join(datapath, zone_raster))
    data = xr.open_dataset(os.path.join(datapath, data_nc))
    data_annual = data.net_infiltration.resample(time = "1AS", restore_coord_dims=True).sum(dim='time')
    data_annual_mean = data_annual.mean(dim = 'time')
    zone_vals_df = xrs.zonal_stats(zones=zones[0], values=data_annual_mean)
    zone_vals_df.to_csv(dataframe_path)
    
def nse(predictions, targets):
    nash = (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))
    return nash


def LU_HSGcount(modelDir, LUfile, HSGfile):   
    
    studyarea  = gpd.read_file(r"georef\SIR2021_5116.shp")
    studyarea = studyarea.loc[studyarea['Area']=='active']

    fn=os.path.join(modelDir, "model", "output", HSGfile)
    ST = xr.open_dataset(fn)
    ST.rio.write_crs('+proj=aea +lat_0=23 +lon_0=-96 +lat_1=29.5 +lat_2=45.5 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs', inplace=True)
    ST = ST.rio.clip(studyarea.geometry.apply(mapping), studyarea.crs, drop=False)
    STarr = ST.band_data.values[0,:,:]
    STarr = np.nan_to_num(STarr, nan=0)

    fn=os.path.join(modelDir, "model", "output", LUfile)
    LC = xr.open_dataset(fn)
    LC.rio.write_crs('+proj=aea +lat_0=23 +lon_0=-96 +lat_1=29.5 +lat_2=45.5 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs', inplace=True)
    LCarr = LC.band_data.values[0,:,:]
    LCarr = np.where(LCarr == -9999, 0, LCarr)
    
    model_df=pd.DataFrame()
    model_df['HydrologicSoilNum']=STarr.ravel()
    model_df['LandUse']=LCarr.ravel()

    model_df=model_df.loc[model_df['HydrologicSoilNum']!=0]
    model_df=model_df.loc[model_df['LandUse']!=0]

    count=model_df.groupby(['HydrologicSoilNum', 'LandUse']).size().reset_index(name="count")
    count=count.sort_values(by='count', ascending=False).reset_index()
    count.to_csv(os.path.join(modelDir, 'model', 'std_input', 'cell_count.csv'))
    return count

def NewLookupTable(thisGrp, lookup_path, HydrologicSoilNum,LandUse,param, multipliers):
    for multiplier in multipliers:
        table = pd.read_csv(lookup_path, sep="\t")
        table = table.set_index('LU_Code')
        
        colnames = [param + '_' + str(int(HydrologicSoilNum)) ]
        rowinds = [int(LandUse)]
        for param_entry in zip(rowinds, colnames):
            new_parameter = table.loc[param_entry]*multiplier
            
            if param == 'CN' and new_parameter > 100:
                new_parameter = 100
                
            table.loc[param_entry] = new_parameter
        new_path = os.path.join(os.path.dirname(lookup_path),"lookup_{}_x{}.txt".format(thisGrp,str(multiplier)))
        table.to_csv(new_path, sep="\t")



def NewControlFile(modelDir, startDT, endDT, nx, ny, parameters, multipliers):
    for param in parameters:
        for multiplier in multipliers:
            controlFile = os.path.join(modelDir, 'model', 'control_file', 'SWB_CT_control.ctl')
            newControlFile = os.path.join(modelDir, 'model', 'control_file', 'SWB_CT_control_'+param+'_x' +str(multiplier)+'.ctl')
            newLookupTable = 'lookup_'+param+'_x' +str(multiplier)+'.txt'
    
            UpdateControlFile(controlFile,newControlFile,newLookupTable,startDT,endDT,nx, ny)

              

def runSWB_calibration(modelDir, parameter, multiplier):
    import os 
    output_prefix = parameter+'_x' +str(multiplier)+'_'
    output_dir = os.path.join(modelDir, 'model', 'output', 'daily')
    lookup_dir =  os.path.join(modelDir, 'model', 'std_input')
    weather_data_dir = os.path.join(modelDir, 'model', 'input', 'daymet')
    data_dir = os.path.join(modelDir, 'model', 'input')
    control_file = os.path.join(modelDir, 'model', 'control_file', 'SWB_CT_control_' + parameter + '_x' +str(multiplier))+'.ctl'
    
    cmd = 'swb2 "{control_file}" --output_prefix="{output_prefix}" --output_dir="{output_dir}" --data_dir="{data_dir}" --lookup_dir="{lookup_dir}" --weather_data_dir="{weather_data_dir}"'.format(
        control_file = control_file, output_prefix = output_prefix, output_dir = output_dir, data_dir=data_dir, lookup_dir=lookup_dir, weather_data_dir = weather_data_dir) 
    os.system(cmd)
    
    
    
def swbstat(outDir, prefix, file):
     import os
     exe = "swbstats2" 
     cmd= '{exe} --output_prefix="{prefix}" --annual_statistics "{f}" >>"{outFile}"'.format(
         exe=exe, prefix=os.path.join(outDir, prefix), f=os.path.join(outDir, 'annual', file),outFile = os.path.join(outDir,"output.txt"))
     print(cmd)
     os.system(cmd)      
     # cmd= '{exe} --output_prefix="{prefix}" --monthly_statistics "{f}" >>output.txt'.format(
         # exe=exe, prefix=os.path.join(outDir, prefix), f=os.path.join(outDir, file))
     # os.system(cmd)
    
  
    
def CompareErrors(errorFileList, lookupFileList,newErrorFile,newLookupTable):
    #read in the error files
    errors = []
    for thisFile in errorFileList:
        with open(thisFile) as f:
            errors.append(float(f.readline()))
    print(errors)
    #get the minimum error run
    min_error_index = np.argmin(errors)
    
    #copy the error and lookup tables for the minimum error run
    shutil.copy2(errorFileList[min_error_index],newErrorFile)
    shutil.copy2(lookupFileList[min_error_index],newLookupTable)
    
def compileAllErrors(frequent_groups,ErrorFiles,outFile):
    resultsDF = pd.DataFrame({'grpid':"base",'HydrologicSoilNum':0, 'LandUse':0}, index=[0])
    resultsDF = pd.concat([resultsDF.reset_index(),frequent_groups[['grpid','HydrologicSoilNum','LandUse']]],ignore_index=True).reset_index()
    resultsDF['Error']=np.nan
    
    #get the base error
    with open(ErrorFiles[0]) as f:
        resultsDF.loc[resultsDF.grpid=="base",'Error']=float(f.readline())
    
    #get the errors for the other groups
    for thisFile in ErrorFiles[1:]:
        thisGrp = os.path.basename(thisFile).split("_")[0]
        with open(thisFile) as f:
            resultsDF.loc[resultsDF.grpid==thisGrp,'Error']=float(f.readline())
    resultsDF.to_csv(outFile)
    
    
