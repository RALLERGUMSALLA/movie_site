Flasksite.py
-- Contains the flask funtionality for the site

templates
-- Contains the HTML for the different links on the site


Setup database:


SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin FROM pg_roles WHERE rolname = 'rasmuslogin';

ALTER ROLE rasmuslogin LOGIN;
ALTER ROLE rasmuslogin CREATEDB;
ALTER ROLE rasmuslogin SUPERUSER;
