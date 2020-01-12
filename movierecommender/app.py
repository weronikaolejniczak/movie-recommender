# TODO:
#  integrate neural networks

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window

import recommender as mvrec


class MyGrid(Widget):

    Window.size = (500, 400)

    title = ObjectProperty(None)
    year = ObjectProperty(None)
    director = ObjectProperty(None)
    cast = ObjectProperty(None)

    def clear(self):
        self.title.text = ""
        self.year.text = ""
        self.director.text = ""
        self.cast.text = ""

    def show_rating(self, movie_rating):
        self.rating.text = str(movie_rating)

    def submit(self):
        if self.title.text != "" and self.year.text != "" and self.director.text != "" and self.cast.text != "":
            self.show_info()

            movie = mvrec.assign_data(self.title.text, self.year.text, self.director.text, self.cast.text)

            self.show_rating(movie.rating)
        else:
            print("Please put in all essential information!\n")

    def show_info(self):
        print(
            "Title: ", self.title.text,
            "\nYear: ", self.year.text,
            "\nDirector: ", self.director.text,
            "\nMain cast: ", self.cast.text,
            "\n"
        )

    def pressed(self):
        self.submit()
        self.clear()


class MyApp(App):

    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()
