"""
The main file for the Daimyo project
Author: Chris Vantine
"""
from database.database import Database
from terraform.config_builder import ConfigBuilder
import os

# the database
sql_database = Database("db_servers.sqlite")


def banner():
    """
    Display the ascii banner
    """
    print("8888888b.           d8b")
    print("888  \"Y88b          Y8P")
    print("888    888")
    print("888    888  8888b.  888 88888b.d88b.  888  888  .d88b.")
    print("888    888     \"88b 888 888 \"888 \"88b 888  888 d88\"\"88b ")
    print("888    888 .d888888 888 888  888  888 888  888 888  888")
    print("888  .d88P 888  888 888 888  888  888 Y88b 888 Y88..88P")
    print("8888888P"  "Y888888 888 888  888  888  \"Y88888  \"Y88P\"")
    print("                                           888")
    print("                                      Y8b d88P")
    print("                                       \"Y88P\"")


def keys():
    """
    User interface for adding keys to the database
    """
    print("----------")
    print("1. AWS")
    print("2. vSphere")
    user_in = input("> ")

    if user_in == "1":
        print("---------")
        print("1. List keys")
        print("2. Add key")
        user_in = input("> ")

        if user_in == "1":
            print(sql_database.get_all_key_aws())
        elif user_in == "2":
            name = input("Set name: ")
            access_key = input("Access key: ")
            private_key = input("Private key: ")
            region = input("Region: ")

            sql_database.add_key_aws(name, access_key, private_key, region)
            print("Key added to database!")
        else:
            print("Invalid input")

    elif user_in == "2":
        print("")
        print("---------")
        print("1. List creds")
        print("2. Add creds")
        user_in = input("> ")

        if user_in == "1":
            print(sql_database.get_all_key_vsphere())
        elif user_in == "2":
            name = input("Set name: ")
            ip_address = input("IP Address: ")
            username = input("Username: ")
            password = input("Password: ")

            sql_database.add_key_vsphere(name, ip_address, username, password)
            print("Creds added to database!")
        else:
            print("Error: Invalid input")

    else:
        print("Error: Invalid input")


def build_config():
    """
    User interface for building a terraform config
    """
    # print banner
    print("")
    print("=====================================")
    print("||         BUILD-A-CONFIG          ||")
    print("||  terraform config constructor   ||")
    print("=====================================")

    # initialize new config file
    user_in = input("Config directory: ")
    if not os.path.exists(user_in):
        os.makedirs(user_in)
    filename = user_in + "/build.tf.json"
    config_builder = ConfigBuilder(filename)

    # build keys list, return early if no keys exists
    aws_keys_list = sql_database.get_all_key_aws()
    vsphere_keys_list = sql_database.get_all_key_vsphere()
    all_keys_list = []

    # each entry in all_keys_list is a tuple, with provider identifier string and name of key
    if len(aws_keys_list) == 0 and len(vsphere_keys_list) == 0:
        print("Error, no keys in database")
        return
    else:
        for key in aws_keys_list:
            all_keys_list += [('aws', key[0])]
        for key in vsphere_keys_list:
            all_keys_list += [('vsphere', key[0])]

    # print a list of usable keys in the database
    print("KEYS:")
    i = 0
    for key in all_keys_list:
        print(str(i) + ". (" + key[0] + ") " + key[1])
        i = i + 1
    print("")

    # handle user key selection
    sentinel = 0
    while sentinel == 0:
        user_in = int(input("Select a key to use ('-1' to continue): "))
        if user_in > i:
            print("Error: selection out of bounds")
        elif user_in == -1:
            sentinel = 1
        else:
            if all_keys_list[user_in][0] == 'aws':
                key = sql_database.get_key_aws(all_keys_list[user_in][1])
                key = key[0]
                config_builder.add_provider_aws(key[0], key[1], key [2], key[3])
                print("Key added: " + str(key))
            elif all_keys_list[user_in][0] == 'vsphere':
                key = sql_database.get_key_vsphere(all_keys_list[user_in][1])
                config_builder.add_provider_vsphere(key[0], key[1], key[2], key[3])
                print("Key added: " + str(key))
            else:
                print("FATAL_ERROR: key in database of unknown provider type")

    # print resource list
    print("")
    print("1. AWS")
    print("2. vSphere")
    print("")

    # handle user resource configuration
    sentinel = 0
    while sentinel == 0:
        user_in = input("Select a provider ('-1' to continue): ")
        if user_in == '-1':
            sentinel = 1
        elif user_in == '1':
            print("AWS")
            name = input("Resource name: ")
            ami = input("AMI: ")
            instance_type = input("Instance type: ")
            config_builder.add_resource_aws_ec2(name, ami, instance_type)
            print("Resource added: ")
            print("\tName:\t\t\t" + name)
            print("\tAMI:\t\t\t" + ami)
            print("\tInstance Type:\t" + instance_type)
        elif user_in == '2':
            print("vSphere")
            name = input("Resource name: ")
        else:
            print("Error: invalid selection")

    # update, then close the file
    print("[i] Writing to file....")
    config_builder.update_file()
    config_builder.close()
    print("[+] Config file built!")
    print("")
    print("Config Builder complete! New terraform config at " + filename)


def terraform_manager():
    """
    User interface for managing a terraform instance
    """


def menu():
    """
    Display and parse input for the main menu
    """
    print("")
    print("==========")
    print("1. Keys")
    print("2. Build TF Config")
    print("3. Terraform Manager")
    user_in = input("> ")

    if user_in == "1":
        keys()
    elif user_in == "2":
        build_config()
    else:
        print("Error: Invalid input")


def main():
    """
    The main function of the program
    """
    banner()
    while True:
        menu()


if __name__ == "__main__":
    main()
