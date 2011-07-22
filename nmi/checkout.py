#! /usr/bin/env python
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('branches.cfg')
br = config.get('Branches', 'branches')
branches = br.split('\n')

cmd = 'git clone http://cdcvs.fnal.gov/projects/glideinwms'
os.system(cmd)
