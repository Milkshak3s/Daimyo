"""
The main file for the Daimyo project
Author: Chris Vantine
"""
from database.database import Database


def main():
    """
    The main function of the program
    """
    sql_database = Database("db_servers.sqlite", "database/build_db.sql")
    sql_database.add_key_aws("test_key", "f4dasf15fasdf", "dsa418as6dsa15", "us-east-1")
    sql_database.add_key_vsphere("test_key2", "10.80.100.14", "terraform_user", "GoodPass")
    print(sql_database.get_key_aws("test_key"))
    print(sql_database.get_key_vsphere("test_key2"))


if __name__ == "__main__":
    main()