#! /usr/bin/env python
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('branches.cfg')
br = config.get('Branches', 'branches')
branches = br.split('\n')

# create a directory to hold each branch
for branch in branches:
  dirname = '%s-branch' % branch
  cmd = "mkdir %s; cd %s; cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only co -r %s glideinWMS; cd .." % (dirname, dirname, branch)
  os.system(cmd)
