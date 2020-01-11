import database


def assign_data(title, year, director, cast):
    rating = 0
    movie = database.Movie(title, year, director, cast, rating)

    return movie


def short_desc(title, year, director, cast):
    # Instantiate the Movie object
    movie = assign_data(title, year, director, cast)

    # Access the instance attributes
    print("{} was aired in {}, directed by {} and casted {}. The rating on IMDB: {}.".format(
        movie.title, movie.year, movie.director, movie.cast, movie.rating))

