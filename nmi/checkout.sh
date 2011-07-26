#!/bin/bash

export currdir=$PWD

#/usr/bin/git clone --mirror http://cdcvs.fnal.gov/projects/burt-test glideinWMS/.git
/usr/bin/git clone --mirror http://cdcvs.fnal.gov/projects/glideinwms glideinWMS/.git


cd glideinWMS
/usr/bin/git config --bool core.bare false
/usr/bin/git checkout master

python ../get-other-branches.py
cd ..

echo "Printing contents of config.txt"
echo "-------------------------------"
grep -v -E '^#' config.txt | sort | uniq

echo
echo "Printing directory contents"
echo "---------------------------"
ls -lrt

