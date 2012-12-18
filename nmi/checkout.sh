#!/bin/bash 

export currdir=$PWD

/usr/bin/git --version
/usr/bin/git clone --mirror http://cdcvs.fnal.gov/projects/glideinwms glideinwms/.git


cd glideinwms
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

