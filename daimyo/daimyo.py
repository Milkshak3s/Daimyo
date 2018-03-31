"""
The main file for the Daimyo project
Author: Chris Vantine
"""
from database.database import Database
#from daimyo.database.database import Database

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
    print("")


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
            print("Invalid input")

    else:
        print("Invalid input")


def menu():
    """
    Display and parse input for the main menu
    """
    print("==========")
    print("1. Keys")
    user_in = input("> ")

    if user_in == "1":
        keys()
    else:
        print("Invalid input")



def main():
    """
    The main function of the program
    """
    banner()
    while True:
        menu()


if __name__ == "__main__":
    main()