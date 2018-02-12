# Project5-OpenFoodFact


It's a project about food substitute, the user enter a food and the software use [**OpenFoodFacts.com**](https://world.openfoodfacts.org/) database to give some substitute.
This application use the french **OpenFood Facts** database and will run in french.

[Trello url](https://trello.com/b/ms61EyzV/project5-openfoodfact) to follow the project


**How to use it ?:**
----------

First, when you launch the app, you got 5 reading choices in the terminal:

 - 1 - Créer un compte utilisateur
 - 2 - Accédez à vos produits sauvegardés
 - 3 - Rechercher un produit dans la listes des catégories
 - 4 - Effacer la base de données actuelle
 - 5 - Créer la base de données locale
 
 If you select 1, You can make a new user account.

 If you select 2, You can access to your saved product.

 If you select 3, the app will ask you to enter the beginning of an category name and will show you a list of 10 foods. Select the number of food in the category and the app will show the description product, where you can buy it, the url from **OpenFoodFacts.com** and some better substitute at your product. At the end, you save the substitute under condition your make a user account.

 If you select 4, You can delete all the database ( user, saved, product and categories), be carreful ! it's not reversible !

 If you select 5, You can build the database and download the french database from **OpenFoodFacts.com**, it may take some time, depend off your speed network connection.

**First use**
----------

For the first use, you must have your local server online and build the database by select the option 5
If you want save some substitute, create a account user before the search

**Installation:**
----------
Install packages:

    pip install -r requirements.txt

Install [MySQL](https://dev.mysql.com/downloads/installer/) >= 5.5



