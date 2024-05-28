import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://rasmuslogin:password@localhost/movie_site')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
