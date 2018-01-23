''' Project 5 - OpenFoodFacts
    Author : Yohan Vienne

    This application get the select product in the Json API from OpenFoodFacts.com to print the console.
    
    Install the requirements.txt to get the packages for this script.

'''
import urllib.request
import json
import database

x = urllib.request.urlopen('https://fr.openfoodfacts.org/categories.json')
print(x.read())


if __name__ == '__main__':
    db = database.SqlRequest('', 'localhost', 'root', '')
    db.delete_db()
