"""Server for movie ratings app."""

from flask import (Flask, render_template, request,flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    '''View homepage for site'''
    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    '''View all movies.'''
    movies = crud.get_movies()

    return render_template('all_movies.html', movies = movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    '''Show details on a particular movie.'''
    
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template("movie_details.html", movie = movie)


@app.route('/movies/<movie_id>', methods=['POST'])
def add_user_rating(movie_id):
    user_id = session['primary_key']
    user = crud.get_user_by_id(user_id)
    movie = crud.get_movie_by_id(movie_id)
    score = request.form.get('rating')
    
    new_rating = crud.create_rating(user, movie, score)

    db.session.add(new_rating)
    db.session.commit()
    flash('Rating submitted!')

    return redirect('/movies')


@app.route('/users', methods = ['POST'])
def register_user():
    """Create a new user."""
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Email already in use. Account already exists.')
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Success! Account created.')
    
    return redirect('/')


@app.route('/login',  methods = ['POST'])
def login():
    """Login to user account."""
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user.password == password:
        session['primary_key'] = user.user_id
        print(session)
        flash('Logged In!')
    else:
        flash('Password does not match.')
        
    return redirect('/')



@app.route('/users')
def all_users():
    """View all users."""
    users = crud.get_users()

    return render_template('all_users.html', users = users)


@app.route('/users/<user_id>')
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    ()
    return render_template('user_details.html', user = user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    
