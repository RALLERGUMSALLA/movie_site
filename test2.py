from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load config from Config class
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://rasmuslogin:password@localhost/DIS_project')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # Table name with the users
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    preferences = db.relationship("Prefer", back_populates="user")

    def __repr__(self):
        return f'<User {self.username}>'

class Prefer(db.Model):
    __tablename__ = 'prefer'
    p_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    filmid = db.Column(db.Integer, db.ForeignKey('film.filmid'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="preferences")
    film = db.relationship("Film", back_populates="preferred_by")

class Film(db.Model):
    __tablename__ = 'film'
    filmid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    imdb_score = db.Column(db.Float, nullable=False)
    preferred_by = db.relationship("Prefer", back_populates="film")

# Create the database and tables
with app.app_context():
    db.create_all()

# Dummy data for some functionality available to all users
public_data = [
    {'title': 'Public Feature 1', 'content': 'This is public feature 1 content.'},
    {'title': 'Public Feature 2', 'content': 'This is public feature 2 content.'},
]

# Dummy data for some functionality available only to logged-in users
private_data = [
    {'title': 'Private Feature 1', 'content': 'This is private feature 1 content.'},
    {'title': 'Private Feature 2', 'content': 'This is private feature 2 content.'},
]

@app.route('/')
def index():
    return render_template('index.html', public_data=public_data, private_data=private_data, username=session.get('username'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        # Query the database for the user
        user = User.query.filter_by(username=session['username']).first()
        if user:
            # Retrieve the movies liked by the user
            liked_movies = [prefer.film for prefer in user.preferences]
            return render_template('dashboard.html', private_data=private_data, username=session['username'], liked_movies=liked_movies)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the database for the user
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/search_users', methods=['GET', 'POST'])
def search_users():
    query = request.args.get('query', '')
    users = []

    if query:
        # Perform a case-insensitive search using the regular expression
        regex_pattern = f'%{query}%'
        users = User.query.filter(or_(
            User.username.ilike(regex_pattern),
            User.email.ilike(regex_pattern)
        )).all()

    return render_template('dashboard.html', private_data=private_data, username=session.get('username'), users=users, query=query)

@app.route('/search_movies', methods=['GET', 'POST'])
def search_movies():
    query = request.args.get('query', '')
    films = []

    if query:
        # Perform a case-insensitive search for films with titles matching the query
        regex_pattern = f'%{query}%'
        films = Film.query.filter(Film.title.ilike(regex_pattern)).all()

    return render_template('dashboard.html', films=films, query=query)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('create_account.html', message='Username already exists')
        elif existing_email:
            return render_template('create_account.html', message='Email already exists')
        
        # Create a new user and add it to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/add_movie', methods=['POST'])
def add_movie():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            # Retrieve form data
            title = request.form['title']
            genre = request.form['genre']
            runtime = int(request.form['runtime'])
            imdb_score = float(request.form['imdb_score'])

            # Create a new movie
            new_movie = Film(title=title, genre=genre, runtime=runtime, imdb_score=imdb_score)

            # Add the new movie to the database
            db.session.add(new_movie)
            db.session.commit()

            # Create a new preference entry for the user
            preference = Prefer(user=user, film=new_movie, rating=0)

            # Add the preference to the database
            db.session.add(preference)
            db.session.commit()

            # Redirect back to the dashboard
            return redirect(url_for('dashboard'))
    # If user is not logged in or encountered an error, redirect to login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
