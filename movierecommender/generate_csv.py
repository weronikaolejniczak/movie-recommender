import re
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


def save_to_file(row, filename, mode):
    file = open(filename, mode)
    try:
        file.write(row + "\n")
    except UnicodeEncodeError:
        row = unidecode(row)
        file.write(str(row) + "\n")


# Generate training set FILMWEB
def generate_from_filmweb(count, filmweb_url):
    filename = "data/filmweb_movies.csv"
    source = requests.get(filmweb_url)
    soup = BeautifulSoup(source.content, 'html.parser')

    # Print the contents of the page
    # print(soup.prettify())

    # Print all <div> elements with class 'filmPreview__card' from the 1st page; 10 elements on each page
    # print(soup.findAll("div", class_="filmPreview__card"))

    for div in soup.findAll("div", class_="filmPreview__card"):

        # Assign movie title to a variable 'title'
        try:
            title = div.find("div", class_="filmPreview__originalTitle").contents[0].replace(",", "")
        except AttributeError:
            title = div.find("h3", class_="filmPreview__title").contents[0].replace(",", "")

        # Assign on-air year to a variable 'year'
        try:
            year = div.find("span", class_="filmPreview__year").contents[0]
        except AttributeError:
            year = "None"

        # Assign director to a variable 'director'
        try:
            director = div.find("div", class_="filmPreview__info--directors")
            director = director.find("a").contents[0]
        except AttributeError:
            director = "None"

        # Append actors to a list 'cast'
        cast = []
        actors = div.find("div", class_="filmPreview__info--cast")

        try:
            actors = actors.findAll("a")
            for actor in actors:
                cast.append(actor.contents[0])
        except AttributeError:
            actors = "None"
            cast.append(actors)

        # Concatenate cast elements into a string
        cast_str = ""
        for actor in cast:
            if cast.index(actor) < len(cast) - 1:
                cast_str = cast_str + actor + "|"
            else:
                cast_str = cast_str + actor

        # Assign rating to a variable 'rating'
        try:
            rating = div.find("span", class_="rateBox__rate").contents[0]
            rating = rating.replace(",", ".")
        except AttributeError:
            rating = 0.0

        # Print all information
        movie = str(title) + "," + str(year) + "," + str(director) + "," + str(cast_str) + "," + str(rating)

        # Write into CSV file
        save_to_file(movie, filename=filename, mode="a")

    # From the first to the last page there are 10 000 (10 cards * 1000 pages) movie cards
    # Second page: "https://www.filmweb.pl/films/search?page=2"
    # Last page: "https://www.filmweb.pl/films/search?page=1000"

    count += 1
    filmweb_url = "https://www.filmweb.pl/films/search?page={}".format(1 + count)

    if count < 971:
        generate_from_filmweb(count, filmweb_url)

    print("Data downloaded into {}.".format(filename))


# Generate testing set IMDB
def generate_from_imdb(count, imdb_url):
    filename = "data/imdb_movies.csv"
    source = requests.get(imdb_url)
    soup = BeautifulSoup(source.content, 'html.parser')

    # Print the contents of the page
    # print(soup.prettify())

    # 50 movie cards per page
    for div in soup.findAll("div", class_="lister-item-content"):

        # Assign movie title to a variable 'title'
        try:
            title = div.find("h3", class_="lister-item-header") \
                .find("a") \
                .contents[0].replace(",", "")
        except AttributeError:
            title = "None"

        # Assign on-air year to a variable 'year'
        try:
            year = div.find("h3", class_="lister-item-header") \
                       .findAll("span")[1] \
                       .contents[0].replace(",", "")[1:]
            year = re.findall("[1-2][0-9][0-9][0-9]", year)[0]
        except AttributeError:
            year = "None"

        # Assign director to a variable 'director'
        try:
            director = div.find("p", class_="")
            director = director.find("a").contents[0]
        except AttributeError:
            director = "None"

        # Append actors to a list 'cast'
        cast = []
        actors = div.find("p", class_="")

        try:
            actors = actors.findAll("a")
            for actor in actors:
                if actors.index(actor) > 0:
                    cast.append(actor.contents[0])
        except AttributeError:
            actors = "None"
            cast.append(actors)

        # Concatenate cast elements into a string
        cast_str = ""
        for actor in cast:
            if cast.index(actor) < len(cast) - 1:
                cast_str = cast_str + actor + "|"
            else:
                cast_str = cast_str + actor

        # Assign rating to a variable 'rating'
        try:
            rating = div.find("div", class_="inline-block ratings-imdb-rating").find("strong").contents[0]
            rating = rating.replace(",", ".")
        except AttributeError:
            rating = 0.0

        # Print all information
        movie = str(title) + "," + str(year) + "," + str(director) + "," + str(cast_str) + "," + str(rating)

        # Write into CSV file
        save_to_file(movie, filename=filename, mode="a")

    # From the first to the last page there are 1 000 (50 cards * 20 pages) movie cards
    # Second page: https://www.imdb.com/search/title/?title_type=tv_movie&user_rating=1.0,10.0&start=51
    # Last page: https://www.imdb.com/search/title/?title_type=tv_movie&user_rating=1.0,10.0&start=9951

    count += 50
    imdb_url = \
        "https://www.imdb.com/search/title/?title_type=tv_movie&user_rating=1.0,10.0&start={}".format(1 + count)

    if count < 1000:
        generate_from_imdb(count, imdb_url)


def main():
    filmweb_url = "https://www.filmweb.pl/films/search"
    imdb_url = "https://www.imdb.com/search/title/?title_type=tv_movie&user_rating=1.0,10.0"

    counter1 = 0
    print("Loading data from IMDB: {}".format(imdb_url))
    generate_from_imdb(counter1, imdb_url)
    print("Data scraped and saved.")

    counter2 = 0
    print("Loading data from Filmweb: {}".format(filmweb_url))
    generate_from_filmweb(counter2, filmweb_url)
    print("Data scraped and saved.")


if __name__ == '__main__':
    main()
