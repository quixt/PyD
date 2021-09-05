
class ApplicationCommand:
    def __init__(self,data):
        self.id:int = data['id']
        self.bot_id:int = data['application_id']
        self.name:str  = data['name']
        self.description:str = data['description']
        self.type = 1