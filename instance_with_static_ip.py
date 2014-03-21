import boto.ec2
# from util import aws_conf

conn = boto.ec2.connect_to_region('us-east-1')
info = {}
def _create_interface(domain='vpc', public=False,
                      subnet=None, groups=None,
                      description=None, index=0):

    eni = conn.create_network_interface(subnet, groups=groups, description=description)
    info['private_ip_address'] = eni.private_ip_address

    if public:
        eip = conn.allocate_address(domain='vpc')
        aa = conn.associate_address(allocation_id=eip.allocation_id, network_interface_id=eni.id)
        info['public_ip_address'] = eip.public_ip

    interface = boto.ec2.networkinterface.NetworkInterfaceSpecification()
    interface.network_interface_id=eni.id
    interface.device_index=index
    interface.description=description

    return interface
def _create_instance(ami=None, key=None,
                     user_data=None, _type='t1.micro',
                     ifaces=None):
    i = conn.run_instances(ami,
                           key_name=key,
                           user_data=user_data,
                           instance_type=_type,
                           network_interfaces=ifaces)
    info['Instance'] = i.instances[0].id
    return info

eth0 = _create_interface(domain='vpc', public=True,
                         subnet='subnet-28604231', groups=['default'],
                         description='TESTING', index=0)

_create_instance(ami='ami-032b416a', key='stevess', ifaces=eth0)