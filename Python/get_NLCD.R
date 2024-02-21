#################
#Download SWB gridded input data
#Author: Madeleine Holland
#Date: 5/25/2022


library(sf)
library(FedData)
library(raster)
library(soilDB)
library(terra)
library(rgeos)
library(rgdal)

setwd("C:/Users/mholland/OneDrive - DOI/Projects/MV")
#r1<-raster("C:\\Users\\mholland\\OneDrive - DOI\\Projects\\MV\\GIS\\grid\\grid\\grid\\grid.asc")
r=raster(xmn=1542200, xmx=1660400, ymn= 104600, ymx=181400, res=100)
values(r)=1
projection(r)=project_crs
proj4string(NLCD)
project_crs="+proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001016 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs +type=crs"
NLCD<-get_nlcd(template=r, label='nlcd19', year=2019, force.redo=T, dataset = 'landcover')
canopy <-get_nlcd(template=r, label='nlcd19', year=2016, force.redo=T, dataset = 'canopy', raster.options=c("NAflag=0"))

NLCD_proj = projectRaster(from = NLCD,  to = r, method = 'ngb')
canopy_proj = projectRaster(from = canopy,  to = r, method = 'ngb')

writeRaster(NLCD_proj, filename=file.path('SWB', 'MV_SWB_Phase1', 'model','input', "nlcd19.asc"), format="ascii",overwrite=TRUE, datatype = 'INT2S', NAflag = -9999)
writeRaster(canopy_proj, filename=file.path('SWB', 'MV_SWB_Phase1', 'model','input', "canopy16.asc"), format="ascii",overwrite=TRUE, datatype = 'INT2S', NAflag = 0)


NLCD<-get_nlcd(template=r, label='nlcd19', year=2019, force.redo=T, dataset = 'landcover')



pr<-stack("C:\\Users\\mholland\\OneDrive - DOI\\Projects\\SACO_SWB\\model\\input\\climate\\pr_csiro-mk3-6-01_RCP85.nc")
pr

# create a raster with proper resolution and extent
modelDir <- 'MV_SWB_Phase1'
extent_shp <- "MV200grid83ft"
output_name <- "nlcd19.asc"

r<-raster("C:\\Users\\mholland\\OneDrive - DOI\\Projects\\MV\\GIS\\grid\\grid\\grid\\grid.asc")
aoi <- readOGR(dsn = file.path('GIS', 'grid', 'grid'), layer = extent_shp)


project_crs="+proj=aea +lat_0=23 +lon_0=-96 +lat_1=29.5 +lat_2=45.5 +x_0=0 +y_0=0 +datum=NAD83 +ellps=GRS80 +units=m +no_defs"

aoi_rast <- raster(extent(aoi), res=152.4003048006096, crs=project_crs)
buff_rast <- raster(extent(aoi_buff), res=152.4003048006096, crs=project_crs)


#pull NLCD data and write out as asc
NLCD<-get_nlcd(template=r, label='nlcd19_lis', year=2019, force.redo=T, dataset = 'landcover')
impervious<-get_nlcd(template=buff_rast, label='nlcd19_lis', year=2019, force.redo=T, dataset = 'impervious')


NLCD_mask <- raster::mask(NLCD, aoi[,2])
plot(NLCD_mask[[1]])
writeRaster(NLCD, filename=file.path(modelDir, 'model','input', "nlcd19_lis.asc"), format="ascii",overwrite=TRUE, datatype = 'INT2S', NAflag = -9999,)
impervious_mask <-  raster::mask(impervious, aoi[2,])
plot(impervious_mask)', '
writeRaster(impervious_mask, filename=file.path(modelDir, 'ancillary', 'LandUse', "nlcd19_impervious_lis.asc"), format="ascii",  overwrite=TRUE)


proj4string(NLCD_mask)


#clip D8 flow direction and write out as ascii
file="C:/Users/mholland/OneDrive - DOI/Projects/LIS_SWB/RAW/NED/NEDFlowDirectionD8_NE.tif"
D8<-raster(file)
D8_crop<-crop(D8, extent(buff_rast))
writeRaster(D8_crop, filename=file.path(modelDir, 'model', 'input', "NED_30m_D8.asc"), format="ascii",overwrite=TRUE)


#split area of interest into grids < 5000 pixels x 5000 pixels
r<-buff_rast
lim <- 800
aoi1=crop(r, extent(r, 1, lim, 1, lim))
aoi2=crop(r, extent(r, lim+1, nrow(r), 1, lim))
aoi3=crop(r, extent(r, 1, lim, lim+1, ncol(r)))
aoi4=crop(r, extent(r, lim+1, nrow(r), lim+1, ncol(r)))

x1 <- mukey.wcs(aoi = aoi1, db = 'gssurgo')
x2 <- mukey.wcs(aoi = aoi2, db = 'gssurgo')
x3 <- mukey.wcs(aoi = aoi3, db = 'gssurgo')
x4 <- mukey.wcs(aoi = aoi4, db = 'gssurgo')
xall<-merge(x1,x2,x3,x4)
output_name <- "gssurgoMUKEY_lis.asc"
writeRaster(xall, filename=file.path(modelDir, 'ancillary', output_name), format="ascii", overwrite=TRUE)


#convert raster to terra raster to work with categorical data
x <- rast(xall)
#get hydrologic soil group keys using soilDB package
MUKEY <- unique(values(x))

hydgrp <- setNames(
  get_SDA_property(
    "hydgrp",
    "Dominant Condition",
    mukeys = MUKEY
  )[, c("mukey", "hydgrp")],
  c("ID",  "hydgrp")
)


#make raster of hydrologic soil groups (integers 1-4 represent soil groups A, B, C, and D)
#levels(x) <- hydgrp
#_hdr <- catalyze(x)
#output_name <- "hydgrp_lis.asc"
#terra::writeRaster(r_hdr, filename=file.path(modelDir, 'model', 'input', output_name), NAflag = -9999, format="AAIGrid", overwrite=TRUE)


#get available soil water content keys using soilDB package
awc <- setNames(
  get_SDA_property(
   property="awc_r",
    method="Weighted Average",
    top_depth=0, 
    bottom_depth=100,
    mukeys = MUKEY
  )[, c("mukey", "awc_r")],
  c("ID",  "awc_r")
)


df=merge(awc,hydgrp)
write.csv(df, file=file.path(modelDir, 'ancillary', "gssurgoKey.csv"))
