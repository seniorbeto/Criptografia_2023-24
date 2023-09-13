from .user import User

class Camera():
    def __init__(self, name:str, owner:str) -> None:
        self.__name = name
        self.__owner = owner

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if name == "":
            raise ValueError("Name cannot be empty")
        elif len(name) > 50:
            raise ValueError("Name cannot be longer than 50 characters")
        
        self.__name = name

    @property
    def owner(self):
        return self.__owner
    
    @owner.setter
    def owner(self, owner):
        if owner == "":
            raise ValueError("Owner cannot be empty")
        elif len(owner) > 50:
            raise ValueError("Owner cannot be longer than 50 characters")
        
        self.__owner = owner
    
    
    def __dict__(self):
        return {
            "name": self.name,
            "owner": self.owner
        }