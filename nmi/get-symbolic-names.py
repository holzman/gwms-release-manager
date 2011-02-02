#!/usr/bin/env python
# gets all branches with commits within the past two weeks and writes branch name to other_branches.txt
import os, re
from datetime import date, timedelta

symbolic_names = []
today = date.today()
root_dir = os.getcwd()
head_dir = root_dir + '/HEAD'
path_to_log = '%s/log.txt' % head_dir
directories = ['glideinWMS/factory', 'glideinWMS/frontend', 'glideinWMS/tools', 'glideinWMS/lib', 'glideinWMS/tools/lib', 'glideinWMS/creation/lib']

os.chdir(head_dir)

# iterate through all files in glideinWMS to get a list of all symbolic names
for directory in directories:
    os.chdir(directory)
    for file in os.listdir(os.getcwd()):
        if file.endswith('.py'):
          # save results of log into log
          cmd = 'cvs log -d ">=%s" %s > log.txt' % (today.isoformat(), file)
          os.system(cmd)

          next = 1
          f = open('log.txt', 'r')

          for line in f:
              if line.startswith('symbolic names'):
                  next = 0
                  continue

              if line.startswith('keyword substitution'):
                  next == 1
                  break

              if next == 0:
		  print('\n')
                  add_symbolic_name = 1

                  version_num = line.split(':')[1].split('.')

                  # first, check if symbolic name version numer has 0 as second to last number
                  if int(version_num[len(version_num)-2]) == 0:
                      print("version number is at end of this line %s")	% line.split('\n')[0]
       	       	      print("version number second to last is 0, need to add")
       	       	  else:
       	       	      print("version number is at end of this line %s") % line.split('\n')[0]
       	       	      print("version number second to last is not 0, do not add")
       	       	      add_symbolic_name	= 0

                  # now check if symbolic name has already been added
                  if add_symbolic_name == 1:
                      symbolic_name_from_file = line.split(':')[0].split('\t')[1]
                      for existing_symbolic_name in symbolic_names:
                          if symbolic_name_from_file == existing_symbolic_name:
                              add_symbolic_name = 0
                              print("symbolic name already exists, not adding")
                              print("symbolic name from line: %s") % symbolic_name_from_file
                              print("symbolic name from array: %s") % existing_symbolic_name

                  if add_symbolic_name == 1:
                      print("symbolic does not exist, adding")
                      print("symbolic name from line: %s") % symbolic_name_from_file
                      symbolic_names.append(symbolic_name_from_file)

          f.close()
    os.chdir(head_dir)

print("Length of symbolic_names: %s") % len(symbolic_names)
print(symbolic_names)

regex_id = re.compile(r"\$Id\:")
regex_date = re.compile("[0-9]{4}\/[0-9]{2}\/[0-9]{2}")

checkout = []
no_checkout = []
no_version_no_date = []
no_version_yes_date = []
yes_version_no_date = []
yes_version_yes_date_not_greater = []

two_weeks_ago = today - timedelta(days=14)

os.system('ls')

# for each symbolic name, diff it against each file. if we can get extract a date from the file version of the output, pop the symbolic_name out
for directory in directories:
    os.chdir(directory)
    print("*************************************************************************************")
    print("In directory %s") % directory
    print("Length of symbolic names: %s") % len(symbolic_names)
    for file in os.listdir(os.getcwd()):
        if file.endswith('.py'):
            print("** In file %s: ") % file
            print("** length of symbolic names: %s") % len(symbolic_names)
            i = 0
            for symbolic_name in symbolic_names:
                i += 1
                print("**Checking symbolic name %s") % i
                cmd = 'cvs diff -r %s %s > diff.txt' % (symbolic_name, file)
                os.system(cmd)

                found_id = 0
                found_date = 0
                
                # get file version
                f = open('diff.txt', 'r')
                for line in f:
                    if regex_id.search(line):
                        found_id = 1
                        if regex_date.search(line):
                            found_date = 1
                            compose_date = regex_date.search(line).group().split('/')
                            version_date = date(int(compose_date[0]), int(compose_date[1]), int(compose_date[2]))
                            print version_date.isoformat()
                            print two_weeks_ago.isoformat()
                            # if this date is within the past two weeks, append branch to checkout
                            if version_date >= two_weeks_ago:
                                print("Version date is greater than two weeks ago. Saving this symbolic name and removing from symbolic_names array")
                                checkout.append(symbolic_name)
                                print("length before removal: %s") % len(symbolic_names)
                                symbolic_names.remove(symbolic_name)
                                print("length after removal: %s") % len(symbolic_names)
                            else:
                                print("Version date is not greater than two weeks ago. Not saving this symbolic name")
                                yes_version_yes_date_not_greater.append(symbolic_name)
                        break

                if found_id == 0 and found_date == 0:
                    print("Did not find file version nor version date")
                    no_version_no_date.append(symbolic_name)

                if found_id == 0 and found_date == 1:
                    print("Did not find file version but found version date")
                    no_version_yes_date.append(symbolic_name)

                if found_id == 1 and found_date == 0:
                    print("Found file version but did not find version date")
                    yes_version_no_date.append(symbolic_name)

                f.close() 
                print("=====================================================================================")

    os.chdir(head_dir)

# remove duplicates
no_version_no_date = list(set(no_version_no_date))
no_version_yes_date = list(set(no_version_yes_date))
yes_version_no_date = list(set(yes_version_no_date))
yes_version_yes_date_not_greater = list(set(yes_version_yes_date_not_greater))
checkout = list(set(checkout))

# remove checkout entries from all other arrays
for symbolic_name in checkout:
    for s in no_version_no_date:
        if s == symbolic_name:
            no_version_no_date.remove(s)

    for s in no_version_yes_date:
        if s == symbolic_name:
            no_version_yes_date.remove(s)

    for s in yes_version_no_date:
        if s == symbolic_name:
            yes_version_no_date.remove(s)

    for s in yes_version_yes_date_not_greater:
        if s == symbolic_name:
            yes_version_yes_date_not_greater.remove(s)

print("no version no date length: %s") % len(no_version_no_date)
print("no version yes date length: %s") % len(no_version_yes_date)
print("yes version no date length: %s") % len(yes_version_no_date)
print("yes version yes date length not greater: %s") % len(yes_version_yes_date_not_greater)
print("checkout length: %s") % len(checkout)

os.chdir(root_dir)

# append symbolic names to config.txt
f = open('config.txt', 'a')
for symbolic_name in checkout:
    f.write(symbolic_name + '\n')
f.close()
