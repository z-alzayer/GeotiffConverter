# GeoTIFF XML Header Cleaner

A simple Python utility that converts ESA SNAP-generated GeoTIFFs to standard GeoTIFF format by removing the special XML header metadata and rewriting them in the description instead as expected by rasterio or gdal.

## Problem
ESA SNAP software outputs GeoTIFF files with additional XML header metadata that can cause compatibility issues with some GIS software. This package provides a simple solution to convert these files into standard GeoTIFF format.

## Installation
 git clone 
 pip install GeotiffConverter 



## Features
- Removes ESA SNAP-specific XML headers
- Preserves essential geospatial metadata
- Maintains data integrity
- Simple and lightweight implementation

## Requirements
- Python >= 3.6
- rasterio
- xml.etree.ElementTree (built-in)
- If you have rasterio working it should just work

## Usage 

from GeotiffConverter import Converter

Converter.write_band_descriptions(img_path, output_path)

## Note

I've only tested this for Sentinel-2 Geotiffs from SNAP, as you'll see from the code it will only output whatever the original Geotiff had there are currently no plans to extend/customise this
