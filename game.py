class Game:
    def __init__(self, name, developer, publisher, year, country, plattform, link):
        self.name = name
        self.developer = developer
        self.publisher = publisher
        self.year = year
        self.country = country
        self.plattform = plattform
        self.link = link

    def Name(self):
        return self.name
    def Developer(self):
        return self.developer
    def Publisher(self):
        return self.publisher
    def Year(self):
        return self.year
    def Country(self):
        return self.country
    def Plattform(self):
        return self.plattform
    def Link(self):
        return self.link