import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

import math
baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     %MSQ%            # ~d_L
   2000001     %MSQ%            # ~d_R
   1000002     %MSQ%            # ~u_L
   2000002     %MSQ%            # ~u_R
   1000003     %MSQ%            # ~s_L
   2000003     %MSQ%            # ~s_R
   1000004     %MSQ%            # ~c_L
   2000004     %MSQ%            # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     1.00000000E+05   # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     1.00000000E+05   # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.10000000E+00   # sdown_L decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         1
DECAY   2000001     0.10000000E+00   # sdown_R decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         1
DECAY   1000002     0.10000000E+00   # sup_L decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         2
DECAY   2000002     0.10000000E+00   # sup_R decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         2
DECAY   1000003     0.10000000E+00   # sstrange_L decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         3
DECAY   2000003     0.10000000E+00   # sstrange_R decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         3
DECAY   1000004     0.10000000E+00   # scharm_L decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         4
DECAY   2000004     0.10000000E+00   # scharm_R decays
#          BR         NDA      ID1       ID2
1.00000E+00    2     1000022         4
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays

DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     0.00000000E+00   # neutralino2 decays
DECAY   1000024     0.00000000E+00   # chargino1+ decays
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

def matchParams(mass):
  if mass>99 and mass<299: return 62., 0.410 
  elif mass < 399: return 62., 0.413
  elif mass < 499: return 62., 0.414
  elif mass < 599: return 64., 0.416
  # the following are copied from SqSq
  elif mass<1299: return 68., 0.237
  elif mass<1451: return 70., 0.243
  elif mass<1801: return 74., 0.246
  else: return 76,0.2

# weighted average of matching efficiencies for the full scan
# must equal the number entered in McM generator params
mcm_eff = 0.413

model = "T2qqgamma"
process = "SqSqPlusGamma"


# Number of events for mass point, in thousands
nevt = 50

xmin, xmax, xstep = 200, 500, 50
dMs = [5,10,20,30,40,50]


# -------------------------------
#    Constructing grid

mpoints = []
for mx in range(xmin, xmax+1, xstep):  
  for dM in dMs:    
    my = mx-dM
    mpoints.append([mx,my,nevt])


for point in mpoints:
    msq = point[0]
    mlsp = point[1]
    qcut, tru_eff = matchParams(msq)
    wgt = point[2]*(mcm_eff/tru_eff)
    
    slhatable = baseSLHATable.replace('%MSQ%','%e' % msq)
    slhatable = slhatable.replace('%MLSP%','%e' % mlsp)

    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        JetMatchingParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 1', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '6:m0 = 172.5',
            'Check:abortIfVeto = on',
        ), 
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'JetMatchingParameters'
        )
    )

    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(wgt),
            GridpackPath =  cms.string('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.3.3/sus_sms/SMS-%s/SMS-%s_mSq-%s_tarball.tar.xz' % (process,process,msq)),
            ConfigDescription = cms.string('%s_%i_%i' % (model, msq, mlsp)),
            SLHATableForPythia8 = cms.string('%s' % slhatable),
            PythiaParameters = basePythiaParameters,
        ),
    )
