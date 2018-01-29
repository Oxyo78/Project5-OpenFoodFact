# ! /usr/bin/env python3
# coding: utf-8

''' Database connector
    Author : Yohan Vienne  V 0.1
'''
import urllib.request
import json

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
        ''' Function to create and download the database'''

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
            print("Base de données créer")
            print("Chargement de la base de données...")

            # Get the french categorie database from OpenFoodFacts and add to the local database
            categories_url = urllib.request.urlopen('https://fr.openfoodfacts.org/categories.json')
            data = categories_url.read()
            json_output = json.loads(data.decode("utf_8"))

            # Change the type to str format, control len size and take of the langage prefixe(Cleaning file)
            for categorie in json_output["tags"]:
                cat_name = categorie['name']
                if (len(cat_name) >= 76) or (len(categorie['url']) >= 151):
                    continue
                if cat_name[2:3] == ":":
                    continue
                data = (cat_name, categorie['url'])

                # Insert into the categories table
                cursor.execute("INSERT IGNORE INTO categories (cat_name, cat_url) VALUES (%s, %s)", data)
                self.db_name.commit()

            # Get the total number of the categories table and print
            cursor.execute("SELECT COUNT(*) FROM categories")
            self.db_name.commit()
            self.sql_message = cursor.fetchone()
            print("Base de données chargé avec %s produits" % (self.sql_message))

        except Exception as e:
            print("Erreur : %s" % e)

    def delete_db(self):
        '''Delete the database'''

        try:
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            cursor.execute("DROP DATABASE IF EXISTS DBOpenFoodFacts;")
            self.db_name.commit()
            print("Base de données supprimer")

        except Exception as e:
            print("Erreur : %s" % e)

    def request_db(self, request_db):
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

        except Exception as e:
            print("Erreur : %s" % e)

    def check_db(self):
        """ Check if the database exist """
        state = 0
        try:
            # Connect to the database
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            database = ("SHOW DATABASES")
            cursor.execute(database)
            for database in cursor:
                database = database[0]
                if str(database) == "dbopenfoodfacts":
                    state = 1
                    break
                else:
                    state = 0
            return state

        except Exception as e:
            # Don't show the error if the doesn't exist
            pass

if __name__ == '__main__':
    # Test
    newdb = SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
    #resultat = newdb.check_db()
    resultat = newdb.request_db("SELECT COUNT(*) FROM user")
    resultat = resultat[0]
    print(resultat)
