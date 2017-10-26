import boto.ec2
from config import aws_access_key_id, aws_secret_access_key, \
    web_server_instance_id, benchmarking_instance_id, \
    web_server_ip, benchmarking_ip, key_pair


class BotoApi(object):
    key_pair_dir = './saved_key_pairs'

    ##intiate the connection
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.is_connect = False
        self.conn = False

    ##build the connection to AWS
    def connect(self, region_name):
        conn = boto.ec2.connect_to_region(region_name=region_name,
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_access_key
                                          )
        self.is_connect = True
        self.conn = conn
        return conn

    ##return all key pairs that are listed
    def get_all_key_pairs(self):
        key_pairs = self.conn.get_all_key_pairs()
        return key_pairs

    ##create a new key pair with name key_name
    def creat_key_pair(self, key_name):
        # Create Key-Pair
        key_pair = self.conn.create_key_pair(key_name)
        key_pair.save(BotoApi.key_pair_dir)
        print 'creat_key_pair', key_pair

    ##return the key pair with key_name
    def get_one_key_pair(self, key_name):
        rs = self.get_all_key_pairs()
        for i in rs:
            if i.name == key_name:
                print i
                return i

    ##create a new security group with name and description
    def create_security_group(self, name, description):
        security_group = self.conn.create_security_group(name, description)
        print security_group

    ##return all the security groups on the list
    def get_all_security_groups(self):
        rs = self.conn.get_all_security_groups()
        return rs

    ##get one specific group with name group_name
    def get_one_security_group(self, group_name):
        rs = self.get_all_security_groups()
        for group in rs:
            if group.name == group_name:
                return group

    ##allow a security group to use icmp server, ssh and http server
    def security_group_authorize(self, group_name):
        security_group = self.get_one_security_group(group_name)
        security_group.authorize('ICMP', -1, -1, '0.0.0.0/0')
        security_group.authorize('TCP', 22, 22, '0.0.0.0/0')
        security_group.authorize('TCP', 80, 80, '0.0.0.0/0')

    ##create an instance
    def run_instances(self, key_pair_name, group_name, image_id, instance_type):
        key_pair = self.get_one_key_pair(key_pair_name)

        ins = self.conn.run_instances(image_id=image_id,
                                       key_name=key_pair.name,
                                       instance_type=instance_type,
                                       security_groups=[group_name])

        print ins

    ##get an instance with instance_id
    def get_one_instance(self, instance_id):
        reservations = self.get_all_reservations()
        for i in reservations:
            if i.instances[0].id == instance_id:
                print i.instances[0]
                return i.instances[0]
        return None

    ##get all reservations on the list
    def get_all_reservations(self):
        test = self.conn.get_all_instances()
        print 'all ', test

        reservations = self.conn.get_all_reservations()
        print 'all ', reservations
        return reservations


    # TODO B3. Terminate V.S. Stop an instance

        # instances = reservations[1].instances
        # print instances,type(instances[0]), instances[0].instance_type, instances[0].placement
        # print instances[0].ip_address


        # print instances.ip_address
        # ssh -i yinhaoti.pem ubuntu@18.220.52.238
        pass

    ##allocate an elastic address from AWS
    def get_elastic_address(self):
        re = self.conn.allocate_address()
        print re

    ##check if the status of an instance is running
    def is_running(self, instance_id):
        instance = self.get_one_instance(instance_id)
        if instance.update() == "running":
            return True
        else:
            return False

    ##associate an instance with a pubic address
    def allocate_address(self, instance_id, public_address):
        if self.conn.associate_address(instance_id, public_address):
            print 'allocate ', instance_id, ' to ', public_address
        else:
            print 'allocate fail'

if __name__ == "__main__":
    # code to run a instance
    ins = BotoApi(aws_access_key_id, aws_secret_access_key)
    ins.connect('us-east-2')
    ins.creat_key_pair(key_pair)
    ins.create_security_group('csc326-group31', 'have a try')
    ins.run_instances(key_pair, 'csc326-group31', 'ami-c5062ba0', 't2.micro')





    # Below are some using examples

    # ins.get_all_key_pairs()
    # ins.get_all_security_groups()
    # ins.run_instances('yinhaoti', 'csc326-group31', 'ami-c5062ba0', 't2.micro')
    # print ins.is_running(web_server_instance_id)
    # ins.get_all_reservations(benchmarking_instance_id, benchmarking_ip)
    # ins.allocate_address(benchmarking_instance_id, benchmarking_ip)
    # ins.get_elastic_address()
    # ins.get_one_security_group('csc326-group31')
    # ins.security_group_authorize('csc326-group31')
    # ins.get_one_key_pair('yinhaoti')
    # ins.create_security_group('csc326-group31','have a try')

    # ab -n 1000 -c 20 http://ec2-18-216-49-43.us-east-2.compute.amazonaws.com/?keywords=helloworld+foo+bar

