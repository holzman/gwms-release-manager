#!/usr/bin/env python
import os, sre, time
from datetime import date, timedelta
import subprocess
from sets import Set

logopts  = ['/usr/bin/git', 'log', '--all', '--oneline', '--since', '"1 week ago"']
logopts += ['--pretty=format:%d']

p = subprocess.Popen(logopts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout, stderr) = p.communicate()
logOutput = stdout.split('\n')

pattern = sre.compile('.*\((.*)\)')

branchlist = Set()
for line in logOutput:  # list that looks like " (branch1, branch2, branch3) "
    m = sre.match(pattern, line)
    if m:
        branches = m.group(1).split(',')
        for x in branches: branchlist.add(x.strip())

# get list of branches to include
p = subprocess.Popen(['/usr/bin/git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

(stdout, stderr) = p.communicate()
includebranches = Set(stdout.split())
#includebranches.add('refs/stash')

branchlist.intersection_update(includebranches)

config_file = open('../config.txt', 'a')
# TODO: read in lines and guarantee uniqueness
config_file.writelines('\n'.join(branchlist))
config_file.close()
