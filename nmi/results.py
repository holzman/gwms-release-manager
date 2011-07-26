#! /usr/bin/env python
import os, datetime, smtplib
from email import Encoders
from email.Utils import COMMASPACE
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

top_line = 'Pylint runs submitted at %s on %s' % (datetime.datetime.now().strftime('%H:%M'), datetime.datetime.now().strftime('%m-%d-%Y'))

html = """\
<html>
<head>
<style type="text/css">
table { border-collapse: collapse }
th, td { border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;}
</style>
</head>
<body>
%s
<br /><br />
""" % top_line

html2 = ''

# open remote_task.err; if pylint error, alert via email
f = open('remote_task.err', 'r')
remote_task_err = f.readlines()
f.close()
error = remote_task_err[0]
if error.endswith('pylint: command not found\n'):
    alert = """\
    Error on submit machine - pylint: command not found.<br />Please reinstall pylint on the submit machine and update pylint.nmi
    """
    html += '%s' % alert
else:
    # no error, proceed with regular email
    html += """\
    <table style="border-collapse: collapse">
    <tr>
    <th style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">Branch</th>
    <th style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">Modules Checked</th>
    <th style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">Modules With Errors</th>
    <th style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">Total Errors</th>
    </tr>
    """

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

            if line.startswith('Modules checked'):
                modules_checked = line.split('=')[1].split('\n')[0]
        
        f.close()

        branch_name = file.split('-err')[0]
        html += """\
        <tr>
        <td style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">%s</td>
        <td style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">%s</td>
        <td style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">%s</td>
        <td style="border-style: solid; border-width: 1px; text-align:center; padding: 2px; font-size: 14px;">%s</td>
        </tr>
        """ % (branch_name, modules_checked, num_files, num_errors)

        if len(filenames) > 0:
            html2 += "<hr>%s: The following modules had errors:<br />" % branch_name
            for filename in filenames:
                html2 += '  %s<br />' % filename  


        # add attachment to attachments array
        if num_errors > 0:
          part = MIMEBase('application', 'octet-stream')
          part.set_payload(open(new_error_files[i],'rb').read())
          Encoders.encode_base64(part)
          part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
          attachments.append(part)

        i+=1
    html += '</table>'

html += html2
html += """\
</body>
</html>
"""

# compose and send email
frm = 'pylint-results@noreply.com'
to = ['glideinwms@fnal.gov']

body = MIMEText(html, 'html')
msg.attach(body)

for attachment in attachments:
    msg.attach(attachment)

msg['Subject'] = 'GIT: glideinWMS pylint errors %s' % datetime.datetime.now().strftime('%m-%d-%Y')
msg['From'] = frm
msg['To'] = COMMASPACE.join(to)

s = smtplib.SMTP()
s.connect()
s.sendmail(frm, to, msg.as_string())
s.quit()
