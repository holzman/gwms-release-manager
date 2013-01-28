#!/bin/bash  
export PYHOME=`pwd`/pylint
export PATH=${PYHOME}/bin:${PATH}

# dive into subdirs only for "prepackage" branches
grep -v '^[[:space:]]*#' config.txt | sort | grep -f prepackage-branches.txt | uniq > config-tmp.txt

echo "prepackage branches:"
echo "--------------------"
cat config-tmp.txt
echo "===================="

export currdir=$PWD
export results=""
export GHOME=`pwd`/glideinwms
 
export PYTHONPATH=${PYHOME}/lib/python2.4/site-packages:${PYTHONPATH}
export PYTHONPATH=${PYHOME}/lib/python2.6/site-packages:${PYTHONPATH}
export PYTHONPATH=${PYTHONPATH}:${GHOME}/lib
export PYTHONPATH=${PYTHONPATH}:${GHOME}/creation/lib
export PYTHONPATH=${PYTHONPATH}:${GHOME}/factory
export PYTHONPATH=${PYTHONPATH}:${GHOME}/frontend
export PYTHONPATH=${PYTHONPATH}:${GHOME}/tools
export PYTHONPATH=${PYTHONPATH}:${GHOME}/tools/lib

while read line
do
  cd ${GHOME}
  ${currdir}/git-1.7.6/git checkout ${line}
#  cd ${currdir}
  
  export errors="$line-err.txt"
  export results="$results $errors"

  modules_checked=0

  for dir in lib creation/lib factory frontend tools tools/lib
  do
    exitstatus=0
    cd ${GHOME}/$dir

    for file in *.py
    do
      ((modules_checked++))
      echo "##" $dir >> $currdir/$errors
      pylint --rcfile=/dev/null --errors-only $file >> $currdir/$errors
    done
    cd $currdir
  done
  echo "Modules checked="$modules_checked >> $currdir/$errors
done < config-tmp.txt

# handle all the rest
grep -v '^[[:space:]]*#' config.txt | sort | grep -v -f prepackage-branches.txt | uniq > config-tmp.txt

echo "package branches:"
echo "--------------------"
cat config-tmp.txt
echo "===================="

while read line
do
    cd ${GHOME}
    ${currdir}/git-1.7.6/git checkout $line
    export errors="$line-err.txt"
    export results="$results $errors"
    exitstatus=0
    cd $currdir
# ignore configGUI -- I'm not ready to build wxPython on NMI yet !
    pylint --rcfile=/dev/null --errors-only glideinwms --ignore=configGUI.py>> $currdir/$errors
    echo "Modules checked=NA" >> $currdir/$errors
done < config-tmp.txt

#unset GHOME
#unset PYTHONPATH

tar czvf results.tar.gz $results

exit $exitstatus

