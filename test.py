def my_decorator(func):
    def bullshit():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return bullshit

def say_hello():
    print("Hello!")

def print_one():
    print("1")

def print_two():
    print("2")

blah = my_decorator(say_hello)

blah()

a = my_decorator(print_one)

a()

print("AAAAAAAAAA")

b = my_decorator(a)

b()

print("ASS")

@my_decorator
def decor_hello():
    say_hello()

decor_hello()


def repeat_decorator(n,func):
    def repeated():
        for i in range(n):
            func()
    return repeated

repeat_two = repeat_decorator(10,print_two)


repeat_two()



