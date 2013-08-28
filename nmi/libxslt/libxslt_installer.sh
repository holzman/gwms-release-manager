#!/bin/bash
export NO_SETUPTOOLS=1

/bin/tar xfvz libxslt-1.1.17.tar.gz
cd libxslt-1.1.17
./configure --prefix=`pwd`/../libxslt && make && make install

