# PKS B1934-638 bandpass simulations

import numpy
import pickle
import os

def getAntennaPositions(myarray):
	if myarray == 'askap':
		xx,yy,zz,dishDiameter = pickle.load(open('askap_antennas.p','rb'))
		nDishes = len(xx)
		coordsys = 'local'
		dishDiameters = numpy.zeros((nDishes,), numpy.float64) + dishDiameter
		dishDiameters = dishDiameters.tolist()
	elif myarray == 'meerkat':
		xx,yy,zz,dishDiameter = pickle.load(open('meerkat_antennas.p','rb'))	
		nDishes = len(xx)
		coordsys = 'local'
		dishDiameters = numpy.zeros((nDishes,), numpy.float64) + dishDiameter
		dishDiameters = dishDiameters.tolist()	
	elif myarray == 'ska':
		xx,yy,zz,dishDiameters = pickle.load(open('ska_antennas.p','rb'))	
		coordsys = 'global'	
	return xx,yy,zz,dishDiameters,coordsys

def write_obsparams(prefix,
	myarray,
	minFreq,
	nChan,
	chanWidth,
	startTime,
	scanLength):
	myarray = myarray.lower()
	projectName = prefix+'_'+myarray+'_'+minFreq+'_'+str(nChan)+'ch_'+chanWidth+'_'+str(int(scanLength/60.0))+'min'
	msName = projectName+'.ms'
	bpTable = 'cal_'+msName+'.B'
	xx,yy,zz,dishDiameters,coordsys = getAntennaPositions(myarray)
	f = open('obsparams.py','w')
	print >>f,'prefix="'+str(prefix)+'"'
	print >>f,'myarray="'+str(myarray)+'"'
	print >>f,'minFreq="'+str(minFreq)+'"'
	print >>f,'nChan='+str(nChan)
	print >>f,'chanWidth="'+str(chanWidth)+'"'
	print >>f,'startTime='+str(startTime)
	print >>f,'scanLength='+str(scanLength)
	print >>f,'projectName="'+str(projectName)+'"'
	print >>f,'msName="'+str(msName)+'"'
	print >>f,'bpTable="'+str(bpTable)+'"'
	print >>f,'xx='+str(xx)
	print >>f,'yy='+str(yy)
	print >>f,'zz='+str(zz)
	print >>f,'dishDiameters='+str(dishDiameters)
	print >>f,'coordsys="'+str(coordsys)+'"'
	f.close()

# ASKAP
bandfreqs = ['0.7GHz', '0.74GHz', '0.78GHz', '0.82GHz', '0.86GHz', '0.9GHz', '0.94GHz', '0.98GHz', '1.02GHz', '1.06GHz', '1.1GHz', '1.14GHz', '1.18GHz', '1.22GHz', '1.26GHz', '1.3GHz', '1.34GHz', '1.38GHz', '1.42GHz', '1.46GHz', '1.5GHz', '1.54GHz', '1.58GHz', '1.62GHz', '1.66GHz', '1.7GHz', '1.74GHz', '1.78GHz', '1.82GHz']

# MeerKAT_L-band
# bandfreqs = ['0.9GHz', '0.94GHz', '0.98GHz', '1.02GHz', '1.06GHz', '1.1GHz', '1.14GHz', '1.18GHz', '1.22GHz', '1.26GHz', '1.3GHz', '1.34GHz', '1.38GHz', '1.42GHz', '1.46GHz', '1.5GHz', '1.54GHz', '1.58GHz', '1.62GHz', '1.66GHz', '1.7GHz']

# MeerKAT_UHF
# bandfreqs = ['0.58GHz', '0.62GHz', '0.66GHz', '0.7GHz', '0.74GHz', '0.78GHz', '0.82GHz', '0.86GHz', '0.9GHz', '0.94GHz', '0.98GHz', '1.02GHz']

# SKA-MID_Band-2
# bandsfreqs = ['0.95GHz', '0.99GHz', '1.03GHz', '1.07GHz', '1.11GHz', '1.15GHz', '1.19GHz', '1.23GHz', '1.27GHz', '1.31GHz', '1.35GHz', '1.39GHz', '1.43GHz', '1.47GHz', '1.51GHz', '1.55GHz', '1.59GHz', '1.63GHz', '1.67GHz', '1.71GHz', '1.75GHz', '1.79GHz']

# SKA-MID_Band-1
# bandfreqs = ['0.35GHz', '0.39GHz', '0.43GHz', '0.47GHz', '0.51GHz', '0.55GHz', '0.59GHz', '0.63GHz', '0.67GHz', '0.71GHz', '0.75GHz', '0.79GHz', '0.83GHz', '0.87GHz', '0.91GHz', '0.95GHz', '0.99GHz', '1.03GHz', '1.07GHz']

for myfreq in bandfreqs:
	for caltime in [300,600,900]:
		mystart = -1*caltime/2
		write_obsparams('bpsims',
			'askap',
			myfreq,
			2000,
			'20kHz',
			mystart,
			caltime)
		print ''
		os.system('python master.py')
