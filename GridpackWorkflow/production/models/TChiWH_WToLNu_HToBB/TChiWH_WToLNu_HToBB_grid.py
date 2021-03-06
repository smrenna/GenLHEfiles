#!/usr/bin/env python

### Script to define scan grid

### Authors:
### Manuel Franco Sevilla
### Ana Ovcharova

import os,sys,math,pprint
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid_utils import *

# Parameters that define the grid in the bulk and diagonal
class gridBlock:
  def __init__(self, xmin, xmax, xstep, ystep):
    self.xmin = xmin
    self.xmax = xmax
    self.xstep = xstep
    self.ystep = ystep
    
model = "TChiWH_WToLNu_HToBB"
process = "C1N2"

# Number of events: min(goalLumi*xsec, maxEvents) (always in thousands)

scanBlocks = []
scanBlocks.append(gridBlock(150, 701, 25, 25))

minDM = 126
maxDM = 176
ymin, ymax = 0, 300

# Number of events for mass point, in thousands
def events(dm):
  if (mx-my)<maxDM: return 100
  else: return 30
  
# -------------------------------
#    Constructing grid

cols = []
Nevents = []
xmin, xmax = 9999, 0
for block in scanBlocks:
  Nbulk, Ndiag = 0, 0
  for mx in range(block.xmin, block.xmax, block.xstep):
    xmin = min(xmin, block.xmin)
    xmax = max(xmax, block.xmax)
    col = []
    my = 0
    begDiag = mx-maxDM
    # Adding bulk points
    if (mx-block.xmin)%block.xstep == 0:
      for my in range(ymin, mx-minDM, block.ystep):
        if my > ymax: continue
        nev = events(mx-my)
        col.append([mx,my, nev])
        Nbulk += nev
    if my !=  mx-minDM and mx-minDM <= ymax:
      my = mx-minDM
      nev = events(mx-my)
      col.append([mx,my, nev])
      Ndiag += nev
    cols.append(col)
  Nevents.append([Nbulk, Ndiag])

mpoints = []
for col in cols: mpoints.extend(col)
mpoints.append([126,0,100])


## Test print out for repeated points
mset = set()
for mp in mpoints: mset.add(mp[0]*10000+mp[1])
Ntot, Ndiff = len(mpoints), len(mset)
if Ntot==Ndiff: print "\nGrid contains "+str(Ntot)+" mass points. No duplicates\n"
else: print "\n\nGRID CONTAINS "+str(Ntot-Ndiff)+" DUPLICATE POINTS!!\n\n"

# -------------------------------
#     Plotting and printing

makePlot([mpoints], 'events', model, process, xmin, xmax, ymin-200, ymax)
Ntot = makePlot([mpoints], 'lumi', model, process, xmin, xmax, ymin-200, ymax)
#makePlot(cols, 'factor')

print '\nScan contains '+"{0:,.0f}".format(Ntot*1e3)+" events\n"
print 'Average matching efficiency (for McM and GEN fragment) = '+"{0:.3f}".format(getAveEff(mpoints,process))
print

for ind in range(len(scanBlocks)):
  Nbulk, Ndiag = Nevents[ind][0]/1e3, Nevents[ind][1]/1e3
  Nblock = Nbulk+Ndiag
  print "From "+'{:>4}'.format(scanBlocks[ind].xmin)+" to "+str(scanBlocks[ind].xmax)+": ",
  print "{0:>4.1f}".format(Nblock)+"M ("+"{0:>4.1f}".format(Nblock/Ntot*100)+" %) events, "+"{0:>4.1f}".format(Nbulk),
  print "M ("+"{0:>4.1f}".format(Nbulk/Ntot*100)+" %) in the bulk, "+"{0:>4.1f}".format(Ndiag)+"M (",
  print "{0:.1f}".format(Ndiag/Ntot*100)+" %) in the diagonal"

print
