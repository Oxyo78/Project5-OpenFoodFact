# ! /usr/bin/env python3
# coding: utf-8

''' Database connector
    Author : Yohan Vienne  V 0.1
'''

import pymysql.cursors

class SqlRequest:
    '''Communication with the SQL datbase.
       Create the class with database name, host address of the server,
       user name and password access'''

    def __init__(self, db_name, host_address, user_name, password):
        '''Class initialisator'''
        self.db_name = db_name
        self.host_address = host_address
        self.user_name = user_name
        self.password = password
        self.sql_message = ''

    def create_db(self):
        ''' Function to create the database'''

        try:
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            with open("database.txt", "r") as file:
                for line in file:
                    command = line.rstrip(";")
                    cursor.execute(command)
                    self.db_name.commit()

        except FileNotFoundError:
            print("Loading error of the file")

        finally:
            self.db_name.close()
            print("Base de donnees creer")

    def delete_db(self):
        '''Delete the database'''

        try:
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            cursor.execute("DROP DATABASE IF EXISTS DBOpenFoodFacts;")
            self.db_name.commit()

        finally:
            self.db_name.close()
            print("Base de donnees supprimer")

    def sql_request(self, request_db):
        '''Request to the database, this function return the answer if not null
           Add the SQL command in parameter when you call the function'''

        try:
            # Connect to the database
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            cursor.execute(request_db)
            self.db_name.commit()
            self.sql_message = cursor.fetchone()
            return self.sql_message

        finally:
            self.db_name.close()
            print('Requete SQL exécuter')


if __name__ == '__main__':
    db_insert = "INSERT INTO bd_off VALUES (NULL, 'Yohan2', 'url.com', '466');"

    newdb = SqlRequest('', 'localhost', 'root', '')
    newdb.delete_db()
    #print(resultat)
