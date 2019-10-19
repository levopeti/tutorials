# smtplib module send mail

import smtplib
from getpass import getpass

TO = 'kun.t1992@gmail.com'
SUBJECT = 'TEST MAIL'
TEXT = 'Ezt egy python script-bol kuldtem.'

# Gmail Sign In
gmail_sender = 'leviskocka@gmail.com'
gmail_passwd = getpass()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)

BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print ('email sent')
except:
    print ('error sending mail')

server.quit()
