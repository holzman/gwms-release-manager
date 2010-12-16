#! /usr/bin/env python
import os
import ConfigParser

# get branches
config = ConfigParser.RawConfigParser()
config.read('branches.cfg')
br = config.get('Branches', 'branches')
branches = br.split('\n')

# get directories
dr = config.get('Directories', 'directories')
directories = dr.split('\n')

# will need to tar results later
tarcmd = 'tar czvf results.tar.gz'

# get path to all_branches
all_branches = os.environ.get('GHOME')

#run pylint on each branch
for branch in branches:
  tarcmd += ' %s-errors.txt' % (branch)
  for directory in directories:
    path = '%s/%s-branch/glideinWMS/%s' % (all_branches, branch, directory)
    cmd = 'pylint --errors-only %s/*.py >> %s-errors.txt' % (path, branch)
    os.system(cmd)

# create results tarball
os.system(tarcmd)
