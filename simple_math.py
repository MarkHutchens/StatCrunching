print("Hello World!")
import random
import math

def roll(number):
    tot = [0] * 6
    for i in range(0,number):
        x = random.randint(1,6)
        y = random.randint(1,4)
        tot[abs(x-y)] += 1

    for i in range(6):
        tot[i] /= number
    print(tot)

x = 1

while(x != 'q'):
    x = input("How many rolls? ")
    roll(int(x))