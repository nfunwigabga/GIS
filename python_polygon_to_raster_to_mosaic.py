# This script takes multiple shapefiles in a directory, creates a raster based for each attribute of the shapefile (you can choose which attributes to create from), and then creates a mosaic of the rasters, one for each attribute.

# create raster files of the shapefiles before looking through to create mosaics
import arcpy, itertools, os, shutil
from arcpy import env
# create folder where output files will be saved initially
if not os.path.exists('s:/arcgisLoop/tifs'):
	os.makedirs('s:/arcgisLoop/tifs') # put the path where the initial output will be saved here
arcpy.env.workspace = r"s:\arcgisLoop" # direcroty of the shapefiles location
rasterOutputPath = r"s:/arcgisLoop/tifs/" 
shpFileList = arcpy.ListFiles("*.shp")
assignmentType = "MAXIMUM_AREA" # can be CELL_CENTER, MAXIMUM_AREA or MAXIMUM_COMBINED_AREA
attributeFields = ["PR", "PW"] # list the attributes that rasters will be created for. Must be the same for all layers
for shpFile in shpFileList:
	for attr in attributeFields:
		lyrName = shpFile.split(".")[0]
		outRaster = rasterOutputPath + attr + '_' + lyrName + ".tif"
 # this is the command to convert to raster. you can check the documentation online and change these parameters as necessary
		arcpy.PolygonToRaster_conversion(in_features=shpFile, value_field=attr, out_rasterdataset=outRaster, cell_assignment=assignmentType, cellsize=0.5)
# create mosaic of all the created rasters
# check of output directory exists and create it is not exists
if not os.path.exists('s:/arcgisLoop/final_mosaics'):
    os.makedirs('s:/arcgisLoop/final_mosaics')
arcpy.env.workspace = r'S:\arcgisLoop\tifs' # reset the workspace to the output tif files.
outws = r'S:\arcgisLoop\final_mosaics'
rasters = arcpy.ListRasters()
# group based on first two letters of the rasters, which is the attribute name
grouped = [list(g) for _, g in itertools.groupby(sorted(rasters), lambda x: x[:3])] 
for group in grouped:
    outname = group[0][:3] + "_mosaic.tif"
    # this is the command to create the mosaic rasters. you can check the documentation online and change these parameters as necessary
    arcpy.MosaicToNewRaster_management(group, outws, outname, pixel_type = "32_BIT_SIGNED", number_of_bands = 1, mosaic_method = "FIRST")
# cleanup by deleting the folder containing the individual tif files. remove this line if you want to keep the individual rasters
shutil.rmtree('s:/arcgisLoop/tifs')
print "-->>> FINAL OUTPUT FILES ARE LOCATED IN " + outws

