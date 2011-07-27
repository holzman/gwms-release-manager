#!/bin/bash
/bin/tar xfvz pylint-0.21.2.tar.gz
cd pylint-0.21.2
python setup.py install --prefix `pwd`/../pylint

cd ..
/bin/tar xfvz logilab-astng-0.20.2.tar.gz
cd logilab-astng-0.20.2
python setup.py install --prefix `pwd`/../pylint

cd ..
/bin/tar xfvz logilab-common-0.51.1.tar.gz
cd logilab-common-0.51.1
python setup.py install --prefix `pwd`/../pylint



