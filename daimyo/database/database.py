"""
Database handler
Author: Chris Vantine
"""
from os.path import exists
import sqlite3


class Database(object):
    """
    Database handler object for SQLite abstraction
    """
    def __init__(self, location, script=None):
        """
        Create the database if it does not exist already
        :param location: the location of the SQLite database file
        """
        self.location = location
        ex = exists(location)
        self.conn = sqlite3.connect(location, check_same_thread=False)
        self.cur = self.conn.cursor()

        if not ex:
            print("Creating database...")
            self.create(script)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the connection when exiting the object
        """
        self.close()

    def close(self):
        """
        Close the connection
        """
        self.conn.close()

    def create(self, script=None):
        """
        Creates a new database
        :param script: the path to the sql script to run
        """
        self.location = "db_servers.sqlite"
        if script is None:
            script = "database/build_db.sql"

        fil = open(script)
        build_script = fil.read()
        fil.close()
        self.cur.executescript(build_script)
        self.conn.commit()

    def qry(self, qry):
        """
        Execute an arbitrary query
        """
        self.cur.execute(qry)
        return self.cur.fetchall()

    def add_key_aws(self, name, access_key, private_key, region):
        """
        Add an aws key to the database
        """
        qry = "INSERT INTO keys_aws('name', 'access', 'private', 'region') VALUES(?,?,?,?);"
        self.cur.execute(qry, (name, access_key, private_key, region))
        self.conn.commit()

    def get_key_aws(self, name):
        """
        Get an aws key by name
        """
        qry = "SELECT * FROM keys_aws WHERE name = ?"
        self.cur.execute(qry, (name,))
        return self.cur.fetchall()

    def get_all_key_aws(self):
        """
        Get a list of ALL aws keys in the database
        """
        qry = "SELECT * FROM keys_aws"
        self.cur.execute(qry, ())
        results = self.cur.fetchall()

        new_results = []
        for item in results:
            new_results += [item]

        return new_results

    def add_key_vsphere(self, name, ip_address, username, password):
        """
        Add a set of vsphere credentials to the database
        """
        qry = "INSERT INTO keys_vsphere('name', 'ip', 'username', 'password') VALUES(?,?,?,?);"
        self.cur.execute(qry, (name, ip_address, username, password))
        self.conn.commit()

    def get_key_vsphere(self, name):
        """
        Get a vsphere credential set by name
        """
        qry = "SELECT * FROM keys_vsphere WHERE name = ?"
        self.cur.execute(qry, (name,))
        return self.cur.fetchall()

    def get_all_key_vsphere(self):
        """
        Get a list of ALL vsphere creds in the database
        """
        qry = "SELECT * FROM keys_vsphere"
        self.cur.execute(qry, ())
        results = self.cur.fetchall()

        new_results = []
        for item in results:
            new_results += [item]

        return new_results
