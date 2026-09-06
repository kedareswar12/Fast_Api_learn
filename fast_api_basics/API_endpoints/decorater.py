def fence(func):
    def wrapper():
        print("++++++++++")
        func()
        print("++++++++++")

    return wrapper


@fence
def log():
    return f"deforated ?"

log()

"""

def log():
    return f"deforated ?"

log()



To make this as a decorater you need to initially write the decorator fxn initially 


def fence(func):
    pass

@fence
def log():
    return f"deforated ?"

log()


"""