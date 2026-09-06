# from mypy_extensions import mypyc_attr ->  extenction is used to give the warnings 


from typing import Any


class City():
    def __inti__(self,name : str, location:int):
        self.name = name
        self.location = location


text = "value"

# type hinting

text:str = "value"

# this also will work 
text:float = 10.09


def root(num:int) -> float :
    num 
    # if you dont mention the typehinting for the parameter you cannot access the objects inside that particular class / datatype
    return pow(num ,.5)

# type hinting can be done on the sequence elements also now 

digits : list[int] = [1,2,3,4]
tables_5 :tuple[int, ...] = (1,2,3,4,5)


# similarly 
shipment: dict[str , str | int]= {
    "content" : "wooden box",
    "satus" : "In Transit"
}

# if you need to have any other datatype use Any 
shipment: dict[str , Any]= {
    "content" : "wooden box",
    "satus" : "In Transit"
}


Delhi= City()
city_temp :tuple[City, float]= ("Delhi" , 545532)
