class User():
    def __init__(self, name, password, salt) -> None:
        self.__name = name
        self.__password = password # la idea es que sea un hash
        self.__salt = salt

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
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        # check if password is hashed
        if password == "":
            raise ValueError("Password cannot be empty")
        self.__password = password
    
    @property
    def salt(self):
        return self.__salt

    def __dict__(self):
        return {
            "name": self.name,
            "password": self.password,
            "salt": self.salt
        }
