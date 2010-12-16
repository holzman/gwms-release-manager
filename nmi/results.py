#! /usr/bin/env python

import os, datetime, smtplib
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart

msg = MIMEMultipart()

# extract results
untar = 'tar -xzvf results.tar.gz'
os.system(untar)

# create file in which to write email body
os.system('touch body.txt')
body = open('body.txt', 'w')

top_line = 'Pylint runs submitted at 10:00am on %s\n\n' % datetime.datetime.now().strftime('%m-%d-%Y')
body.write(top_line)

# count number of files with errors and number of errors
for file in os.listdir(os.getcwd()):
  if file.endswith('errors.txt'):
    f = open(file, 'r')
    list = f.readlines()
    f.close()
    
    num_files = 0
    num_errors = 0

    for line in list:
      if line.startswith('*'):
        num_files += 1

      if line.startswith('E'):
        num_errors += 1
   
    n_line = '%s: %s files had errors (total %s errors)\n' % (file.split('-errors')[0], num_files, num_errors)
    body.write(n_line)

    # attach file
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(file,'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)

body.close()  

# compose and send email
frm = 'pylint-results@noreply.com'
#to = 'sfiligoi@fnal.gov'
#cc = 'malatorr@ucsd.edu'

bd = open('body.txt', 'r')
body = MIMEText(bd.read())
msg.attach(body)
bd.close()

msg['Subject'] = 'glideinWMS pylint errors %s' % datetime.datetime.now().strftime('%m-%d-%Y')
msg['From'] = frm
msg['To'] = to
msg['Cc'] = cc

s = smtplib.SMTP()
s.connect()
s.sendmail(frm, [to, cc], msg.as_string())
s.quit()
