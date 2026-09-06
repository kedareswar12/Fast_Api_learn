
from atexit import register
from typing import Callable , Any

# callable -> can take more arguments and return those arguments 
"""
Callable[[int , int] , int | float]
[int , int] -> function parametric hinting 

def add (a,b -> [int , int] )

, int | float -> retrun type value 

"""



# def decorator( func : Callable[[int , int , Any] , int | float] ):
#     pass

# step1 
routes : dict[str , Callable[[Any] , Any]] = {}


# creating the decorator for the fastapi
# Give me a URL path, and I’ll give you a decorator that stores a function for that path.
def route(path:str): #this will take any number of arguments  because of path
    def register_route(func):
        routes[path] = func
        return func 
    return register_route

"""
route("/shipment) -> path=("/shipment) ->  register_route is waiting fot the func  -> "retrun register_route "

@route("/shipment")
def get_shipment():
    return {
        "content" :"woden box",
        "status": "In_transit"}

get_shipment = route("/shipment")(get_shipment)



"""
@route("/shipment")
def get_shipment():
    return {
        "content" :"woden box",
        "status": "In_transit"}


print(routes)
request :str= ""

while request != "quit":
    request = input("> ")
    if request in routes :
        response = routes[request]()
        print(response , end="\n\n")
    else:
        print("notfound")