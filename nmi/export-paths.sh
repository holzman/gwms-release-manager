#!/bin/bash

export PYHOME=`pwd`/pylint
export GHOME=`pwd`
export PATH=${PYHOME}/bin:${PATH}
export PYTHONPATH=${PYHOME}/lib/python2.4/site-packages:${PYTHONPATH}

for dir in ${GHOME}
do
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/$dir/lib
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/$dir/creation/lib
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/$dir/factory
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/$dir/frontend
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/$dir/tools
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/$dir/tools/lib
done

python pylint.py
