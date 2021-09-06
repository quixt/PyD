class User():
    def __init__(self,json):
        self.id = int(json['id'])
        self.name = json['username']
        self.discriminator = json['discriminator']
        self.bot = json['bot']

        

class Member:
    def __init__(self, data):
        self.id = data['user']['id']
        self.name = data['user']['username']
        self.discriminator = data['user']['discriminator']
        self.joined_at = data['joined_at']
        self.nickname = data['nick']
        self.muted = data['mute']
        self.deafened = data['deaf']
        self.permissions = data['permissions']
