# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 08:54:42 2022

@author: mholland
"""
from Python.SWBUtilities import run_swb, SWB_daily_to_annual
import os 

output_prefix = ''
modelDir  = 'MV_SWB_Phase1'
control_file = os.path.join(modelDir, 'SWB_MV.ctl')
run_swb(modelDir = modelDir, output_subdir = [], prefix = output_prefix, control_file = control_file)

SWB_daily_to_annual(datapath = os.path.join(modelDir, 'model', 'output', 'daily'), recharge_nc='MVnet_infiltration__1980-01-01_to_1981-12-31__384_by_591.nc')
		
		

