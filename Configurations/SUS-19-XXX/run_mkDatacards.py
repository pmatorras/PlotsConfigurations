#!/usr/bin/env python

import sys
import os

if len(sys.argv)<4:
    print 'Please, specify year, tag and sigset values!'
    sys.exit()

if sys.argv[1]=='-1':
    yearset='2016-2017-2018'
elif sys.argv[1]=='0':
    yearset='2016'
elif sys.argv[1]=='1':
    yearset='2017'
elif sys.argv[1]=='2':
    yearset='2018'
else:
    yearset=sys.argv[1]

tag=sys.argv[2]

sigset=sys.argv[3]

if len(sys.argv)==5:
    fileset=sys.argv[4]
else:
    fileset=sigset
if 'SM-' not in fileset:
    fileset = 'SM-' + fileset

exec(open('./signalMassPoints.py').read())

years = yearset.split('-')

for year in years:
    
    os.system('mkdir -p ./Datacards/'+year)

    for model in signalMassPoints:
        if model in sigset:
            for massPoint in signalMassPoints[model]:
                if massPointInSignalSet(massPoint, sigset):
                      
                    os.system('mkDatacards.py --pycfg=configuration.py --tag='+year+tag+' --sigset=SM-'+massPoint+' --outputDirDatacard=./Datacards/'+year+'/'+massPoint+' --inputFile=./Shapes/'+year+'/plots_'+tag+'_'+fileset+'.root') 