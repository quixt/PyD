class User():
    def __init__(self,json):
        self.id = int(json['id'])
        self.name = json['username']
        self.discriminator = json['discriminator']
        self.bot = json['bot']