import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

import database

import generate_csv as gencsv

# Datasets
DATAFRAME = "data/filmweb_movies.csv"  # (9692 lines)
# DATAFRAME = "data/imdb_movies.csv"  # (1000 lines)


def clear_object(filename):
    read = open(filename)
    lines = read.readlines()
    del lines[-1]
    read.close()

    write = open(filename, "w")
    write.writelines(lines)
    write.close()


def save_object(movie):
    test_movie = str(movie.title) + "," + str(movie.year) + "," + \
                 str(movie.director) + "," + ''.join(movie.cast).replace(",", "|") + "," + str(movie.rating)
    filename = DATAFRAME
    mode = "a"  # write mode
    gencsv.save_to_file(test_movie, filename, mode)


def train_model(dataset, target):
    # Initialize the model class.
    model = LinearRegression()
    # Fit the model to the training data.
    model.fit(dataset, target)

    return model


def preprocess_data(dataset, encoder):
    # Convert the categorical columns into numeric; integer encoding
    dataset['year'] = encoder.fit_transform(dataset['year'])
    dataset['director'] = encoder.fit_transform(dataset['director'])
    dataset['cast'] = encoder.fit_transform(dataset['cast'])
    dataset['rating'] = encoder.fit_transform(dataset['rating'])

    return dataset


def predict_rating(movie):
    save_object(movie)

    # Columns in the dataset
    column_names = ['title', 'year', 'director', 'cast', 'rating']

    # Import data and select the rows
    train_data = pd.read_csv(DATAFRAME,
                             sep=",",
                             names=column_names,
                             usecols=['year', 'director', 'cast', 'rating'],
                             encoding="windows-1252")

    # Make a histogram of all the ratings
    # plt.hist(train_data['rating'])
    # plt.show()

    # Create the LabelEncoder object
    le = preprocessing.LabelEncoder()

    # Preprocess data
    train_data = preprocess_data(train_data, le)

    # Take the last encoded entry of a dataframe (user input), erase from the dataframe
    test = train_data.tail(1)
    train_data = train_data.iloc[:-1]

    # Assign the rating column as target
    target = train_data['rating']

    # Train model
    model = train_model(train_data.iloc[:, 0:3], target)

    # Slice test set
    test = test.iloc[:, 0:3]

    # Generate our predictions for the test set
    predictions = model.predict(test)
    x = [int(predictions[0])]
    predicted_rating = le.inverse_transform(x)[0]

    # Clear movie from the database
    clear_object(filename=DATAFRAME)

    return predicted_rating


def assign_data(title, year, director, cast):
    initial_rating = 0.0

    # Instantiate the Movie object
    movie = database.Movie(title, year, director, cast, initial_rating)

    # Predict the rating
    movie.rating = predict_rating(movie)

    return movie


def summarize(title, year, director, cast, rating):
    # Separate elements in cast with a comma
    cast = ', '.join(cast)

    # Access the instance attributes
    print("{} from {}, directed by {}, casts {}. The predicted rating: {}.\n".format(
        title, year, director, cast, rating))


# movie1 = database.Movie("Titanic", 1997, "James Cameron", "Leonardo DiCaprio|Kate Winslet", 7.3)
# predict_rating(movie1)
