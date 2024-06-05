1. In folder SuperStats/src:
    2. copy and rename file "RenameTo___.env___.txt" to ".env" to create .env file.
    2. In .env file:
        3. Change/Insert postgres password: DB_PASSWORD = _Insert_your_password_here_
        3. Chose whether to initialize SuperStats DB or not (initialisation is required on first run): DB_INIT = True/False 
1. In terminal:
    2. Intall python=3.10 in new environment
    2. Navigate to SuperStats/src folder
    2. pip install -r requirements.txt
    2. flask run 

# Green Groceries

## Initialization ✔

Clone / download repository files and run the following to install the required packages (preferably within a venv):

    pip install -r requirements.txt

Create a new database in pgAdmin (preferably named GreenGroceries) and add the following to your .env file (normally
.env should be a private file containing user secrets, in this case we have kept it inside the project files for easy
access for the TAs):

    SECRET_KEY=<secret_key>
    DB_USERNAME=postgres || <postgres_user_name>
    DB_PASSWORD=<postgres_user_password>
    DB_NAME=GreenGroceries || <postgres_db_name>

When all this information is present (and correct) the server can be started with:

    flask run

## Folder setup 📁

The app is divided into multiple folders similar to the structure of the example project, with a few tweaks:

- __blueprints__: Contains all the separate blueprints of the app (submodules of the app the store different parts of
  the functionality)
- __dataset__: Contains the csv file used to import the produce data
- __static__: Contains static files like images, css and js files (in this case javascript was not needed in the
  frontend)
- __templates__: This is the template folder of the app that stores all html files that are displayed in the user
  browser
- __utils__: Contains the sql files and script that generate the postgresql database. Also contains a script that
  generates custom choices objects for flask forms used in SelectFields taken from the dataset.

At the root folder of the app (./GreenGroceries) six more scripts are present with the following roles:

- __\_\_init\_\_.py__: Initializes the flask app and creates a connection to the database (and a cursor object for
  future queries)
- __app.py__: Runs the app created by \_\_init__.py
- __filters.py__: Implements custom template filters for nicer formatting of data in the frontend
- __forms.py__: Implements forms used to save data from users (similar to the example project)
- __models.py__: Implements custom classes for each of the database tables to store data in a clean OOP manner (again,
  similar to the example project, but our models inherit the dict class for faster and more readable lookups)
- __queries.py__: Implements functions for each needed query to the database used inside the app (similar to the
  functional part of the models.py file within the example project)

## Routes 📌

Both implemented blueprints come with a __routes.py__ file that initialize a __Blueprint__ object and define _routes_
for the app.

- __Login__:
    - __/home__: Home page
    - __/about__: About page
    - __/style-guide__: Style guide (displays all html elements used, just for fun and css debugging)
    - __/login__: User login page (for simplicity in debugging, password hashing was omitted even though the example
      project made it pretty clear and easy to implement with bcrypt)
    - __/signup__: User signup (creation) page
    - __/logout__: Logs user out and sends back to login page

- __Produce__:
    - __/produce__: Search page for all produce in the database
    - __/add-produce__: Page where farmer users can add their produce (customers trying to submit will get an error)
    - __/your-produce__: Page where farmers can view and manage their produce
    - __/produce/restock/<pk>__: Page where farmers can restock a certain product
    - __/produce/buy/<pk>__: Page where customers get redirected to in order to buy a certain product
    - __/produce/your-orders__: Page where customers can view their orders

## Known backend issues / Intended features ⁉

- There is no good differentiation between customers and farmers in the _current_user_ global variable
- This results in some security issues when accessing links ment for farmers as customers and vice-versa (should be
  checked by the validation methods of the forms, but in the perfect scenario specific links should only be accessible
  by specific users)
- Given the correct url, farmers may be able to update data on other farmers produce (not tested, but seems logical)

All of these issues can be solved with a bit of extra work on the design of the app (specifically how the _current_user_
is represented by the __User__ interface within __models.py__ such that it also knows whether the logged-in user is a
farmer or a customer)

## Known frontend issues ☹

- The produce page may be a bit confusing as the filters seem to be preselected. This is not the case as the first load
  of the produce page simply displays the filtering form which has multiple select fields with options coming from the _
  choices_ defined above, no empty option was added in this case
- The app is not the most responsive on mobile devices in most cases (navbar is the issue)
- Missing confirmation messages on successful form submissions (for example when adding produce) everything works but
  nothing happens when it does work, so it maybe is a bit confusing.1
- Missing favicon.ico console error (ignored)
