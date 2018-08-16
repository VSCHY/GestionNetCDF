FC 		= /opt/intel/composerxe-2011.3.174/bin/intel64/ifort
FCF 	= -c
LIB_INC = 
RM 		= /bin/rm 
F2PY 		= /usr/bin/f2py
NCLIBFOLD	= /home/anthony.schrapffer/bin/anaconda2/lib
NCINCFOLD	= /home/anthony.schrapffer/bin/anaconda2/include 
LIB_NETCDF	= -L$(NCLIBFOLD) -lnetcdff -lnetcdf -I$(NCINCFOLD)
FCFLAGS = $(FCF) $(DBGFLAGS)

# Sources for f2py
srcs = module_forc.f90

####### ###### ##### #### ### ## #

MODULES = \
	module_forc.o

FINTMODULES = \
	module_forc.o

all : \
        module_forc.o

clean :
	$(RM) *.mod *.o

#########################

module_forc.o:
	$(F2PY) -c -m module_forc module_forc.f90
