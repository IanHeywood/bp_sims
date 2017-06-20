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

for myfreq in ['0.7GHz','0.8GHz','0.9GHz','1.0GHz','1.1GHz','1.2GHz','1.3GHz','1.4GHz','1.5GHz','1.6GHz','1.7GHz']:
	for caltime in [300,600,900]:
		mystart = -1*caltime/2
		write_obsparams('bpsims',
			'askap',
			myfreq,
			1024,
			'20kHz',
			mystart,
			caltime)
		print ''
		os.system('more obsparams.py')
