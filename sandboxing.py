"""Example of wrapper with explanation"""
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)

    return wrapper


@decorator
def f(x, num):
    """does some math"""
    return x * x + num


print(f(2, num=3))
print(f.__name__)
print(f.__doc__)

"""change @wraps and see the difference in outputs"""
