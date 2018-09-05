#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Tools for NetCDF files
Created on Wed Jun 27 16:08:26 2018

@author: Anthony Schrapffer
"""

from module_forc import *
from netCDF4 import Dataset as NetCDFFile
from netCDF4 import num2date
from netCDF4 import date2num
import datetime 


def nc_dis(outdir, datos, stname, units, name, varname):
    # Create File
    #outdir = "/home/anthony/Documents/temp/GestionNetCDF/test2.nc"
    foo = NetCDFFile(outdir, 'w')

    # Create dimensions
    dimt = 1428
    dims = 1
    foo.createDimension('time', dimt)
    foo.createDimension("stn", dims)

    # Variable time
    newvar = foo.createVariable("time", "double", ("time"), zlib = True)
    newvar.setncattr("standard_name", "time")
    newvar.setncattr("axis", "T")
    newvar.setncattr("long_name", "Time axis")
    newvar.setncattr("calendar", "gregorian")
    newvar.setncattr("units", "seconds since 1900-01-01 00:00:00")
    newvar.setncattr("time_origin", "1900-01-01 00:00:00")

    Ld=[]
    Ln = []
    i=0
    while i<1428:
        y = i/12
        m = i-y*12+1
        d = datetime.datetime(i/12+1900,m,1)
        Ld.append(d)
        Ln.append(date2num(d,"seconds since 1900-01-01 00:00:00", calendar = "gregorian"))
        i=i+1

    newvar[:] = Ln[:]


    # Variable hydro
    newvar = foo.createVariable(varname, "float", ("time", "stn"), zlib=True)
    newvar.setncattr("standard_name", name)
    newvar.setncattr("units", units)
    newvar.setncattr("long_name", "Discharge for "+stname)
    newvar.setncattr("coordinates", "time_centered")
    newvar[:,0] = datos[:]
    #Ajout valores obtenidos

    
    foo.sync()
    foo.close()
