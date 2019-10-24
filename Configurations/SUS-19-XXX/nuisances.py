### nuisances

### general parameters
if '2016' in opt.tag : 
    year = '_2016'
    lumi_uncertainty = '1.025'
elif '2017' in opt.tag : 
    year = '_2017'
    lumi_uncertainty = '1.023'
elif '2018' in opt.tag : 
    year = '_2018'
    lumi_uncertainty = '1.025'

### nuisances = {}
 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'samples' : {}
             }

### lnN

# luminosity -> https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#TabLum

nuisances['lumi']  = {
               'name'  : 'lumi_13TeV'+year,
               'samples'  : { },
               'type'  : 'lnN',
}
for sample in samples.keys():
    if sample!='DATA' and sample!='ZZ'  and sample!='ttZ' and sample!='WZ'  and sample!='DY':
        nuisances['lumi']  ['samples'][sample] = lumi_uncertainty 

# trigger

nuisances['trigger']  = {
               'name'  : 'trigger'+year,
               'samples'  : { },
               'type'  : 'lnN',
}
for sample in samples.keys():
    if sample!='DATA' and sample!='ZZ'  and sample!='ttZ' and sample!='WZ'  and sample!='DY':
        nuisances['trigger']  ['samples'][sample] = '1.02'

# background cross sections and scale factors

normBackgrounds = {
    #'ttbar' : { 'all'   : { '1.10' : [ '_All' ]                    } }, # -> rate parameter
    'tW'    : { 'all'   : { '1.10' : [ '_All' ]                    } }, 
    #'WW'    : { 'all'   : { '1.10' : [ '_All' ]                    } }, # -> rate parameter
    'ttW'   : { 'all'   : { '1.50' : [ '_All' ]                    } },
    'VZ'    : { 'all'   : { '1.50' : [ '_All' ]                    } },
    'VVV'   : { 'all'   : { '1.50' : [ '_All' ]                    } },
    'WZ'    : { 'all'   : { '1.50' : [ '_All' ]                    } }, # 0.97 +/- 0.09
    'ttZ'   : { 'all'   : { '1.50' : [ '_All' ]                    } }, # 1.44 +/- 0.3
    'ZZ'    : { 'nojet' : { '1.26' : [ '_NoJet' ]                  },   # 0.74 +/- 0.19
                'jet'   : { '1.14' : [ '_NoTag', '_Tag' ]          },   # 1.21 +/- 0.17
                'veto'  : { '1.12' : [ '_Veto' ]                   } }, # 1.06 +/- 0.12
    'DY'    : { 'jet  ' : { '1.32' : [ '_Tag', '_Veto', '_NoTag' ] },
                'nojet' : { '2.00' : [ '_NoJet' ]                  } },
}

for background in normBackgrounds:
    for region in normBackgrounds[background]:
        nuisancename = 'norm'+background+region
        value, subregions = normBackgrounds[background][region].items()[0]
        nuisances[nuisancename]  = {
            'name'    : nuisancename+year, 
            'samples' : { background : value },
            'cuts'    : [ ], 
            'type'    : 'lnN',
        }
        for cut in cuts.keys():
            for subregion in subregions:
                if subregion=='_All' or subregion in cut:
                    nuisances[nuisancename]['cuts'].append(cut)
                    break

### shapes

# lepton reco, id, iso, fastsim

weightEle   = '('+EleWeight.replase('IdiIsoSF', 'IdIsoSF_Syst')+')/('+EleWeight+')'
weightMuo   = '('+MuoWeight.replase('IdiIsoSF', 'IdIsoSF_Syst')+')/('+MuoWeight+')'
weightLep   = '('+LepWeight.replase('IdiIsoSF', 'IdIsoSF_Syst')+')/('+LepWeight+')'
weightEleFS = weightEle.replace('IdIsoSF', 'FastSimSF')
weightMuoFS = weightMuo.replace('IdIsoSF', 'FastSimSF')
weightLepFS = weightLep.replace('IdIsoSF', 'FastSimSF')

leptonSF = { 
    #'trakreco'        : [ '1.', '1.' ], ->  no scale factor required 
    #'electronIdIso'   : [ weightEle.replace('Syst', 'Up'),   weightEle.replace('Syst', 'Down')   ],
    #'muonIdIso'       : [ weightMuo.replace('Syst', 'Up'),   weightMuo.replace('Syst', 'Down')   ],
    'leptonIdIso'     : [ weightLep.replace('Syst', 'Up'),   weightLep.replace('Syst', 'Down')   ], 
    #'electronIdIsoFS' : [ weightEleFS.replace('Syst', 'Up'), weightEleFS.replace('Syst', 'Down') ],
    #'muonIdIsoFS'     : [ weightMuoFS.replace('Syst', 'Up'), weightMuoFS.replace('Syst', 'Down') ],
    'leptonIdIsoFS'   : [ weightLepFS.replace('Syst', 'Up'), weightLepFS.replace('Syst', 'Down') ], 
}

for scalefactor in leptonSF:
    nuisances[scalefactor]  = {
        'name'  : scalefactor+year,
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in samples.keys():
        if sample!='DATA':
            if 'FS' not in scalefactor:
                nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]
            else:
                for model in signalMassPoints:
                    if sample in signalMassPoints[model].keys():
                        nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]

# b-tagging scale factors

weight1b = 'btagWeight_1tag_syst/btagWeight_1tag'
weight0b = '(1.-btagWeight_1tag_syst)/(1.-btagWeight_1tag)'

btagSF = {
    'btag1b'     : [ weight1b.replace('syst', 'b_up'),         weight1b.replace('syst', 'b_down') ],
    'btag0b'     : [ weight0b.replace('syst', 'b_up'),         weight0b.replace('syst', 'b_down') ],
    'mistag1b'   : [ weight1b.replace('syst', 'l_up'),         weight1b.replace('syst', 'l_down') ],
    'mistag0b'   : [ weight0b.replace('syst', 'l_up'),         weight0b.replace('syst', 'l_down') ],
    'btag1bFS'   : [ weight1b.replace('syst', 'b_up_fastsim'), weight1b.replace('syst', 'b_down_fastsim') ],
    'btag0bFS'   : [ weight0b.replace('syst', 'b_up_fastsim'), weight0b.replace('syst', 'b_down_fastsim') ],
    'ctag1bFS'   : [ weight1b.replace('syst', 'c_up_fastsim'), weight1b.replace('syst', 'c_down_fastsim') ],
    'ctag0bFS'   : [ weight0b.replace('syst', 'c_up_fastsim'), weight0b.replace('syst', 'c_down_fastsim') ],
    'mistag1bFS' : [ weight1b.replace('syst', 'l_up_fastsim'), weight1b.replace('syst', 'l_down_fastsim') ],
    'mistag0bFS' : [ weight0b.replace('syst', 'l_up_fastsim'), weight0b.replace('syst', 'l_down_fastsim') ],
}

for scalefactor in btagSF:
    nuisances[scalefactor]  = {
        'name'  : scalefactor+year,
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
        'cuts'  : [ ]           
    }
    for sample in samples.keys():
        if sample!='DATA':
            if 'FS' not in scalefactor:
                nuisances[scalefactor]['samples'][sample] = btagSF[scalefactor]
            else:
                for model in signalMassPoints:
                    if sample in signalMassPoints[model].keys():
                        nuisances[scalefactor]['samples'][sample] = btagSF[scalefactor]
    for cut in cuts.keys():
        if ('1b' in scalefactor and '_Tag' in cut) or 
           ('0b' in scalefactor and ('_Veto' in cut or '_NoTag' in cut)):
            nuisances[scalefactor]['cuts'].append(cut)

# pileup

nuisances['pileup']  = {
    'name'  : 'pileup', # inelastic cross section correlated through the years
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if sample!='DATA':
        nuisances['pileup']['samples'][sample] = [ 'puWeightPu/puWeight', 'puWeightDown/puWeight' ] 

# nonprompt lepton rate

nuisances['nonpromptLep']  = {
    'name'  : 'nonpromptLep'+year, 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if sample!='DATA':
        nuisances['nonpromptLep']['samples'][sample] = [ 'nonpromptLepSF_Up/nonpromptLepSF', 'nonpromptLepSF_Down/nonpromptLepSF' ] 

# top pt reweighting

nuisances['toppt']  = {
    'name'  : 'toppt', # assuming the mismodeling is correlated through the years 
    'samples'  : { 'ttbar' : [ '1./'+Top_pTrw, '1.' ] },
    'kind'  : 'weight',
    'type'  : 'shape',
}

# isr fastsim
nuisances['isrFS']  = {
    'name'  : 'isrFS', # assuming the mismodeling is correlated through the years 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    for model in signalMassPoints:
        if 'T2' in model:
            isrWeight = [ '0.5*(3.*isrW-1.)', '0.5*(isrW+1.)/isrW' ]
        elif 'TChi' in model:
            isrWeight = [ '(2.*isrW-1.)/isrW', '1./isrW' ]
        elif:
            print 'ERROR: no isrW implementation for model', model
        if sample in signalMassPoints[model].keys():
            nuisances['isrFS']['samples'][sample] = isrWeight

### mt2ll backgrounds (special case for shape uncertainties)

# mt2ll top and WW

mt2llRegions = ['SR1_', 'SR2_', 'SR3_']
mt2llBins = ['Bin4', 'Bin5', 'Bin6', 'Bin7']
mt2llEdges = ['60.', '80.', '100.', '120.', '999999999.']
mt2llSystematics = [0.05, 0.10, 0.20, 0.30]

for mt2llregion in mt2llRegions: 
    for mt2llbin in range(len(mt2llBins)):

        mt2llsystname = mt2llregion + mt2llBins[mt2llbin]
        mt2llweightUp = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.+mt2llSystematics[mt2llbin])+' : 1.'  
        mt2llweightDo = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.-mt2llSystematics[mt2llbin])+' : 1.'  
        
        nuisances['Top_'+mt2llsystname]  = {
               'name'  : 'Top_'+mt2llsystname+year,
               'samples'  : { 
                   'ttbar' : [ mt2llweightUp, mt2llweightDo],
                   'tW'    : [ mt2llweightUp, mt2llweightDo],
               },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [ ]           
              }
        
        nuisances['WW_'+mt2llsystname]  = {
               'name'  : 'WW_'+mt2llsystname+year,
               'samples'  : { 
                   'WW' : [ mt2llweightUp, mt2llweightDo],
               },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [ ]           
              }

        for cut in cuts.keys():
            if mt2llregion in cut:
                nuisances['Top_'+mt2llsystname]['cuts'].append(cut)
                nuisances['WW_' +mt2llsystname]['cuts'].append(cut)

# mt2ll DY (from control regions)
 
# mt2ll ZZ (from k-factors)

# mt2ll signal

nuisances['metfastsim']  = {
               'name'  : 'metfastsim',
               'samples'  : { },
               'kind'  : 'tree',
               'type'  : 'shape',
              }
for sample in samples.keys():
    for model in signalMassPoints:
        if sample in signalMassPoints[model].keys():
            nuisances['metfastsim']['samples'][sample] = ['1.2', '0.8'] # placeholder

### LHE weights

### JES and MET

### rate parameters

rateparameters = {
    'Topnorm' :  { 
        'samples' : [ 'ttbar', 'tW' ],
        'subcut'  : '',
    },
    'WWnorm'  : {
        'samples' : [ 'WW' ],
        'subcut'  : '',
    },
    'NoJetRate_JetBack' : {
        'samples' : [ 'ttbar', 'tW', 'ttW', 'ttZ' ],
        'subcut'  : '_NoJet_',
        'limits'  : '[0.5,1.5]',
    },
    'JetRate_JetBack' : {
        'samples'  : [ 'ttbar', 'tW', 'ttW', 'ttZ' ],
        'subcut'   : '_NoTag_',
        'bondrate' : 'NoJetRate_JetBack',
    },
    'NoJetRate_DibosonBack' : {
        'samples' : [ 'WW', 'WZ' ],
        'subcut'  : '_NoJet_',
        'limits'  : '[0.7,1.3]'
    },
    'JetRate_DibosonBack' : {
        'samples' : [ 'WW', 'WZ' ],
        'subcut'  : '_NoTag_',
        'bondrate' : 'NoJetRate_DibosonBack',
    },
}

if hasattr(opt, 'inputFile'):
    for mt2llregion in mt2llRegions: 
        for rateparam in rateparameters: 
            
            rateparamname = rateparam + '_' + mt2llregion
            
            for sample in rateparameters[rateparam]['samples']:
                
                nuisances[sample+rateparamname]  = {
                    'name'  : rateparamname+year,
                    'samples'  : { sample : '1.00' },
                    'type'  : 'rateParam',
                    'cuts'  : [ ] 
                }
                
                if 'limits' in rateparameters[rateparam].keys():
                    nuisances[sample+rateparamname]['limits'] = rateparameters[rateparam]['limits'] 
                    
                for cut in cuts.keys():
                    if mt2llregion in cut and rateparameters[rateparam]['subcut'] in  cut:

                        nuisances[sample+rateparamname]['cuts'].append(cut)
                        
                        if 'bondrate' in rateparameters[rateparam].keys():

                            bond_formula = '1+@0/@1*(1.-@2)' 
                                
                            fileIn = ROOT.TFile(opt.inputFile, "READ")

                            nuisances[sample+rateparamname]['bond'] = {}

                            for variable in variables.keys():

                                histoB = fileIn.Get(cut+'/'+variable+'/histo_'+sample)
                                cutB = rateparameters[rateparam]['subcut']
                                cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcut']
                                histoA = fileIn.Get(cut.replace(cutB, cutA)+'/'+variable+'/histo_'+sample)
                                yieldB = '%-.4f' % histoB.Integral()
                                yieldA = '%-.4f' % histoA.Integral()
            
                                bond_parameters = yieldA+','+yieldB+','+rateparameters[rateparam]['bondrate']+'_'+mt2llregion+year

                                nuisances[sample+rateparamname]['bond'][variable] =  { bond_formula : bond_parameters }

                            fileIn.Close()



