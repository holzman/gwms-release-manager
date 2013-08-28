#!/bin/sh

echo "Host Name: `hostname -f 2>&1`"
echo "Host Arch: `uname -i 2>&1`"
echo "Host Distro: `cat /etc/redhat-release 2>&1`"
echo "Python Version: `python -V 2>&1`"
echo "Current Working Directory: `pwd`"
echo "Current Directory Contents: "
/bin/ls -lrt

