__author__ = 'mark'
import math


def print_isosceles(h):
    #Prints an isosceles triangle with h rows.
    final = "*" * (h - 1)
    row = " " * (h-1)
    while(row != final):
        print(row[::-1] + "*" + row)
        row = row.replace(" ", "*", 1)
    print(row[::-1] + "*" + row)

def distance(point1x, point1y, point2x, point2y):
    to_return = 0

    return to_return

def point_is_in_circle(origin_x, origin_y, diameter, x, y):
    to_return = False
    centerx = origin_x + (diameter // 2)
    centery = origin_y + (diameter // 2)
    distx =
    disty =
    return to_return

print_isosceles(10)
print(point_is_in_circle(5, 15, 100, 52, 61))