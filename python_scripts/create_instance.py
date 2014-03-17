import boto
import boto.ec2
import urllib2

req = urllib2.Request("https://raw.github.com/DH-Box/dhbox/master/install_box.sh")
opener = urllib2.build_opener()
f = opener.open(req)

conn = boto.ec2.connect_to_region("us-east-1")

user_data = f.read()

conn.run_instances('ami-032b416a', key_name='stevess', security_groups=['default'], instance_type='t1.micro', user_data=user_data)

