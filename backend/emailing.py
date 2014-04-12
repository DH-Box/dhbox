import smtplib
import sys
from string import Template
import ConfigParser

def make_an_email(who, ip_address, filename='../email.txt'):
    
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
    header = 'To:' + to + '\n' + 'From: ' + 'do-not-reply@dhbox.org' + '\n' + 'Subject:testing \n'
    print header
    template = open(filename).read()
    msg = Template(template).substitute(ip_address=ip_address)
    msg = header + '\n '+msg+' \n\n'
    smtpserver.set_debuglevel(1)
    # try:
    #     smtpserver.starttls() 
    #     smtpserver.login(login, password) 
    #     smtpserver.sendmail(gmail_user, to, msg)
    # finally:
    #     smtpserver.quit()

    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()


if __name__ == '__main__':
    make_an_email(sys.argv[1], sys.argv[2])