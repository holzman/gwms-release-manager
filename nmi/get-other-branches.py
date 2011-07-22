#!/usr/bin/env python
import os, sre, time
from datetime import date, timedelta
import subprocess
from sets import Set

logopts  = ['git', 'log', '--all', '--oneline', '--since', '"1 week ago"']
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

# get list of remote branches to exclude
p = subprocess.Popen(['git', 'branch', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

(stdout, stderr) = p.communicate()
excludebranches = Set(stdout.split())
excludebranches.add('refs/stash')

branchlist.difference_update(excludebranches)

config_file = open('config.txt', 'a')
config_file.writelines('\n'.join(branchlist))
config_file.close()
