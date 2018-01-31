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

def create_user(db_state):
    """ Create a user account """
    if db_state is 1:
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous créer un utilisateur ? O/n ")
            if choice.upper() == "N":
                menu()
                break
            elif choice.upper() == "O":
                user_name = input("Nom d'utilisateur: ")
                newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
                user = newdb.request_db("INSERT INTO user (user_name) VALUES ('%s')" % user_name)
                if user is None:
                    print("Nom d'utilisateur créer, retour au menu...")
                else:
                    print("Utilisateur déjà enregistré, retour au menu...")
                time.sleep(3)
                menu()
                break
            else:
                choice = 0
    else:
        print("\nVeuillez créer la base de données, retour au menu...")
        time.sleep(3)
        menu()  

def access_sav():
    pass

def search_product(db_state, categories_count):
    """ Search a product in categories list """
    if db_state is 1:
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous rechercher un produit ? O/n ")
            if choice.upper() == "N":
                menu()
                break
            elif choice.upper() == "O":
                search_loop = 0
                while search_loop is 0:
                    categorie = input(
                        "\nEntrez le début du nom de la catégorie: ")
                    newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
                    results = newdb.search_db(str(categorie))
                    for number,item in enumerate(results):
                        print("{} - {}".format(number, item))
                    cat_choice = input("\nEntrez le numéro correspondant à votre recherche, tapez Q pour quitter ou n'import quel lettre pour relancer une recherche: ")
                    if cat_choice.upper() == "Q":
                        print("Retour au menu...")
                        time.sleep(3)
                        menu()
                        break
                    elif int(cat_choice) >= 0 and int(cat_choice) <= len(results):
                        newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
                        # Fonction non operationnelle, conception de la fonction database.product_db
                        # pour récupérer les produits

                    else:
                        continue
            else:
                choice = 0
    else:
        print("\nVeuillez créer la base de données, retour au menu...")
        time.sleep(3)
        menu()

def destroy_database():
    """ Option 4 - Delete the database """
    newdb = db.SqlRequest('', 'localhost', 'root', '')
    newdb.delete_db()
    print("\nBase de données effacée, retour au menu...")
    time.sleep(3)
    menu()

def create_database(db_state):
    """ Option 5 - Create the database and download the categories list """
    newdb = db.SqlRequest('', 'localhost', 'root', '')
    if db_state == 0:
        newdb.create_db()
        #print("")
        print("\nRetour au menu...")
        time.sleep(3)
        menu()
    else:
        #print("")
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
    
    if db_state is 1:
        # Get the user count
        newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
        user_count = newdb.request_db("SELECT COUNT(*) FROM user")
        user_count = user_count[0]
        # Get the categories count
        newdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')
        categories_count = newdb.request_db("SELECT COUNT(*) FROM categories")
        categories_count = categories_count[0]

        if user_count is 0:
            print("Veuillez créer un compte utilisateur pour pouvoir sauvegarder un produit")
        else:
            print("Il y a %s utilisateur(s) enregistré(s) dans la base de données." % user_count)
        print("La base de données possède actuellement %s categories" % categories_count)
    else:
        print("Il n'y a aucune base de données actuellement")

    print("*********************************************************************\n")
    print("Que voulez vous faire ?\n")
    print("1-Créer un compte utilisateur")
    print("2-Accédez à vos produits sauvegardés")
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
            create_user(db_state)
        elif int(choice) == 2:
            pass
        elif int(choice) == 3:
            search_product(db_state, categories_count)
        elif int(choice) == 4:
            destroy_database()
        elif int(choice) == 5:
            create_database(db_state)
            


"""x = urllib.request.urlopen('https://fr.openfoodfacts.org/categories.json')
print(x.read())"""


if __name__ == '__main__':
    menu()