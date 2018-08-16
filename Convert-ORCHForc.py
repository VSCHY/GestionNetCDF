#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 16:08:26 2018

@author: anthony
"""

from module_forc import *
from netCDF4 import Dataset as NetCDFFile
from netCDF4 import num2date

# Add variable
def addvariable(indir, datan, i, j, foo):
    """
    Add a variable datan from indir between time i-j in foo (already opened)
    """
    # Variable Environment
    odata = get_var(indir, datan, 0)
    newdata = foo.createVariable(datan, odata.dtype, ("time", 'lat', 'lon'))
    for attrn in odata.ncattrs():
        attrv = getattr(odata, attrn)
        newdata.setncattr(attrn, attrv)
    data = conv_var(indir, datan, i,j)
    newdata[:,:,:] = data[:,:,:]
    return newdata

# Conversion via Fortran
def conv_var(indir, varn, i,j):
    """
    Convert variable varn from indir between timestep i and j from land - lon/lat
    """
    ncfile = NetCDFFile(indir, 'r')
    dimx, dimy, dimland = get_dim(indir)
    dimt = j-i
    T = ncfile.variables[varn][i:j,:]
    land = ncfile.variables["land"][:]
    T2 = module_forc.land(dimx=dimx, dimy=dimy, dimt=dimt, dimland=dimland, landloc=land, oldvar=T)
    return T2

def get_dim(indir):
    """
    Get the dimension of x, y and land
    """
    # dimx, dimy, dimt, dimland
    ncfile = NetCDFFile(indir, 'r')
    dimx = len(ncfile.variables["nav_lon"][0,:])
    dimy = len(ncfile.variables["nav_lon"][:,0])
    dimland = len(ncfile.variables["land"][:])
    return dimx, dimy, dimland

def get_var(chem_file, varname, dim):
    """
    Get variable -varname- of dimension -dim- from file -chem_file-.
    """
    salid = NetCDFFile(chem_file, 'r')
    if dim == 0:
        var = salid.variables[varname]
    if dim == 1:
        var = salid.variables[varname][:]
    if dim == 2:
        var = salid.variables[varname][:,:]
    if dim == 3:
        var = salid.variables[varname][:,:,:]
    if dim == 4:
        var = salid.variables[varname][:,:,:,:]
    return var

def CreatNetCDF_convert(outdir, indir, datan, i, j):
    """
    Create NetCDF from converting file -indir- to -outdir-
    getting variable -datan- between timestep i and j (python index)
    """
    
    dimt = j-i
    dimx, dimy, dimland = get_dim(indir)    
    # Create the file
    foo = NetCDFFile(outdir, 'w')
    print dimx
    print dimy
    print dimt
    
    # Creation dimensions
    foo.createDimension("lon", dimx)
    foo.createDimension("lat", dimy)
    foo.createDimension('time', dimt)

    # Environment variables

    # lon
    ovar = get_var(indir, "nav_lon", 0)
    newvar = foo.createVariable("lon", ovar.dtype, ("lon"))
    newvar[:] = ovar[0,:]
    newvar.setncattr("standard_name", "longitude")
    newvar.setncattr("long_name", "Longitude")
    newvar.setncattr("units", "degrees_east")
    newvar.setncattr("CoordinateAxisType", "Lon")
    
    # lat
    ovar = get_var(indir, "nav_lat", 0)
    newvar = foo.createVariable("lat", ovar.dtype, ("lat"))
    newvar[:] = ovar[:,0]
    newvar.setncattr("standard_name", "latitude")
    newvar.setncattr("long_name", "Latitude")
    newvar.setncattr("units", "degrees_north")
    newvar.setncattr("CoordinateAxisType", "Lat")
        
    # time
    ovar = get_var(indir, "time", 0)
    newvar = foo.createVariable("time", ovar.dtype, ("time"))
    newvar[:] = ovar[i:j]
    for attrn in ovar.ncattrs():          
        attrv = getattr(ovar, attrn)
        newvar.setncattr(attrn, attrv)

    addvariable(indir, datan, i, j, foo)
    
    foo.sync()
    foo.close()



###################################################
###################################################
#################### MAIN #########################
###################################################
###################################################

indir = "/home/anthony/Documents/Doctorat/MODELADO/TP/FINAL/output/CRUNCEP/cruncep_halfdeg_2002.nc"
outdir = "/home/anthony/Documents/temp/GestionNetCDF/test.nc"
datan = "Tair"

ncin = NetCDFFile(indir, 'r')
# Get i, j
time = ncin.variables["time"]
dtime = num2date(time[:], time.units)
i=0
j=len(time)
# Pour faire entre i et j / pour avoir juste un mois
# Possibilite faire par mois et reunir apres
"""
for i in range(0, len(dtime)):
    if dtime[i].month == 4:
        break

for j in range(i, len(dtime)):
    if dtime[j].month == 5:
        break
"""
ncin.close()


CreatNetCDF_convert(outdir, indir, datan, i, j)

### Pour ajouter autre au meme fichier : reouvrir et utiliser addvariables
# Sinon pour faire un autre fichier : 
"""
outdir = "/home/anthony/Documents/Doctorat/MODELADO/TP/FINAL/output/CRUNCEP/cruncep_halfdeg_rainf_042002.nc"
datan = "Rainf"
CreatNetCDF(outdir, indir, datan, i, j)
"""
