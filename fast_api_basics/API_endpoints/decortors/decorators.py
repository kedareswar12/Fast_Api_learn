# def fence(func):
#     def wrapper():
#         print("*" * 5)
#         func
#         print("*" * 5)



# def greet():
#     print("Hello Fence")

# another_function = fence(greet)
# another_function()



from typing import Any, Callable


route :dict[str , Callable[[Any] , Any]]={}

def routes(path:str):
    def register_user(func):
        route[path] = func
        return func
    return register_user

@routes("/shipment")
def get_shipment():
    return {
        "concent" : "Box",
        "status" : "In Transit"
    }

print(route)

request = ""

while request != "quit":
    request = input(">  ")

    if request in route:
        response=route[request]()
        print(response , end="\n")
    else:
        print("Not found")