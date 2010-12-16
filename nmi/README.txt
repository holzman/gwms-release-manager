# branches.cfg
Configuration file to list branches to checkout as well as directories to run pylint against.

# pylint.nmi
Points to pylint NMI build.

# checkout.py
Checks out each branch into its own directory.

# export-paths.sh
Exports environment variables (ie, PYTHONPATH), then calls pylint.py

# pylint.py
Runs pylint against each branch, saves the results of each branch in a text file and tarballs all results.

# results.py
Extracts results and sends email with brief error description along and error files attached.
Be sure to uncomment and set 'to' and 'cc' if needed.

# gwms-all.submit
Be sure to uncomment and set 'notify' email to be notified on job completion.
Be sure to uncomment and set cron parameters for recurring job.
