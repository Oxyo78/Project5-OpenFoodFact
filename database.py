# ! /usr/bin/env python3
# coding: utf-8

''' Database connector
    Author : Yohan Vienne  V 0.1
'''

import pymysql.cursors

class SqlRequest:
    '''Execute some request to the SQL datbase.
       Create the class with database name, host address of the server,
       user name and password access'''

    def __init__(self, db_name, host_address, user_name, password):
        '''Class initialisator'''
        self.db_name = db_name
        self.host_address = host_address
        self.user_name = user_name
        self.password = password
        self.sql_message = ''

    def sql_execute(self, execute_line):
        ''' Function to execute a request to the database'''

        try:
            # Connect to the database
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           charset='utf8')
            cursor = self.db_name.cursor()
            cursor.execute(execute_line)
            self.db_name.commit()

        finally:
            self.db_name.close()
            print("Commande executer")


    def sql_get_answer(self, request_db):
        '''Ask to the database, this function return the answer'''

        try:
            # Connect to the database
            self.db_name = pymysql.connect(host=self.host_address,
                                           user=self.user_name, password=self.password,
                                           charset='utf8')
            cursor = self.db_name.cursor()
            cursor.execute(request_db)
            self.sql_message = cursor.fetchone()
            return self.sql_message

        finally:
            self.db_name.close()


if __name__ == '__main__':
    import os
    sql = '''CREATE SCHEMA IF NOT EXISTS `DBOpenFoodFacts` DEFAULT CHARACTER SET utf8;
             USE `DBOpenFoodFacts`;
             CREATE TABLE IF NOT EXISTS `DBOpenFoodFacts`.`BD_OFF` (`OFF_id` INT NOT NULL AUTO_INCREMENT,
                                                                   `OFF_name` VARCHAR(45) NOT NULL,
                                                                   `OFF_url` VARCHAR(150) NOT NULL,
                                                                   `OFF_product` INT NOT NULL,
                                                                   PRIMARY KEY(`OFF_id`, `OFF_product`),
                                                                   UNIQUE INDEX `OFF_product_UNIQUE` (`OFF_product` ASC));
          ENGINE = InnoDB'''
    newdb = SqlRequest('', 'localhost', 'root', '')
    newdb.sql_execute(sql)
    os.system('PAUSE')
