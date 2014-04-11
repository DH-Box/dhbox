import smtplib
import sys
from string import Template

def make_an_email(who, ip_address, filename='../email.txt'):
    to = who
    gmail_user = 'srzweibel@gmail.com'
    gmail_pwd = 'tryharder'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
    print header
    template = open(filename).read()
    msg = Template(template).substitute(ip_address=ip_address)
    # msg = "Welcome to DH Box! You can find your new DH Box at http://"+ ip_address +"."
    msg = header + '\n '+msg+' \n\n'
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()


if __name__ == '__main__':
    make_an_email(sys.argv[1], sys.argv[2])