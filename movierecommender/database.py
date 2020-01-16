import re


class Movie:

    # Class Attribute

    # Initializer / Instance Attributes
    def __init__(self, title, year, director, cast, rating):
        self.title = title
        self.year = year
        self.director = director
        self.cast = cast
        self.rating = rating

    def check_year(self):
        if re.match("^(18(8[8-9]|9[0-9]))|(19[0-9][0-9])|(20([0-1][0-9]|20))$", self.year):
            return 0
        else:
            return 1

    def check_director(self):
        if re.match(
                "^[A-Z][a-z]*([a-z]+|(-[A-Z][a-z]+)|(\'[a-z]+)|( [A-Z][a-z]*))( ([A-Z]|(von [A-Z]))[a-z]+(((( )|-)[A-z][a-z]+)?)*)?",
                self.director):
            return 0
        else:
            return 1

    def check_cast(self):
        for actor in self.cast:
            if re.match(
                    "^[A-Z][a-z]*([a-z]+|(-[A-Z][a-z]+)|(\'[a-z]+)|( [A-Z][a-z]*))( ([A-Z]|(von [A-Z]))[a-z]+(((( )|-)[A-z][a-z]+)?)*)?",
                    actor):
                return 0
            else:
                return 1

    def check_rating(self):
        if re.match("^[0-9]\.[0-9]$", str(self.rating)):
            return 0
        else:
            return 1

    def check_data(self):
        if self.check_year() == 0 \
                and self.check_director() == 0 \
                and self.check_cast() == 0 \
                and self.check_rating() == 0:
            return 0
        else:
            print("Oh no! Incorrect data, try again!")
