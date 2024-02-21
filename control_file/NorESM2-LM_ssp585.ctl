%% Martha's Vineyard
%% Net infiltration to groundwater system

%%'swb2 "{control_file}" --output_prefix="{output_prefix}" --output_dir="{output_dir}" --data_dir="{data_dir}" --lookup_dir="{lookup_dir}" --weather_data_dir="{weather_data_dir}"'.format(
%% output_prefix = 'MV', output_dir = 'MV_LIS_Phase1/model/output', lookup_dir = 'MV_LIS_Phase1/model/std_input', weather_data_dir = 'MV_LIS_Phase1/model/input/cliamte', data_dir = 'MV_SWB_Phase1/model/input'


! Grid definition: NAD83(2011) / Massachusetts Island (ftUS) 
!      nx    ny     xll          yll         resolution

GRID 1182 768 1542200 104600 100

BASE_PROJECTION_DEFINITION +proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs


%% Define methods
-----------------
SOIL_MOISTURE_METHOD            THORNTHWAITE-MATHER
RUNOFF_METHOD                   C-N DOWNHILL-ROUTING
EVAPOTRANSPIRATION_METHOD       HARGREAVES-SAMANI
INTERCEPTION_METHOD 		BUCKET
FOG_METHOD 			NONE
FLOW_ROUTING_METHOD 		NONE
IRRIGATION_METHOD 		NONE
ROOTING_DEPTH_METHOD		STATIC
CROP_COEFFICIENT_METHOD 	NONE
DIRECT_RECHARGE_METHOD 		NONE
SOIL_STORAGE_MAX_METHOD 	CALCULATED 
AVAILABLE_WATER_CONTENT_METHOD 	GRIDDED
#INITIAL_ABSTRACTION_METHOD	TR55 		#Ia = 0.2S 
INITIAL_ABSTRACTION_METHOD 	HAWKINS		#Ia = 0.05S; overall effect is to increase runoff for smaller precipitation events, this method has been suggested to be more appropriate for long-term simulation
 
%% define location, projection, and conversions for weather data
----------------------------------------------------------------
TMAX NETCDF CMIP6/tasmax.NorESM2-LM.ssp585.2015-2100.LOCA_16thdeg_Celcius_Final.nc
TMAX_GRID_PROJECTION_DEFINITION +proj=longlat +datum=WGS84 +no_defs
TMAX_SCALE_FACTOR                 1.8
TMAX_ADD_OFFSET                  32.0
TMAX_MISSING_VALUES_CODE      -9999.0
TMAX_MISSING_VALUES_OPERATOR      <=
TMAX_MISSING_VALUES_ACTION       mean
TMAX_NETCDF_Z_VAR     	       tasmax
TMAX_NETCDF_X_VAR                 lon
TMAX_NETCDF_Y_VAR                 lat

TMIN NETCDF CMIP6/tasmin.NorESM2-LM.ssp585.2015-2100.LOCA_16thdeg_Celcius_Final.nc
TMIN_GRID_PROJECTION_DEFINITION +proj=longlat +datum=WGS84 +no_defs
TMIN_SCALE_FACTOR                 1.8
TMIN_ADD_OFFSET                  32.0
TMIN_MISSING_VALUES_CODE      -9999.0
TMIN_MISSING_VALUES_OPERATOR      <=
TMIN_MISSING_VALUES_ACTION       mean
TMIN_NETCDF_Z_VAR     	       tasmin
TMIN_NETCDF_X_VAR                 lon
TMIN_NETCDF_Y_VAR                 lat

PRECIPITATION NETCDF CMIP6/pr.NorESM2-LM.ssp585.2015-2100.LOCA_16thdeg_Final.nc
PRECIPITATION_GRID_PROJECTION_DEFINITION +proj=longlat +datum=WGS84 +no_defs
PRECIPITATION_SCALE_FACTOR          3401.5766399999998   #kg/m2 to inches
PRECIPITATION_MISSING_VALUES_CODE      -9999.0
PRECIPITATION_MISSING_VALUES_OPERATOR      <=
PRECIPITATION_MISSING_VALUES_ACTION       mean
PRECIPITATION_NETCDF_Z_VAR                pr
PRECIPITATION_NETCDF_X_VAR                 lon
PRECIPITATION_NETCDF_Y_VAR                 lat

OUTPUT_GRID_SUFFIX asc

# -- Alternative Initial Abstraction Term
# Has the effect of increasing runoff generation for areas 
# with low curve numbers and for smaller storms. Woodward
# and others (2003) suggest that this may be the more appropriate
# formulation for long-term simulations. The default method in
# swb is the classic formulation.
#INITIAL_ABSTRACTION_METHOD HAWKINS


INITIAL_CONTINUOUS_FROZEN_GROUND_INDEX CONSTANT 100.0
UPPER_LIMIT_CFGI 83.
LOWER_LIMIT_CFGI 55.

%% specify location and projection for input GIS grids
------------------------------------------------------

LAND_USE ARC_GRID nlcd19.asc
LANDUSE_PROJECTION_DEFINITION  +proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs

FLOW_DIRECTION ARC_GRID NED_30m_D8.asc
FLOW_DIRECTION_PROJECTION_DEFINITION  +proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs

HYDROLOGIC_SOILS_GROUP ARC_GRID hydsoilgrp.asc
HYDROLOGIC_SOILS_GROUP_PROJECTION_DEFINITION +proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs

AVAILABLE_WATER_CONTENT ARC_GRID awc.asc
AVAILABLE_WATER_CONTENT_PROJECTION_DEFINITION +proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs
AVAILABLE_WATER_CONTENT_SCALE_FACTOR         0.12   #cm/100cm to in/ft

%%IRRIGATION_MASK ARC_GRID 
%%IRRIGATION_MASK_PROJECTION_DEFINITION 



%% specify location and names for all lookup tables
---------------------------------------------------

LAND_USE_LOOKUP_TABLE MVLookup_NLCD.txt
#OPEN_WATER_LAND_USE 11

%% initial conditions for soil moisture and snow storage amounts
%% may be specified as grids, but using a constant amount and
%% allowing the model to "spin up" for a year is also acceptable.

INITIAL_PERCENT_SOIL_MOISTURE CONSTANT 75
INITIAL_SNOW_COVER_STORAGE CONSTANT 0


%%DUMP_VARIABLES COORDINATES 558059. 432426.
DUMP_VARIABLES 250 182

OUTPUT_OPTIONS NET_INFILTRATION BOTH BOTH BOTH
# OUTPUT_OPTIONS variable daily_output monthly_output annual_output

DISLIN PARAMETERS RECHARGE
SET_Z_AXIS_RANGE DAILY 0 1.5 0.1
SET_Z_AXIS_RANGE MONTHLY 0 7 1.0
SET_Z_AXIS RANGE ANNUAL 0 20 2 
SET_DEVICE PDF
SET_FONT Times-Bold
Z_AXIS_TITLE RECHARGE, IN IN.
%% start and end date may be any valid dates in SWB version 2.0
%% remember to allow for adequate model spin up; running the
%% model for just a month or two will give questionable results

START_DATE 01/01/2015
END_DATE 12/31/2100
