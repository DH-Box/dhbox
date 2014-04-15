import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from string import Template
import ConfigParser

def make_an_email(who, ip_address, subject, text='../email.txt', is_file=True):
    
    config = ConfigParser.ConfigParser()
    config.read("../settings.cfg")
    gmail_user = str(config.get('config', 'MAIL_USERNAME'))
    gmail_pwd = str(config.get('config', 'MAIL_PASSWORD'))
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    to = who 
    # header = 'To:' + to + '\n' + 'From: ' + 'do-not-reply@dhbox.org' + '\n' + 'Subject:testing \n'
    # print header

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'do-not-reply@dhbox.org'
    msg['To'] = to
    if is_file:
        html = open(text).read()
        body = Template(html).substitute(ip_address=ip_address)
    else:
        html = text
    text = MIMEText(body, 'html')
    
    smtpserver.set_debuglevel(1)
    msg.attach(text)
    smtpserver.sendmail(gmail_user, to, msg.as_string())
    print 'done!'
    smtpserver.close()


if __name__ == '__main__':
    make_an_email(sys.argv[1], sys.argv[2], "Your New DH Box")