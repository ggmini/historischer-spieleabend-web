class Topic:
    def __init__(self, name, games, id, date, moderator):
        self.name = name
        self.games = games
        self.id = id
        self.date = date
        self.moderator = moderator
    
    def Name(self):
        return self.name
    def Games(self):
        return self.games
    def Id(self):
        return self.id
    def Date(self):
        return self.date
    def Moderator(self):
        return self.moderator