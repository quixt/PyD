
class Activities:

    class Game:
        def  __init__(self,*,name:str):
            self.type = 1
            self.name = name
    class Listening:
        def  __init__(self):
             pass
    class Watching:
        def  __init__(self):
             pass

    
class Status:
    class online:
        st = "online"
    class dnd:
        st = "dnd" 
    class idle:
        st = "idle"