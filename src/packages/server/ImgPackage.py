from PIL import Image

class ImgPackage():
    def __init__(self, author, date, time, path) -> None:
        self.__author = author
        self.__date = date
        self.__time = time
        self.__path = path
        self.__image = (Image.open(path)).copy()

    @property
    def author(self):
        return self.__author
    
    @property
    def date(self):
        return self.__date
    
    @property
    def time(self):
        return self.__time
    
    @property
    def image(self):
        return self.__image
    
    def __str__(self) -> str:
        return f"Author: {self.author}, Date: {self.date}, Time: {self.time}\n"
    
    def __repr__(self) -> str:
        return self.__str__()
