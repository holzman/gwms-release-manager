#!/usr/bin/env python
import os, re, time
from datetime import date, timedelta

root_dir = os.getcwd()
head_dir = root_dir + '/glideinWMS'
log_file = head_dir + '/log.txt'
status_file = head_dir + '/status.txt'
os.chdir(head_dir)

d = date.today() + timedelta(days=1)
tomorrow = '%s-%s-%s' % (d.year, d.month, d.day)
d = date.today() - timedelta(days=14)
two_weeks_ago = '%s-%s-%s' % (d.year, d.month, d.day)

directories = ['factory', 'frontend', 'tools', 'lib', 'tools/lib', 'creation/lib']

for directory in directories:
    os.chdir(directory)
    for file in os.listdir(os.getcwd()):
        if file.endswith('.py'):
            cmd = 'cvs log -N -S -d "%s<%s" %s >> %s' % (two_weeks_ago, tomorrow, file, log_file)
            os.system(cmd)
    os.chdir(head_dir)

# grab file names and revision numbers
f = open('log.txt', 'r')
a = {}

# each file could have many revisions
n = 0
for line in f:
    if line.startswith('RCS file'):
        filename = line.split('\n')[0].split(',v')[0].split('glideinWMS/')[-1] + "_flag"

    if line.startswith('revision'):
        rev_array = line.split('\n')[0].split(' ')[1].split('.')
        if len(rev_array) > 2:
            rev_array.pop()
        branch = ''
        for i in range(len(rev_array)):
            if i == 0:
                branch += '%s' % rev_array[i]
            else:
                branch += '.%s' % rev_array[i]
        filename += "%s" % n
        a[filename] = branch
        n += 1

f.close()

# find tag names
tags = []

if len(a) > 0:
    for filename, branch in a.iteritems():
        # strip filename of flag and add closed parenthesis to branch
        filename = filename.split('_flag')[0]
        branch = branch + ')\n'
        cmd = 'cvs status -v %s > status.txt' % filename
        os.system(cmd)

        f = open('status.txt', 'r')
        for line in f:
            if line.endswith(branch):
                tag = line.split('\t')[1]
                tags.append(tag)
        f.close()

os.chdir(root_dir)

config_file = open('config.txt', 'a')

tagnames = set(tags)
for tagname in tagnames:
    if tagname != '':
        line = tagname + '\n'
        config_file.write(line)

config_file.close()
