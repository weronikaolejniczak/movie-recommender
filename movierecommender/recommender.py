# TODO:
#  prepare training and testing set,
#  write algorithm for neural networks,
#  train algorithm,
#  test algorithm

import database

# Data sets
TRAINING_SET = "data/filmweb_movies.csv"
TESTING_SET = "data/imdb_movies.csv"


def predict_rating():
    rating = 0

    # Generate list of possible ratings: float numbers from 0.0 to 10.0
    class_names = [x * 0.1 for x in range(0, 100)]

    return rating


def assign_data(title, year, director, cast):
    # Predict the rating
    rating = predict_rating()

    # Instantiate the Movie object
    movie = database.Movie(title, year, director, cast, rating)

    # Show a short summary
    summarize(title, year, director, cast, rating)

    return movie


def summarize(title, year, director, cast, rating):
    # Separate elements in cast with a comma
    cast = cast.replace("\n", ", ")

    # Access the instance attributes
    print("{} was aired in {}, directed by {} and casted {}. The predicted rating: {}.".format(
        title, year, director, cast, rating))

