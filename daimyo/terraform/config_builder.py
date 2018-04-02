"""
Terraform configuration file constructor
Author: Chris Vantine
"""
import json


class ConfigBuilder:
    """
    Object for constructing terraform files
    """
    def __init__(self, location):
        """
        Initialize the file builder, write a blank terraform template json block to the file
        :param location: the path to the terraform file
        """
        self.file = open(location, "w+")
        self.data = {'provider':[], 'data':[], 'resource':[]}
        self.update_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the file when exiting"""
        self.close()

    def close(self):
        """Close the file"""
        self.file.close()

    def update_file(self):
        """Write the current json data set to the file"""
        self.file.seek(0)
        json.dump(self.data, self.file, indent=4)
        self.file.truncate()
        self.file.seek(0)
        self.data = json.load(self.file)

    def add_provider_aws(self, name, access_key, private_key, region):
        """
        Add an aws provider block to the config
        :param name: the alias for the set of keys
        :param access_key: the target aws access key
        :param private_key: the target aws private key
        :param region: the target aws region
        """
        self.data['provider'] += [{'aws':{'alias':name,
                                          'access_key':access_key,
                                          'private_key':private_key,
                                          'region':region}}]

    def add_provider_vsphere(self, name, ip_address, username, password):
        """
        Add a vsphere provider block to the config
        :param name: the alias for the set of credentials
        :param ip_address: location of target vSphere instance
        :param username: target username
        :param password: target password
        :return:
        """
        self.data['provider'] += [{'vsphere':{'alias':name,
                                              'ip':ip_address,
                                              'username':username,
                                              'password':password}}]

    def add_resource_aws_ec2(self, name, ami, instance_type):
        """
        Add an ec2 resource block to the config
        :param name: the alias for the instance
        :param ami: the amazon image code to install
        :param instance_type: the aws type/size of ec2 instance
        """
        self.data['resource'] += [{'aws_instance':{name:{'ami':ami,
                                                         'instance_type':instance_type}}}]
