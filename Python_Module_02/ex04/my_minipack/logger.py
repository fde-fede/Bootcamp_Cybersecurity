import time
from random import randint
import os

def log(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        xtime = time.perf_counter() - start
        with open("machine.log", mode = "a+", encoding="utf-8") as file:
            user = os.getenv('USER', "unknown")
            name = func.__name__.replace('_', ' ').title()
            if xtime > 0.001:
                file.write(f"({user}) Running")
            else:
                file.write(f"({user}) Running: {name:18} [ exec-time = {xtime * 1000:.3f} ms ]\n")
        return result
    return wrapper