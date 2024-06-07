# SuperStats - Supersuperliga statistics

https://github.com/mVigholt/DIS.git

## Conforming to requirements ✔
  1. Public git repository
  1. E/R diagram in Superstats/diagram
  1. How to Initiate, compile, run and interact with webpage in readme.md
  1. SQL INSERT/UPDATE/DELETE/SELECT statements used for database interaction
  1. Regular expression matching used at signup (username should be a mail)


## Initialization ✔

1. In folder SuperStats/src:
    1. copy and rename file "RenameTo___.env___.txt" to ".env" to create .env file.
    1. In .env file:
        1. Change/Insert postgres password: DB_PASSWORD = _Insert_your_password_here_
        1. Chose whether to initialize SuperStats DB or not (initialisation is required on first run): DB_INIT = True/False 
1. In terminal:
    1. Intall python=3.10 in new environment
    1. Navigate to SuperStats/src folder
    1. pip install -r requirements.txt
    1. Run program with or without specifying host and port: 
      1. flask run 
      1. flask run -h localhost -p 5000


## Folder setup 📁

The app is divided into multiple folders similar to the structure of the example project, with a few tweaks:

- __blueprints__: Contains all the separate blueprints of the app (submodules of the app the store different parts of the functionality)
- __dataset__: Contains the csv file used to import startdata
- __static__: Contains static files like images, css and js files (in this case javascript was not needed in the frontend)
- __templates__: This is the template folder of the app that stores all html files that are displayed in the user browser
- __utils__: Contains the sql files and script that generate the postgresql database. Also contains a script that generates custom choices objects for flask forms used in SelectFields taken from the dataset.


### At the root folder of the app (./src) six more scripts are present with the following roles:

- __\_\_init\_\_.py__: Initializes the flask app and creates a connection to the database (and a cursor object for future queries)
- __app.py__: Runs the app created by \_\_init__.py
- __filters.py__: Implements custom template filters for nicer formatting of data in the frontend
- __forms.py__: Implements forms used to save data from users (similar to the example project)
- __models.py__: Implements custom classes for each of the database tables to store data in a clean OOP manner (again, similar to the example project, but our models inherit the dict class for faster and more readable lookups)
- __queries.py__: Implements functions for each needed query to the database used inside the app (similar to the functional part of the models.py file within the example project)

## Routes 📌

Both implemented blueprints come with a __routes.py__ file that initialize a __Blueprint__ object and define _routes_ for the app.

- __LoginTabs__:
    - __/home__: Home page
    - __/about__: About page
    - __/style-guide__: Style guide (displays all html elements used, just for fun and css debugging)
    - __/login__: User login page (for simplicity in debugging, password hashing was omitted even though the example project made it pretty clear and easy to implement with bcrypt)
    - __/signup__: User signup (creation) page
    - __/logout__: Logs user out and sends back to login page

- __InfoTabs__:
    - __/Player-info__: Search page for statistics on all players in the database
    - __/Club-info__: Search page for statistics on all clubs in the database
    - __/League-Table__: List of statistics on all clubs in the database
    - __/Add-match__: Page where a signed in manager can add matchinfo for a match involving their club.
    - __/Delete-match__: Page where a signed in manager can delete a match involving their club.