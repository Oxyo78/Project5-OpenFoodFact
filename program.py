''' Project 5 - OpenFoodFacts
    Author : Yohan Vienne
    V 0.3

    This application get the select product in the Json API from OpenFoodFacts.com to show in a window app.
    
    Install the requirements.txt to get the packages for this script.

'''
import urllib.request
import json
import os
import sys
import time

import database as db

program_loop = True

# Creation of SQL connector
newdb = db.SqlRequest('', 'localhost', 'root', '')
conecdb = db.SqlRequest('dbopenfoodfacts', 'localhost', 'root', '')

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "Linux":
        os.system("clear")

def create_user(db_state):
    """ Create a user account """
    if db_state is True:
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous créer un utilisateur ? O/n ")
            if choice.upper() == "N":
                break
            elif choice.upper() == "O":
                user_name = input("Nom d'utilisateur: ")
                # Request to the DB
                user = conecdb.request_db(
                    "INSERT INTO user (user_name) VALUES ('%s')" % user_name, True)
                if not user:
                    print("Nom d'utilisateur créer, retour au menu...")
                else:
                    print("Utilisateur déjà enregistré, retour au menu...")
                time.sleep(2)
                break
            else:
                choice = 0
    else:
        print("\nVeuillez créer la base de données, retour au menu...")
        time.sleep(2)

def access_sav(db_state, user_count):
    """Show the saved product in saved table """
    if db_state is True:
        if user_count is not 0:
            choice = 0
            while choice is 0:
                # Request to the DB
                user_list = conecdb.request_db(
                    "SELECT * FROM user ORDER BY user_id", True)
                choice = input("\nVoulez vous afficher les produits sauvegardés ? O/n ")
                if choice.upper() == "N":
                    break
                elif choice.upper() == "O":
                    user_choice = 0
                    user_id = []
                    while user_choice is 0:
                        print("\nVoici le(s) utilisateur(s) enregistré\n")
                        for num, user in user_list:
                            print("{} - {}".format(num, user))
                            user_id.append(num)
                        user_choice = input("\nSélectionné l'utilisateur à afficher: ")
                        if user_choice.isdigit():
                            if int(user_choice) in user_id:
                                # Request to the DB
                                user_sav = conecdb.request_db("""SELECT categories.cat_name, saved.sav_name, saved.sav_shop, saved.sav_url, saved.sav_nutriscore
                                                        FROM categories INNER JOIN saved
                                                        ON saved.sav_cat_id=categories.cat_id
                                                        WHERE saved.sav_user_id = {}""".format(user_choice), True)
                                # If user doesn't have saved product
                                if not user_sav:
                                    print("Cet utilisateur n'a aucun produit sauvegardé, retour au menu...")
                                    time.sleep(2)
                                # Print the result of the user saved
                                product_count = 1
                                for item in user_sav:
                                    print("\n*****************************************")
                                    print("Produit {}:".format(product_count))
                                    print("Le produit {} appartient à la catégorie {}.".format(
                                        item[1], item[0]))
                                    if item[2] == "Inconnu":
                                        print("Il n'y a pas de magasin connu pour ce produit")
                                    else:
                                        print("On peut trouver ce produit chez {}".format(item[2]))
                                    print("Voici le lien URL du produit: {}".format(item[3]))
                                    print("*****************************************")
                                    product_count += 1
                                show_substitute = 0
                                while show_substitute is 0:
                                    show_substitute = input("Voulez vous afficher le substitut d'un produit ? O/n ")
                                    if show_substitute.upper() == "O":
                                        product = input("Veuillez entrer le numéro du produit à substituer: ")
                                        if int(product) >= 1 and int(product) <= product_count:
                                            print(
                                                "Chargement de la liste des produits correspondant...")
                                            conecdb.request_db(
                                                "TRUNCATE product")
                                            conecdb.product_db(
                                                user_sav[int(product) - 1][0])
                                            nutriscore_list = conecdb.request_db(
                                                """SELECT product.pro_name, product.pro_nutriscore 
                                                FROM product 
                                                WHERE product.pro_nutriscore > {} """.format(user_sav[int(product)-1][4]), True)
                                            print("\n*****************************************\n")
                                            for name, nutriscore in nutriscore_list:
                                                print("Le produit {} a un meilleur score nutritionnel avec un score de {}.".format(name, nutriscore))
                                            print("Appuyez sur une touche pour revenir au menu...")
                                            break_time = os.popen("pause")
                                            break_time.read()
                                        else: 
                                            print("Choix incorrect")
                                            show_substitute = 0
                                    elif show_substitute.upper() == "N":
                                        break
                                    else:
                                        print("\nChoix incorrect, veuillez entrer O(Oui) ou N(Non) ")
                                        show_substitute = 0
                            else:
                                print("\nChoix incorrect ")
                                choice = 0
                        else:
                            print("\nChoix incorrect, veuillez entrer un chiffre correspondant à la liste\n")
                            time.sleep(2)
                            user_choice = 0
                else:
                    choice = 0
        else:
            print("Il n'y a aucun utilisateur enregistré, retour au menu...")
            time.sleep(2)
    else:
        print("\nIl n'y a pas de base de données créer, retour au menu...")
        time.sleep(2)

def search_product(db_state, user_count):
    """ Search a product in categories list """
    # If the DB exist
    if db_state is True:
        choice = 0
        while choice is 0:

            # Check count of user in DB
            if user_count is 0:
                print("\nAttention ! Il n'y a pas de compte utilisateur créer pour sauvegarder")
            choice = input("\nVoulez vous rechercher un produit ? O/n ")
            if choice.upper() == "N":
                break
            elif choice.upper() == "O":
                search_loop = 0
                while search_loop is 0:
                    categorie = input("\nEntrez le début du nom de la catégorie: ")
                    print("")

                    # Request to the DB
                    results = conecdb.cat_search_db(str(categorie))
                    if len(results) == 0 :
                            print("Aucun résultat")
                            continue
                    for number, item in enumerate(results):
                        print("{} - {}".format(number, item))
                    print("\nEntrez le numéro correspondant à votre recherche,")
                    cat_choice = input("Tapez Q pour quitter ou n'importe quel lettre pour relancer une recherche: ")
                    if cat_choice.isdigit():
                        if int(cat_choice) >= 0 and int(cat_choice) < 10:

                            # Request to the DB
                            conecdb.request_db("TRUNCATE product")
                            print("Chargement des résultats...")

                            # Request to the DB
                            conecdb.product_db(results[int(cat_choice)])
                        else:
                            print("\nChoix du chiffre incorrect, retour à la recherche...\n")
                            time.sleep(2)
                            continue
                    else:
                        if cat_choice.upper() == "Q":
                            print("Retour au menu...")
                            time.sleep(3)
                            break
                        else:
                            print("\nRetour à la recherche...\n")
                            # Request to the DB
                            conecdb.request_db("TRUNCATE product")
                            time.sleep(2)
                            continue
                    product_list = conecdb.product_show_db()
                    if not product_list:
                        print("Aucun produit trouver dans la categorie, retour au menu...")
                        time.sleep(2)
                    print("\nVoici une selection de produit dans la catégorie {} :".format(results[int(cat_choice)]))
                    for pro_id, pro_name in product_list:
                        print(str(pro_id) + " - " + pro_name)
                    product_choice = input("\nQuel produit voulez vous consulter ? (Q pour revenir au menu) ")
                    if product_choice.isdigit():
                        if int(product_choice) >=0 and int(product_choice) <= len(product_list):
                            # Request the product table for the product description by join the categories table
                            product_sql = conecdb.request_db("""SELECT 
                                categories.cat_name, product.pro_name, product.pro_shop, 
                                product.pro_url, product.pro_nutriscore 
                                FROM categories INNER JOIN product 
                                ON categories.cat_id = product.pro_cat_id 
                                WHERE product.pro_id = '{}'""".format(product_choice), True)
                            product = product_sql[0]
                            # Request the product table for better nutrition score
                            pro_better_score = conecdb.request_db(
                                """SELECT `pro_name`, `pro_nutriscore` FROM `product` 
                                WHERE product.pro_nutriscore > {}""".format(product[4]), True)
                            # Print the result of the search product
                            print("\n*****************************************")
                            print("\nLe produit {} appartient à la catégorie {}.".format(product[1], product[0]))
                            if product[2] == "Inconnu":
                                print("Il possède un score nutritionnel de {}, il n'y a aucun magasin connu pour l'acheter.".format(product[4]))
                            else:
                                print("Il possède un score nutritionnel de {}, vous pouvez le trouver chez {}.".format(product[4], product[2]))
                            print("Voici le lien URL du produit : {}".format(product[3]))
                            print("\n*****************************************")
                            if  not pro_better_score :
                                print("\nIl n'y a aucun produit avec un meilleur score nutritionnel dans cette catégorie")
                            else:
                                for product, score in pro_better_score:
                                    print("Le produit {} a un meilleur score nutritionnel avec un score de {}.".format(product, score))
                                print("")
                            # Save the product
                            if user_count == 0:
                                print("Impossible de sauvegarder le produit, il n'y a pas de compte utilisateur")
                                print("Appuyez sur une touche pour revenir au menu...")
                                break_time = os.popen("pause")
                                break_time.read()
                                break
                            else:
                                save_choice = 0
                                while save_choice is 0:
                                    save_choice = input("Voulez vous sauvegarder le produit ? O/n ")
                                    if save_choice.upper() == "O":
                                        # Get the user on the DB
                                        user = conecdb.request_db(
                                            "SELECT * FROM user ORDER BY user_id", True)
                                        for id, user_name in user:
                                            print("{} - {}".format(id, user_name))
                                        user_choice = 0
                                        while user_choice is 0:
                                            user_choice = input("Quelle utilisateur voulez-vous utiliser ? ")
                                            if user_choice.isdigit() >= 1 and user_choice.isdigit() <= len(user):
                                                user_choice = int(user_choice)
                                                # Insertion of product in saved table
                                                conecdb.request_db("""INSERT INTO saved (sav_user_id, sav_name, sav_shop, sav_url, sav_cat_id, sav_nutriscore) 
                                                                    SELECT user.User_id, product.pro_name, product.pro_shop, product.pro_url, product.pro_cat_id, product.pro_nutriscore
                                                                    FROM user, product 
                                                                    WHERE product.pro_id = {} AND user.User_id = {}""".format(product_choice, user_choice))
                                                print("Produit sauvegardé, retour au menu...")
                                                time.sleep(2)
                                                break
                                            elif user_choice.upper() == "Q":
                                                print("Retour au menu...")
                                                time.sleep(2)
                                                break
                                            else:
                                                print("Choix incorrect, veuillez recommencer.")

                                    elif save_choice.upper() == "N":
                                        print("\nRetour au menu...")
                                        time.sleep(2)
                                        break
                                    else:
                                        print("\nChoix incorrect")
                                        save_choice = 0
                    elif product_choice.upper() == "Q":
                        print("Retour au menu...")
                        time.sleep(2)
                        break
                    else:
                        print("Choix incorrect, retour à la recherche...")
                        time.sleep(2)
                        continue
            else:
                choice = 0
    else:
        print("\nVeuillez créer la base de données, retour au menu...")
        time.sleep(2)

def destroy_database(db_state):
    """ Option 4 - Delete the database """
    if db_state is True:
        newdb.delete_db()
        print("\nBase de données effacer, retour au menu...")
        time.sleep(2)
    else:
        print("\nAucune base de données, retour au menu...")
        time.sleep(2)

def create_database(db_state):
    """ Option 5 - Create the database and download the categories list """
    if db_state is False:
        newdb.create_db('database.sql')
        print("\nRetour au menu...")
        time.sleep(3)
    else:
        print("\nLa base de données existe déja, retour au menu...")
        time.sleep(3)


# Main program
while program_loop is True:
    choice = 0
    user_count = 0
    categories_count = 0
    # Check if the database exist
    db_state = newdb.check_db()
    # Clear prompt
    clear_prompt()
    print("\nBienvenue sur la base de données OpenFoodFacts FR.")
    print("")
    
    if db_state is True:
        # Get the user count
        user_count = conecdb.request_db("SELECT COUNT(*) FROM user")
        # Get the categories count
        categories_count = conecdb.request_db(
            "SELECT COUNT(*) FROM categories")
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
        choice = input("\nVotre choix (Tapez Q pour quitter): ")
        # Stop the program
        if choice.upper() == "Q":
            program_loop = False
            break
        # Check if the input is a digit and between 0 and 6
        elif choice.isdigit() == False or int(choice) >= 6 or int(choice) == 0:
            print("\nVous devez entrer un nombre entre 1 et 5\n")
            time.sleep(2)
            break
        # Run the input choice
        elif int(choice) == 1:
            create_user(db_state)
        elif int(choice) == 2:
            access_sav(db_state, user_count)
        elif int(choice) == 3:
            search_product(db_state, user_count)
        elif int(choice) == 4:
            destroy_database(db_state)
        elif int(choice) == 5:
            create_database(db_state)

if __name__ == '__main__':
    pass
