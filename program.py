''' Project 5 - OpenFoodFacts
    Author : Yohan Vienne

    This application get the select product in the Json API from OpenFoodFacts.com to show in a window app.
    
    Install the requirements.txt to get the packages for this script.

'''
import urllib.request
import json
import os
import sys
import time

import database as db


def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "Linux":
        os.system("clear")

def create_user():
    """ Create a user account """
    pass

def access_sav():
    pass

def search_product():
    pass

def destroy_database():
    pass

def create_database(db_state):
    """ Option 5 - Create the database and download the categories list """
    newdb = db.SqlRequest('', 'localhost', 'root', '')
    if db_state == 0:
        print("")
        newdb.create_db()
        print("Retour au menu...")
        time.sleep(3)
        menu()
    else:
        print("\nLa base de données existe déja, retour au menu...")
        time.sleep(3)
        menu()

def menu():
    """ Main screen of application """
    choice = 0

    # Check if the database exist
    newdb = db.SqlRequest('', 'localhost', 'root', '')
    db_state = newdb.check_db()
    # Clear prompt
    clear_prompt()
    print("\nBienvenue sur la base de données OpenFoodFacts FR.")
    print("")
    
    # Get the User table count
    if db_state == 1:
        newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
        user = newdb.request_db("SELECT COUNT(*) FROM user")
        user = user[0]
        if user == 0:
            print("Veuillez créer un compte utilisateur pour pouvoir sauvegarder un produit")
        else:
            print("Il y a %s utilisateur(s) enregistrer dans la base de données." % user)
    else:
        print("Il n'y a aucune base de données actuellement")

    print("*********************************************************************\n")
    print("Que voulez vous faire ?\n")
    print("1-Créer un compte utilisateur")
    print("2-Accédez a vos produits sauvegarder")
    print("3-Rechercher un produit dans la listes des catégories")
    print("4-Effacer la base de données actuelle")
    print("5-Créer la base de données locale")
    while choice == 0:
        choice = input("Votre choix (Tapez Q pour quitter): ")
        # Stop the program
        if choice.upper() == "Q":
            break
        # Check if the input is a digit and between 0 and 6
        elif choice.isdigit() == False or int(choice) >= 6 or int(choice) == 0:
            print("\nVous devez entrer un nombre entre 1 et 5\n")
            choice = 0
        # Run the input choice
        elif int(choice) == 1:
            pass
        elif int(choice) == 2:
            pass
        elif int(choice) == 3:
            pass
        elif int(choice) == 4:
            pass
        elif int(choice) == 5:
            create_database(db_state)
            


"""x = urllib.request.urlopen('https://fr.openfoodfacts.org/categories.json')
print(x.read())"""


if __name__ == '__main__':
    #newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
    menu()
