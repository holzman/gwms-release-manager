#!/bin/bash


/bin/tar xfvz rrdtool-1.4.7.tar.gz
cd rrdtool-1.4.7
./configure --prefix=`pwd`/../rrdtool && make && make install


