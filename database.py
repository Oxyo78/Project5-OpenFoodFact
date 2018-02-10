# ! /usr/bin/env python3
# coding: utf-8

''' Database connector
    Author : Yohan Vienne  V 0.3
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

    def create_db(self, filename):
        ''' Function to create and download the database'''

        try:
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            # Open SQL file
            with open(filename, 'r') as fileToRead:
                sqlFile = fileToRead.read()

            # split all command by ';'
            sqlCommand = sqlFile.split(';')

            # Execute each command in sqlcommand
            for command in sqlCommand:
                try:
                    if command.strip() != '':
                        cursor.execute(command)
                except pymysql.err.InternalError as msg:
                        print("Erreur: {}".format(msg))
            print("\nBase de données créer")
            print("\nChargement de la base de données...")

            # Get the french categorie database from OpenFoodFacts and add to the local database
            categories_url = urllib.request.urlopen('https://fr.openfoodfacts.org/categories.json')
            data = categories_url.read()
            json_output = json.loads(data.decode("utf_8"))

            # Change the type to str format, control len size and take of the langage prefixe(Cleaning file)
            for categorie in json_output["tags"]:
                cat_name = categorie['name']
                cat_name = cat_name.replace("'", " ")
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
        
        finally:
            self.db_name.close()

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
        
        finally:
            self.db_name.close()

    def request_db(self, request_db, multi_result = False):
        '''Request to the database, this function return the answer if not null
           Add the SQL command in parameter, use multi_result=True for a list answer 
           (by default False => single answer)'''
        self.sql_message = ''
        try:
            # Connect to the database
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')
            cursor = self.db_name.cursor()
            cursor.execute(request_db)
            self.db_name.commit()
            if multi_result is True:
                self.sql_message = [item for item in cursor.fetchall()]
            else:
                self.sql_message = cursor.fetchone()
                self.sql_message = self.sql_message[0]
            return self.sql_message

        except Exception as e:
            return e

        finally:
            self.db_name.close()

    def check_db(self):
        """ Check if the database exist """
        state = False
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
                state = True
                break
            else:
                state = False
        self.db_name.close()
        return state

    def cat_search_db(self, name_search):
        """ Return a search of 10 items """
        self.db_name = pymysql.connect(host=self.host_address,
                                    user=self.user_name, password=self.password,
                                    database=self.db_name, charset='utf8')
        cursor = self.db_name.cursor()
        result = ("SELECT cat_name FROM categories WHERE cat_name LIKE '{}%' LIMIT 10".format(name_search))
        cursor.execute(result)
        results = [item[0] for item in cursor.fetchall()]
        self.db_name.close()
        return results

    def product_show_db(self):
        """ Show the product table """
        results = list()
        self.db_name = pymysql.connect(host=self.host_address,
                                       user=self.user_name, password=self.password,
                                       database=self.db_name, charset='utf8')
        cursor = self.db_name.cursor()
        request = ("""SELECT pro_id, pro_name FROM product ORDER BY pro_id""")
        cursor.execute(request)
        results = [item for item in cursor.fetchall()]
        self.db_name.close()
        return results
    
    def product_db(self, categorie_name):
        """ Get the product list from the categorie """
        try:
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           database=self.db_name, charset='utf8')

            cursor = self.db_name.cursor()
            # Get the product list from the selected categorie
            cursor.execute("SELECT cat_url, cat_id FROM categories WHERE cat_name LIKE '{}'".format(categorie_name))
            result = cursor.fetchone()
            url_product_list, cat_product_list = result
            url_product_list += ".json"
            product_url = urllib.request.urlopen(url_product_list)
            data = product_url.read()
            json_output = json.loads(data.decode("utf_8"))

            # Get information from the product list
            for product in json_output['products']:
                if len(product['product_name_fr']) > 76:
                    continue
                product_name = product['product_name_fr']
                product_name = product_name.replace("'", ' ')
                if 'stores' in product:
                    product_shop = str(product['stores'])
                    product_shop = product_shop.replace(' ', '-')
                    if product_shop is "":
                        product_shop = ("Inconnu")
                else:
                    product_shop = ("Inconnu")
                product_url = product['url']
                nutr_sco = product['nutrition_score_debug']
                # Try id the nutrition score number if decade number
                try:
                    int(nutr_sco[len(nutr_sco)-2])
                    nutrition_score = nutr_sco[len(nutr_sco)-2]+nutr_sco[len(nutr_sco)-1]
                except:
                    nutrition_score = nutr_sco[len(nutr_sco)-1]
                if nutrition_score.isdigit() is True:    
                    nutrition_score = int(nutrition_score)
                else:
                    nutrition_score = 0
                # Insert into the categories table
                cursor.execute("""INSERT INTO product 
                    (pro_name, pro_shop, pro_url, pro_nutriscore, pro_cat_id) 
                    VALUES ('%s', '%s', '%s', %d, %d) 
                    ON DUPLICATE KEY UPDATE pro_name = '%s'""" % 
                    (product_name, product_shop, product_url, nutrition_score, cat_product_list, product_name))
                self.db_name.commit()
                
        except Exception as e:
            print("Erreur : %s" % e)

        finally:
            self.db_name.close()

if __name__ == '__main__':
    # Test
    newdb = SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
    #resultat = newdb.request_db("SELECT pro_name FROM product", True)
    resultat = newdb.create_db('database.sql')
    #resultat = newdb.product_db("Boissons")
    #resultat = resultat[0]
    print(resultat)
    #print(resultat[0][0])
    #print(type(resultat))
