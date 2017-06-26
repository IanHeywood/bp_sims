# PKS B1934-638 bandpass simulations

import numpy
import pickle
import Pyxis
import ms
import mqt
import os

do_steps = [0,1,2,3]
delete_ms = True
solnorm = False
mqt.MULTITHREAD = 8
ref_ant = '0'

def pokeTDLconf(filename,param,value):
	lines = []
	f = open(filename,'r')
	line = f.readline()
	while line:
		lines.append(line.rstrip('\n'))
		line = f.readline()
	f.close()
	f = open(filename,'w')
	for line in lines:
		parts = line.replace(' ','').split('=')
		if parts[0] == param:
			print >>f,parts[0]+' = '+value
		else:
			print >>f,line
	f.close()

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

# Stick a write_obsparams call in here to run in one-shot mode, otherwise use looper.py
	
# step = 0 
# Read in obsparams file
if 0 in do_steps:
	from obsparams import *

# step = 1
# Execute make_ms.py CASA script (also reads in obsparams)
# End product is a MS with 1934-638 model in MODEL_DATA
if 1 in do_steps:
	os.system('casa -c make_ms.py --nologger --log2term --nogui')

# step = 2
# Use MeqTrees to add field source visibilities to MODEL_DATA
# Write result to DATA
if 2 in do_steps:
	tdl_sizes = str(dishDiameters).replace('[','').replace(']','').replace(',',' ')
	pokeTDLconf('tdlconf.profiles','analytic_beams.wsrt_cos3_beam.dish_sizes',tdl_sizes)
	mqt.run('turbo-sim.py',
	job='simulate',
	config='tdlconf.profiles',
	section='bp_sims',
	args=['ms_sel.msname='+msName,
		'tiggerlsm.filename=PKS_B1934-638_ATCA_BETA.lsm.html',
		'ms_sel.tile_size=512'])

# step = 3
# Generate a bandpass table deriving corrections for DATA against MODEL_DATA 
if 3 in do_steps:
	cc = 'bandpass('
	cc+= 'vis="'+msName+'",'
	cc+= 'caltable="'+bpTable+'",'
	cc+= 'solnorm='+str(solnorm)+','
	cc+= 'solint="inf",'
	cc+= 'refant="'+ref_ant+'")'
	std.runcasapy(cc)

if delete_ms:
	os.system('rm -rf '+msName)
