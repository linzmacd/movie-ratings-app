"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')
model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as filename:
    movie_data = json.loads(filename.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie dictionary. 
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    
    # Then, get the release_date and convert it to a datetime object with datetime.strptime
    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')

    # TODO: create a movie here and append it to movies_in_db
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

    model.db.session.add_all(movies_in_db)
    model.db.session.commit()


for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # TODO: create a user here
    db_user = crud.create_user(email, password)
    model.db.session.add(db_user)
    
    # TODO: create 10 ratings for the user
    for num in range(10):
        random_movie = choice(movies_in_db)
        score_new = randint(1,5)

        rating = crud.create_rating(db_user, random_movie, score_new)
        model.db.session.add(rating)

model.db.session.commit()