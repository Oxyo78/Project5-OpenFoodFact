# Project5-OpenFoodFact


It's a project about food substitute, the user enter a food and the software use [**OpenFoodFacts.com**](https://world.openfoodfacts.org/) database to give some substitute.
This application use the french **OpenFood Facts** database and will run in french.

[Trello url](https://trello.com/b/ms61EyzV/project5-openfoodfact) to follow the project


**How to use it ?:**
----------

First, when you launch the app, you got 2 reading choices in the terminal:

 - 1 - Quel aliment souhaitez-vous remplacer ? 
 - 2 - Retrouver mes aliments substitués.
 
 If you select 1, the app will ask you to select an category in a list of 10 foods. Select the number of food in the category and the app will show  the desciption product, where you can buy it and the url from **OpenFoodFacts.com**.
 
 The app will ask you if you want to save the food product or make a new search.

If you select 2, the app will show you the list of your saved food product, select the number of the product to see the desciption, shop and url.

**Installation:**
----------
Install packages:

    pip install -r requirements.txt

Install [MySQL](https://dev.mysql.com/downloads/installer/) >= 5.5

**Functionality:**
----------

new_user_database:
This function create a new folder named "user" for the MySQL database if no exist.
If you want to delete the database, delete "user" folder the home path of the program.py file

save_user_food:
This function save a food product from the user search.
The database will save the name, description, shop and OpenFoodFacts URL.

call_user_food:
This function will print the list of the food product name in the database and ask the user which one he want to see the description, shop and URL.

food_category_database:
This function will create a database and get the FR category json file from the OpenFoodFacts.org.

