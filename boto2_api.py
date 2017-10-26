import boto.ec2

from config import IAM_AWS_access_key_id, IAM_AWS_secret_access_key, \
    web_server_instance_id, benchmarking_instance_id, \
    web_server_ip, benchmarking_ip, key_pair


class BotoApi(object):
    key_pair_dir = './saved_key_pairs'

    # Initiate the connection
    def __init__(self, IAM_AWS_access_key_id, IAM_AWS_secret_access_key):
        self.IAM_AWS_access_key_id = IAM_AWS_access_key_id
        self.IAM_AWS_secret_access_key = IAM_AWS_secret_access_key
        self.is_connect = False
        self.conn = False

    # Build the connection to AWS
    def connect(self, region_name):
        conn = boto.ec2.connect_to_region(region_name=region_name,
                                          aws_access_key_id=IAM_AWS_access_key_id,
                                          aws_secret_access_key=IAM_AWS_secret_access_key
                                          )
        self.is_connect = True
        self.conn = conn
        return conn

    # Return all key pairs that are listed
    def get_all_key_pairs(self):
        key_pairs = self.conn.get_all_key_pairs()
        return key_pairs

    # Create a new key pair with name key_name
    def creat_key_pair(self, key_name):
        # Create Key-Pair
        key_pair = self.conn.create_key_pair(key_name)
        key_pair.save(BotoApi.key_pair_dir)
        print 'creat_key_pair', key_pair

    # Return the key pair with key_name
    def get_one_key_pair(self, key_name):
        rs = self.get_all_key_pairs()
        for i in rs:
            if i.name == key_name:
                print i
                return i

    # Create a new security group with name and description
    def create_security_group(self, name, description):
        security_group = self.conn.create_security_group(name, description)
        print security_group

    # Return all the security groups on the list
    def get_all_security_groups(self):
        rs = self.conn.get_all_security_groups()
        return rs

    # Get one specific group with name group_name
    def get_one_security_group(self, group_name):
        rs = self.get_all_security_groups()
        for group in rs:
            if group.name == group_name:
                return group

    # Allow a security group to use icmp server, ssh and http server
    def security_group_authorize(self, group_name):
        security_group = self.get_one_security_group(group_name)
        security_group.authorize('ICMP', -1, -1, '0.0.0.0/0')
        security_group.authorize('TCP', 22, 22, '0.0.0.0/0')
        security_group.authorize('TCP', 80, 80, '0.0.0.0/0')

    # Create an instance
    def run_instances(self, key_pair_name, group_name, image_id, instance_type):
        key_pair = self.get_one_key_pair(key_pair_name)

        ins = self.conn.run_instances(image_id=image_id,
                                       key_name=key_pair.name,
                                       instance_type=instance_type,
                                       security_groups=[group_name]
                                      )

        print ins

    # Get an instance with instance_id
    def get_one_instance(self, instance_id):
        reservations = self.get_all_reservations()
        for i in reservations:
            if i.instances[0].id == instance_id:
                print i.instances[0]
                return i.instances[0]
        return None

    # Get one instance's attribute
    def get_one_instance_attribute(self,instance_id, attribute_name):
        ins = self.get_one_instance(instance_id)
        print ins.get_attribute(attribute_name)
        return ins.get_attribute(attribute_name)

    def is_instance_with_EBS_block(self, instance_id):
        re = ins.get_one_instance_attribute(instance_id, 'rootDeviceName')
        if re['rootDeviceName'] == '/dev/xvda':
            print 'yes, it is'
            return True
        return False

    # Get all reservations on the list
    def get_all_reservations(self):
        test = self.conn.get_all_instances()
        print 'all ', test

        reservations = self.conn.get_all_reservations()
        print 'all ', reservations
        return reservations

    # Stop a instance
    def stop_instance(self, instance_ids):
        # instance_ids=['instance-id-1', 'instance-id-2', ...]
        self.conn.stop_instances(instance_ids=instance_ids)


    # Terminate a instance
    def terminate_instance(self, instance_ids):
        # instance_ids=['instance-id-1', 'instance-id-2', ...]
        self.conn.terminate_instances(instance_ids=instance_ids)

    # get a elastic address and associate it to a instance
    def get_elastic_address_and_allocate(self, instance_id):
        re = self.conn.allocate_address()
        re.associate(instance_id= instance_id)
        print re

    # check if the status of an instance is running
    def is_running(self, instance_id):
        instance = self.get_one_instance(instance_id)
        if instance.update() == "running":
            return True
        else:
            return False


if __name__ == "__main__":
    # code to run a instance
    ins = BotoApi(IAM_AWS_access_key_id, IAM_AWS_secret_access_key)
    ins.connect(region_name = 'us-east-2')
    # ins.security_group_authorize('yinhaoti group')
    # ins.creat_key_pair('yinhaoti')
    # ins.create_security_group("yinhaoti group", 'first use')
    # ins.run_instances(key_pair, 'yinhaoti group', 'ami-c5062ba0', 't2.micro')

    # Associate a Static IP
    # ins.get_elastic_address_and_allocate(web_server_instance_id)

    # terminate or stop a instance
    # check if it's a EBS Block
    # if ins.is_instance_with_EBS_block('i-06875de131d39eea8'):
    #     ins.stop_instance(['i-0eac41551c0dbd94b'])
    #     ins.terminate_instance(['i-06875de131d39eea8'])




    # Below are some using examples


    # ins.get_all_key_pairs()
    # ins.get_all_security_groups()
    # ins.run_instances('yinhaoti', 'csc326-group31', 'ami-c5062ba0', 't2.micro')
    # print ins.is_running(web_server_instance_id)
    # ins.get_all_reservations(benchmarking_instance_id, benchmarking_ip)
    # ins.allocate_address(benchmarking_instance_id, benchmarking_ip)
    # ins.get_elastic_address_and_allocate(web_server_instance_id)
    # ins.get_one_security_group('csc326-group31')
    # ins.security_group_authorize('csc326-group31')
    # ins.get_one_key_pair('wynn')
    # ins.create_security_group('csc326-group31','have a try')

    # conn = boto.ec2.connect_to_region("us-west-2")
    # conn.run_instances(image_id=image_id,
    #                    key_name=key_pair.name,
    #                    instance_type=instance_type,
    #                    security_groups=[group_name])
    #
    #


    # ssh -i yinhaoti.pem root@18.216.120.1

    # ssh -i "yinhaoti.pem" ec2-user@ec2-18-216-120-1.us-east-2.compute.amazonaws.com

    # ab -n 1000 -c 20 http://ec2-18-216-49-43.us-east-2.compute.amazonaws.com/?keywords=helloworld+foo+bar

    # scp -i key_pair.pem <FILE-PATH> ubuntu@<PUBLIC-IP-ADDRESS>:~/<REMOTE-PATH>