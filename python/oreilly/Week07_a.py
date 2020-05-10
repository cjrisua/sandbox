
class Grape():
    def __init__(self,Name):
        self.varietal = Name

class Wine(Grape):
    def __init__(self,Name,Vintage,Varietal):
        Grape.__init__(self,Varietal)
        self.__name = Name
        self.__vintage = Vintage

    @property
    def name(self):
        return self.__name
    
    @property
    def vintage(self):
        return self.__vintage
    
    @vintage.setter
    def vintage(self,vintage):
        self.__vintage = vintage

wine=Wine("Favia","2016","Cabernet Sauvignon")
wine.vintage = 2010
print(f"{wine.name} {wine.vintage} {wine.varietal}")
