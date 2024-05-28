from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
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
    __tablename__ = 'users'  # Specify the table name explicitly
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Define relationship with Prefer model
    preferences = db.relationship("Prefer", back_populates="user")

    def __repr__(self):
        return f'<User {self.username}>'

class Prefer(db.Model):
    __tablename__ = 'prefer'
    P_ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    FilmID = db.Column(db.Integer, db.ForeignKey('film.filmid'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Define relationship with User and Film models
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

    # Define relationship with Prefer model
    preferred_by = db.relationship("Prefer", back_populates="film")

# Create the database and tables
with app.app_context():
    db.create_all()

# Dummy data for some functionality available only to logged-in users
private_data = [
    {'title': 'Private Feature 1', 'content': 'This is private feature 1 content.'},
    {'title': 'Private Feature 2', 'content': 'This is private feature 2 content.'},
]

@app.route('/')
def index():
    return render_template('index.html', private_data=private_data, username=session.get('username'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
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
        
        # Check if the username or email already exists
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

if __name__=="_main_":
    app.run(debug=True)