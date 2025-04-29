from datetime import datetime   

def greet_decorator(func):
    def wrapper(*args,**kwargs):
        print("Hello All!")
        func(*args,**kwargs)
        print("Goodbye!")
    return wrapper

def after4PMDeny(func):
    def wrapper(*args,**kwargs):
        try:
            now = datetime.now().hour
            if now>=16:
                raise Exception("After 4 PM, no more requests are allowed")
        except Exception as e:
            print(e)
        finally:
            func(*args, **kwargs)
    return wrapper

@after4PMDeny
@greet_decorator
def greet():
    print("Hello World!")

@greet_decorator
def greet_eve():
    print("Hello Eve!")

@greet_decorator
def greet_adam():
    print("Hello Adam!")


if __name__ == '__main__':
    greet()
    greet_eve()
    greet_adam()