# For you Sezim

import turtle
import math
import time


screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("#111111")
screen.title("from a BTS fan:")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(3)


def draw_heart(scale=10, color="red"):
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.color(color)
    t.begin_fill()

    for angle in range(0, 360):
        x = 16 * math.sin(math.radians(angle)) ** 3
        y = 13 * math.cos(math.radians(angle)) - 5 * math.cos(math.radians(2*angle)) - 2 * math.cos(math.radians(3*angle)) - math.cos(math.radians(4*angle))
        t.goto(x * scale, y * scale)

    t.end_fill()


scale = 10
while True:
    t.clear()
    scale = 10 + 2 * math.sin(time.time() * 3)
    draw_heart(scale, "#A4DEFF")


    
    t.penup()
    t.goto(0, -180)
    t.color("white")
    t.write("Добро Пожаловать на IT", align="center", font=("Arial", 18, "bold"))

    time.sleep(60.0)


turtle.done()