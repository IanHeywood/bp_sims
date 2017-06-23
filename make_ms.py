import numpy
import pylab
import pickle
from obsparams import *
c = 299792458.0 # speed of light

# def getAntennaPositions(myarray):
# 	if myarray == 'askap':
# 		xx,yy,zz,dishDiameter = pickle.load(open('askap_antennas.p','rb'))
# 		nDishes = len(xx)
# 		coordsys = 'local'
# 		dishDiameters = numpy.zeros((nDishes,), numpy.float64) + dishDiameter
# 		dishDiameters = dishDiameters.tolist()
# 	elif myarray == 'meerkat':
# 		xx,yy,zz,dishDiameter = pickle.load(open('meerkat_antennas.p','rb'))	
# 		nDishes = len(xx)
# 		coordsys = 'local'
# 		dishDiameters = numpy.zeros((nDishes,), numpy.float64) + dishDiameter
# 		dishDiameters = dishDiameters.tolist()	
# 	elif myarray == 'ska':
# 		xx,yy,zz,dishDiameters = pickle.load(open('ska_antennas.p','rb'))	
# 		coordsys = 'global'	
# 	return xx,yy,zz,dishDiameters,coordsys
	
def sim_ms(prefix,myarray,minFreq,nChan,chanWidth,startTime,scanLength,xx,yy,zz,dishDiameters,coordsys):
	projectName = prefix+'_'+myarray+'_'+minFreq+'_'+str(nChan)+'ch_'+chanWidth+'_'+str(int(scanLength/60.0))+'min'
	RA_central = '19h39m25.027s' 
	Dec_central = '-63d42m45.63s'
	Stokes = 'XX XY YX YY'
	integrationTime = '120s'
	refTime = me.epoch('IAT','2018/01/01')
	elevationLimit = '8.0deg'
	shadowLimit = 0.001
	#xx,yy,zz,dishDiameters,coordsys = getAntennaPositions(myarray)
	# nDishes = len(xx)
	# dishDiameters = numpy.zeros((nDishes,), numpy.float64) + dishDiameter
	# dishDiameters = dishDiameters.tolist()
	clName = projectName+'.cl'
	msName = projectName+'.ms'
	refRA = qa.unit(RA_central)
	refDec = qa.unit(Dec_central)
	direction = me.direction(rf = 'J2000', v0 = refRA, v1 = refDec)
	cl.addcomponent(dir = direction, flux = 1.0, freq = minFreq)
	cl.rename(filename = clName)
	cl.done()
	sm.open(msName)
	sm.setspwindow(spwname = prefix,
		freq = minFreq,
		deltafreq = chanWidth,
		freqresolution = chanWidth,
		nchannels = nChan,
		stokes = Stokes)
	if myarray == 'askap':
		obsPosition = me.observatory('ATCA')
	else:
		obsPosition = me.observatory('MeerKAT')
	sm.setconfig(telescopename = myarray,
		x = xx,
		y = yy,
		z = zz,
		dishdiameter = dishDiameters,
		mount = 'ALT-AZ',
		coordsystem = coordsys,
		referencelocation = obsPosition)
	sm.setfeed(mode = 'perfect X Y')
	sm.setfield(sourcename = prefix,
		sourcedirection = me.direction(rf = 'J2000', v0 = refRA, v1 = refDec))
	sm.settimes(integrationtime = integrationTime,
		usehourangle = True,
		referencetime = refTime)
	sm.setlimits(shadowlimit = shadowLimit,
		elevationlimit = elevationLimit)
	sm.setauto(autocorrwt = 0.0)
	scan = 0
	endTime = startTime + scanLength
	while (startTime < endTime):
		sm.observe(prefix, prefix, starttime = str(startTime)+'s', stoptime = str(startTime + scanLength)+'s')
		me.doframe(refTime)
		me.doframe(obsPosition)
		hadec = me.direction('hadec', qa.time(str(startTime + scanLength / 2)+'s'), refDec)
		azel = me.measure(hadec,'azel')
		sm.setdata(msselect = 'SCAN_NUMBER==' + str(scan))
		sm.predict(complist = clName)
		startTime = startTime + scanLength
		scan += 1
	sm.done()
	os.system('rm -rf ' + clName)

	setjy(vis=msName,standard='Perley-Butler 2010',usescratch=True)

	return msName

sim_ms(prefix,myarray,minFreq,nChan,chanWidth,startTime,scanLength,xx,yy,zz,dishDiameters,coordsys)
