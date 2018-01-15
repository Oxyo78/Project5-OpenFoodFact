''' Build the Mysql database
    V.0.1
    Author : Yohan Vienne
'''
# ! /usr/bin/env python3
# coding: utf-8

import pymysql.cursors

def new_dtb():
    ''' Function to create the database'''

    #sql = "CREATE SCHEMA IF NOT EXISTS `DBOpenFoodFacts` DEFAULT CHARACTER SET utf8"

    # Connect to the database
    db = pymysql.connect(host='localhost', user='root', password='', charset='utf8')


    # Open database connection
    #db = PyMySQL.connect("localhost", "testuser", "test123", "TESTDB")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

    # Create table as per requirement
    """sql = CREATE TABLE EMPLOYEE (
    FIRST_NAME  CHAR(20) NOT NULL,
    LAST_NAME  CHAR(20),
    AGE INT,  
    SEX CHAR(1),
    INCOME FLOAT )"""

    cursor.execute(sql)

    # disconnect from server
    db.close()

    """ try:
        with connection.cursor() as cursor:
            # Create the database
            for line in sql:
        cursor.execute(sql)
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM dbopenfoodfacts"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
        #print("Base de donnees creer")"""

if __name__ == '__main__':
    import os
    new_dtb()
    os.system("PAUSE")
