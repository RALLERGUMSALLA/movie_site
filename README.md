# PROJECT OVERVIEW 

This project consists of a Flask-based website that interacts with a PostgreSQL database using SQLAlchemy. The website allows users to search for movies, users, and producers, and to create a personalized dashboard with favorite movies and producers.


## DIRECTORY STRUCTURE 

data
-- Contains the data for the database

sql
-- Contains the sql queries to create the database

templates
-- Contains the HTML for the different links on the site

README.md
-- Contains what you are reading now

requirements.txt
-- Contains the requirements to run the code

website.py
-- Contains the flask funtionality for the site

## Setting up the DB

### Prerequisites

* Install PostgreSQL and pgAdmin 4
* Create a new database in pgAdmin called `DIS_project`

### Create Login/Group Roles

* Create a new login role with username `rasmuslogin` and password `password`
* Grant the following privileges to the role via a query to the database:
```sql:
ALTER ROLE rasmuslogin LOGIN;
ALTER ROLE rasmuslogin CREATEDB;
ALTER ROLE rasmuslogin SUPERUSER;
```

### Create Schema and Insert Data

* Create a new schema using the SQL script in `create_table.txt`
* Insert data from the provided CSV files:
	+ `favor.csv`
	+ `film.csv`
	+ `prefer.csv`
	+ `producer.csv`
	+ `produces.csv`
	+ `users.csv`
* Use the SQL script in `insert_data.txt` to upload the data, modifying the path to the CSV files as needed

## Setting up the Site

### Install Dependencies

* Run `pip install -r requirements.txt` to install the required packages

### Run the Site

* Run `python3 website.py` from the command line
* Copy the http link that appears and paste it into a browser

Congratulations! You are now ready to browse the website.

## Browsing the Site

### Browsing without logging in

* When not logged in to a user, your access to the sites features is limited. 
* You only get access to the search features of the website

### Create a New User

* Create a new user on the website by clicking on create an account
* Here you can create an account by typing a username, email and password.

### Home Page

* Search for movies, users, and producers. This is done using SQLAlchemy's ilike. and the PostgreSQL equievelant of this is (for users search):
```sql:
SELECT * FROM users
WHERE username ILIKE '%query%' OR email ILIKE '%query%';
```
* Able to rate producers and movies, and check other users rating
* View your own favorite movies and producers on the dashboard and your ratings

### Favorite Producers

* Select a producer and give a rating
* Press "Favorite and Rate" to add the producer to the user's favorites

### Favorite movies

* Select a movie and give a rating
* Press "Favorite", after giving a rating, to add the movie to the user's favorites

### Viewing other users rating

* Select a user and press "View Dashboard" (only some of the created dummy users have favorites, 'David' is one that has)

## Dummy User

* Create a dummy user called `sara` with password `123` and any email address
* Run the SQL script in `example.txt` to add favorite movies
* Browse the favorite movies and producers to see the expected results
* With a created user and logged in, you can then add and rate your favourite producers

* Or create your own user and play around with the different features

## Future Improvements

* Make the site look better
* Be able to remove a producer/movies from your favorites 
* Notification, if new producer/movie is added to the database that you favor.





