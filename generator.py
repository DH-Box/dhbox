import urllib2

req = urllib2.Request("https://raw.github.com/DH-Box/dhbox/master/install_box.sh")
opener = urllib2.build_opener()
f = opener.open(req)

user_data_script = f.read()

cft = CloudFormationTemplate(description="DH Box Generated Template")
properties = {
    'ImageId': 'ami-032b416a',
    'InstanceType': 't1.micro',
    'UserData': base64(user_data_script),
    "KeyName": "stevess"
}
attributes = [
    Metadata(
        {
            "AWS::CloudFormation::Init": {
                "config": {
                    "packages": {
                        "apt": {
                            "apache2": [],
                            "default-jdk": [],
                            "shellinabox": [],
                            "ant": [],
                            "git-core": [],
                            "bash-completion": [],
                            "python-zmq": [],
                            "python-matplotlib": []
                        },
                    },
                    "commands": {
                        "test": {
                            "command": "echo \"$CFNTEST\" > test.txt",
                            "env": {"CFNTEST": "I come from config1."},
                            "cwd": "~",
                            "test": "test ! -e ~/test.txt",
                            "ignoreErrors": "false"
                        }
                    },
                    "sources": {
                        "/var/www/html": "https://s3.amazonaws.com/engelke/public/webcontent.zip"
                    },
                    "services": {
                        "sysvinit": {
                            "apache2": {
                                "enabled": "true",
                                "ensureRunning": "true"
                            }
                        }
                    },
                    "users": {
                        "dhbox": {
                            "groups": ["groupOne", "groupTwo"],
                            "uid": "50",
                            "homeDir": "/tmp"
                        }
                    },
                    "groups": {
                        "groupOne": {
                        },
                        "groupTwo": {
                            "gid": "45"
                        }
                    }
                }
            }
        }
    ),
]
cft.resources.add(Resource('MyInstance', 'AWS::EC2::Instance', properties, attributes))
