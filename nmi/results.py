#! /usr/bin/env python

import os, datetime, smtplib
from email import Encoders
from email.Utils import	COMMASPACE
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart

attachments = []
error_files = []
new_error_files = []
msg = MIMEMultipart()

# extract results
untar = 'tar -xzvf results.tar.gz'
os.system(untar)

# create file in which to write email body
os.system('touch body.txt')
body = open('body.txt', 'w')

top_line = 'Pylint runs submitted at %s on %s\n\n' % (datetime.datetime.now().strftime('%H:%M'), datetime.datetime.now().strftime('%m-%d-%Y'))
body.write(top_line)

# open remote_task.err, if pylint error alert via email
f = open('remote_task.err', 'r')
remote_task_err = f.readlines()
f.close()
error = remote_task_err[0]
if error.endswith('pylint: command not found\n'):
  alert = ('Error on submit machine - pylint: command not found.\nPlease reinstall pylint on the submit machine and update pylint.nmi')
  body.write(alert)
else:
  # no error, proceed with regular email

  # count number of files with errors and number of errors
  for file in os.listdir(os.getcwd()):
    if file.endswith('err.txt'):
      error_files.append(file)
      new_error_filename = file.split('-err')[0]+'-errors.txt'
      cmd = 'touch %s' % new_error_filename
      os.system(cmd)
      new_error_files.append(new_error_filename)

  # sort error_files by file name length
  error_files.sort(key=lambda x: len(x))
  new_error_files.sort(key=lambda x: len(x))

  top_lines = []
  bottom_lines = []

  i = 0

  for file in error_files:
    f = open(file, 'r')
    list = f.readlines()
    f.close()

    # open corresponding new_error_file to write to
    f = open(new_error_files[i], 'a')  

    num_files = 0
    num_errors = 0
    filenames = []

    for line in list:
      if line.startswith('##'):
        filepath = line.split(' ')[1].split('\n')[0]

      if line.startswith('*'):
        num_files += 1
        filename = filepath+'/'+line.split(' ')[2].split('\n')[0]
        filenames.append(filename)
      
        # add path to line
        line_arr = line.split(' ')
        new_line = line_arr[0]+' '+line_arr[1]+' '+filepath+'/'+line_arr[2]
        f.write(new_line)

      if line.startswith('E'):
        num_errors += 1
        f.write(line)
  
    if len(filenames) > 0:
      bottom_lines.append('_________________________\n\n')
      n_line = '%s - The following %s modules had errors (total %s errors)\n' % (file.split('-err')[0], num_files, num_errors)
      bottom_lines.append(n_line)

      n_line = ''
      for filename in filenames:    
        bottom_lines.append('  '+filename+'\n')
    else:
      n_line = '%s - %s modules had errors (total %s errors)' % (file.split('-err')[0], num_files, num_errors)
      top_lines.append(n_line+'\n')

    f.close()

    # add attachment to attachments array
    if num_errors > 0:
      part = MIMEBase('application', 'octet-stream')
      part.set_payload(open(new_error_files[i],'rb').read())
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
      attachments.append(part)

    i += 1

  # write top lines then bottom lines
  for line in top_lines:
    body.write(line)
  for line in bottom_lines:
    body.write(line)

body.close()  

# compose and send email
frm = 'pylint-results@noreply.com'
to = ['sfiligoi@fnal.gov', 'burt@fnal.gov', 'malatorr@fnal.gov']

bd = open('body.txt', 'r')
body = MIMEText(bd.read())
msg.attach(body)
bd.close()

for attachment in attachments:
  msg.attach(attachment)

msg['Subject'] = 'glideinWMS pylint errors %s' % datetime.datetime.now().strftime('%m-%d-%Y')
msg['From'] = frm
msg['To'] = COMMASPACE.join(to)

s = smtplib.SMTP()
s.connect()
s.sendmail(frm, to, msg.as_string())
s.quit()
