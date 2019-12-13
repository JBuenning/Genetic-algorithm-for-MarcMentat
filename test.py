import random

def a():
    print('a')
def b():
    print('b')


array = [a,b]

fnc = random.choice(array)

fnc()