import boto
import urllib2
import json

req = urllib2.Request("https://raw.github.com/DH-Box/dhbox/master/out.json")
opener = urllib2.build_opener()
f = opener.open(req)
data = json.load(f)
template = json.dumps(data)

c = boto.connect_cloudformation()
c.create_stack(template_body=template, stack_name='DHBox', parameters=[('KeyName', 'stevess')])

