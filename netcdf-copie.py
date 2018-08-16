import numpy as np
from netCDF4 import Dataset as NetCDFFile

file1=''
ofile=''



def searchInlist(listname, nameFind):
    """ Function to search a value within a list
    listname = list
    nameFind = value to find
    >>> searInlist(['1', '2', '3', '5'], '5')
    True
    """
    for x in listname:
      if x == nameFind:
        return True
    return False


onew = NetCDFFile(ofile, 'w')
onc1 = NetCDFFile(file1, 'r')

for dimn in onc1.dimensions:
    if not searchInlist(onew.dimensions,dimn):
        odim = onc1.dimensions[dimn]
        if odim.isunlimited():
            onew.createDimension(dimn, None)
        else:
            onew.createDimension(dimn, len(odim))
for varn in onc1.variables:
    print varn + " ...."
    if not searchInlist(onew.variables,varn):
        ovar = onc1.variables[varn]
        newvar = onew.createVariable(varn, ovar.dtype, ovar.dimensions)
        if np.prod(ovar.shape) > 300*300*100:
            for it in range(0,ovar.shape[0], 5):
                 print "  ", iit, ',', eit
                 iit = it
                 eit = it + 5
                 newvar[iit:eit,] = ovar[iit:eit,]
            if eit != ovar.shape[0]:
                 print "  ", iit, ',', eit
                 iit = eit
                 eit = ovar.shape[0]
                 newvar[iit:eit,] = ovar[iit:eit,]
        else:
            newvar[:] = ovar[:]
        for attrn in ovar.ncattrs():
            attrv = ovar.getncattr(attrn)
            newvar.setncattr(attrn,attrv)
        onew.sync()

# global attr
for attrn in onc1.ncattrs():
    attrv = onc1.getncattr(attrn)
    onew.setncattr(attrn,attrv)
onew.sync()
onc1.close()
onew.close()
