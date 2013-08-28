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

# pylint 
export PYTHONPATH=${PYHOME}/lib/python2.4/site-packages:${PYTHONPATH}
export PYTHONPATH=${PYHOME}/lib/python2.6/site-packages:${PYTHONPATH}

# rrdtool
export PYTHONPATH=`pwd`/rrdtool/lib/python2.4/site-packages:${PYTHONPATH}
export PYTHONPATH=`pwd`/rrdtool/lib/python2.6/site-packages:${PYTHONPATH}
export PYTHONPATH=`pwd`/rrdtool/lib64/python2.4/site-packages:${PYTHONPATH}
export PYTHONPATH=`pwd`/rrdtool/lib64/python2.6/site-packages:${PYTHONPATH}
export LD_LIBRARY_PATH=`pwd`/rrdtool/lib:${LD_LIBRARY_PATH}

# dummy-ldap
export PYTHONPATH=`pwd`/dummy-ldap:${PYTHONPATH}

# libxslt
export PYTHONPATH=`pwd`/libxslt/lib/python2.4/site-packages:${PYTHONPATH}
export PYTHONPATH=`pwd`/libxslt/lib/python2.6/site-packages:${PYTHONPATH}
export PYTHONPATH=`pwd`/libxslt/lib64/python2.4/site-packages:${PYTHONPATH}
export PYTHONPATH=`pwd`/libxslt/lib64/python2.6/site-packages:${PYTHONPATH}

export BAREPYTHONPATH=${PYTHONPATH}

# pythonpath for pre-packaged only
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
  
  export errors="${line/\//.}-err.txt"
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

export PYTHONPATH=${BAREPYTHONPATH}
while read line
do
    cd ${GHOME}
    ${currdir}/git-1.7.6/git checkout $line
    export errors="${line/\//_SLASH_}-err.txt"
    export results="$results $errors"
    exitstatus=0
    cd $currdir
# ignore configGUI -- I'm not ready to build wxPython on NMI yet !
    pylint --rcfile=/dev/null --errors-only -e F0401 glideinwms --ignore=configGUI.py>> $currdir/$errors
    # get list of python scripts without .py extension
    scripts=`find glideinwms -path glideinwms/.git -prune -o -exec file {} \; -a -type f | grep -i python | grep -vi '\.py' | cut -d: -f1`
#    echo "checking version ${line} files: ${scripts}"
#    echo "- bb +-+-+-+-+-+-+-+-+"
#    pylint --rcfile=/dev/null ${scripts}
#    echo "- ee +-+-+-+-+-+-+-+-+"
    pylint --rcfile=/dev/null --errors-only -e F0401 ${scripts} >> $currdir/$errors

    echo "Modules checked=NA" >> $currdir/$errors
done < config-tmp.txt

#unset GHOME
#unset PYTHONPATH

tar czvf results.tar.gz $results

exit $exitstatus

