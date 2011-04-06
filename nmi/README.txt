* Specify default branches in config.txt
* Specify notification recipient in gwms.submit
* Specify results email recipients in results.py
* Specify cron hour and minute for recurring runs in gwms.submit
* Ensure checkout.sh, pylint-gwms.sh, and results.py are executable

Process:
  First we need to install pylint onto the remote NMI machine.
  The pylint installation files are found in the pylint directory;
  Just run <nmi_submit pylint.submit>. Make a note of the run id.
  The disk cleaner will remove our installed files unless we pin
  the run. To do this, run <nmi_pin -days='X' runid>, where X is
  the number of days to keep the run and runid is the noted run id.
  Currently, it is pinned until February, 2012.

  Before running gwms.submit, we need to tell our job where
  to find the previously installed pylint files. We do so in the
  pylint.nmi file by setting <input_runids> to the noted run id.

  Now we can submit our gwms job:

  First, checkout.sh runs. We checkout the HEAD branch first, which
  is needed for get-other-branches.py.

  Next, get-other-branches.py runs. Here, for each python file in
  factory, frontend, tools, lib, tools/lib, and creation/lib we do
  the following:
    1. Run cvs log to check if any changes have been made to the file
       in the last two weeks.
    2. If a change was made, we extract the file name and revision number.
    3. For each file with changes, we run cvs status to get the list of
       tagnames for this file. We then check this list for the tagname
       that corresponds to the revision number.
    4. Last, we write the tagnames to config.txt

  Now that config.txt includes a list of all the branches that we are
  interested in, we run pylint-gwms.sh, which runs pylint against the
  necessary modules of each branch and tarballs the results.

  Finally, results.py runs which extracts the results and sends out
  the appropriate email.
