library(raster)
library(sf)
library(soilDB)
library(rgdal)
library(tidyverse)
library(FedData)

library(fasterize)
setwd("C:/Users/mholland/OneDrive - DOI/Projects/MarthasVineyard")
modelDir = 'MV_SWB_Phase1'
aoi<-raster('GIS\\grid\\grid\\grid\\grid.asc')

NLCD<-get_nlcd(template=aoi, label='nlcd19', year=2019, force.redo=T, dataset = 'landcover')
NLCD_proj<-projectRaster(from=NLCD,res=200, crs = crs(aoi), method='ngb')
writeRaster(NLCD_proj, filename=file.path('SWB', modelDir, 'model','input', "nlcd19.asc"),driver= 'ASCII', overwrite=TRUE, datatype = 'INT2S', NAflag = -9999)


#clip D8 flow direction and write out as ascii
file="C:/Users/mholland/OneDrive - DOI/Projects/LIS_SWB/RAW/NED/NEDFlowDirectionD8_NE.tif"
D8<-raster("GIS\\D8_MV.ovr")
D8_crop<-crop(D8, extent(aoi))


x <- mukey.wcs(aoi = aoi, db = 'gssurgo', res=60.96)
output_name <- "gssurgoMUKEY_lis.asc"
writeRaster(x, filename=file.path('GIS', 'Soil', output_name), overwrite=TRUE)


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
write.csv(df, file=file.path('AncillaryData', "gssurgoKey.csv"))
