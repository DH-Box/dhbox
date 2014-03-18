# to run: cfn_py_generate generator.py out.json
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
    "KeyName": "stevess",
    }

cft.parameters.add(Parameter('KeyName', 'String',
    {
      "Description" : "Name of an existing EC2 KeyPair to enable SSH access to the instances",
      "Type": "String",
      "MinLength": "1",
      "MaxLength": "255",
      "AllowedPattern" : "[\\x20-\\x7E]*",
      "ConstraintDescription" : "can contain only ASCII characters."
    })
)

cft.resources.add(Resource('MyEIP', 'AWS::EC2::EIP',
    {
     "InstanceId" : { "Ref" : "NewServer" }
     })
)

cft.outputs.add(Output('DnsName',
    get_att('NewServer', 'PublicDnsName'),
    'The public DNS Name for DH Box')
)

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
                            "homeDir": "/tmp"
                        }
                    },
                    "groups": {
                        "groupOne": {
                        },
                        "groupTwo": {
                        }
                    }
                }
            }
        }
    ),
]
cft.resources.add(Resource('NewServer', 'AWS::EC2::Instance', properties, attributes))
