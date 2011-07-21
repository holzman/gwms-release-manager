#!/bin/bash -vx
 
# assumes you already have the appropriate GlideinWMS tarball in /usr/src/redhat/SOURCES
# see the specfile for details

cp -f SOURCES/* /usr/src/redhat/SOURCES/
cp -f SPECS/* /usr/src/redhat/SPECS/

rpmbuild -bs /usr/src/redhat/SPECS/glideinwms-vofrontend.spec
