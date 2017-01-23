#!/bin/sh
SCRIPT="../../test/scripts/submitLHECondorJob.py"
MODEL="tHW"

for MPROD in {350..550..20}; do  
    python ${SCRIPT} ${MODEL}_mH-${MPROD} --in-file /hadoop/cms/store/user/${USER}/mcProduction/GRIDPACKS/${MODEL}_mH-${MPROD}/${MODEL}_mH-${MPROD}_tarball.tar.xz  --proxy ${vomsdir} --nevents 25000 --njobs 5
done


