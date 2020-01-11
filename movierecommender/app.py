from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

import recommender as mvrec


class MyGrid(Widget):

    title = ObjectProperty(None)
    year = ObjectProperty(None)
    director = ObjectProperty(None)
    cast = ObjectProperty(None)

    def erase(self):
        self.title.text = ""
        self.year.text = ""
        self.director.text = ""
        self.cast.text = ""

    def submit(self):
        if self.title.text != "" and self.year.text != "" and self.director.text != "" and self.cast.text != "":
            self.show_info()
            mvrec.short_desc(self.title.text, self.year.text, self.director.text, self.cast.text)
        else:
            print("Please put in all essential information!\n")

    def show_info(self):
        print(
            "Title: ", self.title.text,
            "\nYear: ", self.year.text,
            "\nDirector: ", self.director.text,
            "\nCast: ", self.cast.text,
            "\n"
        )

    def pressed(self):
        self.submit()
        self.erase()


class MyApp(App):

    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()



