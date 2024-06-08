------ PROJECT OVERVIEW ------------

This project consists of a Flask-based website that interacts with a PostgreSQL database using SQLAlchemy. The website allows users to search for movies, users, and producers, and to create a personalized dashboard with favorite movies and producers.


Test2.py
-- Contains the flask funtionality for the site

templates
-- Contains the HTML for the different links on the site

requirements.txt
-- Contains the requirements to run the code


------ SETTING UP THE DB ------------

First get postgresSQL and pgadmin 4

Then create new database in pgadmin called DIS_project

Then make sure to create a Login/Group Roles, give it the username: rasmuslogin, and the password: password

Make sure this login has the access to the database by giving this query: 

>>ALTER ROLE rasmuslogin LOGIN;

>>ALTER ROLE rasmuslogin CREATEDB;

>>ALTER ROLE rasmuslogin SUPERUSER;

In the database create the new schema with present under SQL create_table.txt. 

Insert data from the given CSV files: 
- favor.csv
- film.csv
- prefer.csv
- producer.csv
- produces.csv 
- users.csv 

The code for uploading the data can be found under SQL insert_data.txt - you just have to change the path to the csv files. 

------ SETTING UP THE SITE ------------

First download the packages present in requirements.txt 
>> pip install -r requirements.txt

Then run from command line:
>> python3 test2.py 

Copy the link that pops up into a browser. 

Congratulations! You are ready to browse the website. 

------ BROWSING THE SITE ------------

Now you can create a new user. 

In Home you can search for movies, users and producers (here we have implemented pur regex expressions). 

In Dashboard you can see the movies liked by the user and the favorite producers with the given rating. 

In Home, under search producers, you can select one and give a rating and by pressing "favorite and rate" you will add this producer with the given rating to the producers that are favored by the user. 

------ DUMMY USER ------------

Create a dummy user: on the webpage create a user called sara with password 123 and any mail you like. Then run the code under SQL example.txt and browse the favourite movies and see that the right 3 movies appear. 

Now you can also add favourite producers. 






SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin FROM pg_roles WHERE rolname = 'rasmuslogin';

ALTER ROLE rasmuslogin LOGIN;
ALTER ROLE rasmuslogin CREATEDB;
ALTER ROLE rasmuslogin SUPERUSER;



CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);





