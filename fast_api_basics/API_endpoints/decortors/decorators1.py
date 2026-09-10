from ast import Name
from typing import Any, Callable


# def decorator(func):
#     def wrapper():
#         print("Function Started")
#         func()
#         print("Function Ended")
#     return wrapper


# def greet():
#     print("Hello Kedar")

# x = decorator(greet)
# x()


routes : dict[str , Callable[[Any] , Any]] = {

    "Abc" : "def()"
}


def route(path : str):
    def register_routes(func):
        routes[path] = func
        return func
    return register_routes


@route("/shipment")
def get_shipment():
    return {
        "content" : "Mobile",
        "Shipment" : "In transit"
    }

request = ""

while request != "quit":
    request = input(">  ")
    if request in routes:
        response = routes[request]()
        print(response)
    else: 
        print('Not found')


# routes[request] -> calling the mapped function

# example_dict = {
#     "Name" : "Kedareswar",
#     "Working" : "Software Engineer"
# }
# print(example_dict['Name'])