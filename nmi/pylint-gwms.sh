#!/bin/bash
export PYHOME=`pwd`/pylint
export PATH=${PYHOME}/bin:${PATH}

grep -v '^[[:space:]]*#' config.txt > config-tmp.txt

export currdir=$PWD
export results=""

while read line
do
  export GHOME=`pwd`/$line/glideinWMS
  export PYTHONPATH=${PYHOME}/lib/python2.4/site-packages:${PYTHONPATH}
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/lib
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/creation/lib
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/factory
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/frontend
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/tools
  export PYTHONPATH=${PYTHONPATH}:${GHOME}/tools/lib
  
  export errors="$line-err.txt"
  export results="$results $errors"

  for dir in lib creation/lib factory frontend tools tools/lib
  do
    exitstatus=0
    cd ${GHOME}/$dir

    for file in *.py
    do
      echo "##" $dir >> $currdir/$errors
      pylint --errors-only $file >> $currdir/$errors
    done 
    cd $currdir
  done
  unset GHOME
  unset PYTHONPATH
done < config-tmp.txt

tar czvf results.tar.gz $results

exit $exitstatus

