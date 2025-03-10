import turtle
import random
import time
from ball import *
from ground import *
from line import *
# Основний код програми
screen = turtle.Screen()
screen.setup(width=1200, height=800)
screen.tracer(0)
screen.title('Гравітація з шаріками')
screen.bgcolor('#9dd3f2')
turtle.color("#914a03")
radius = 10
sleep = 0.001
first_click = True
xpos1=None
ypos1=None
xpos2=None
ypos2=None
surface = Surface()
balls = []

def create_ball(x, y, radius=10):
    vx = random.uniform(-5, 5)
    vy = random.uniform(5, 15)
    ball = Ball(x, y, vx, vy, radius)
    balls.append(ball)

def on_right_click(x, y):
    create_ball(x, y, radius)

def create_line(x1,y1,x2,y2):
    line = Line(x1,y1,x2,y2)
    lines.append(line)
    line.draw()

def on_left_click(x,y):
    global first_click, xpos1, ypos1,xpos2,ypos2
    if first_click:
        xpos1 = x
        ypos1 = y
        first_click = False
    else:
        xpos2 = x
        ypos2 = y
        create_line(xpos1,ypos1,xpos2,ypos2)
        first_click = True
        print(xpos1,ypos1,xpos2,ypos2)

def on_a_click():
    global radius
    radius += 1

def on_d_click():
    global radius
    radius -= 1

def on_z_click():
    global sleep
    sleep += 0.001

def on_c_click():
    global sleep
    if sleep>=0:
        return
    sleep -= 0.001

screen.onscreenclick(on_right_click, 3)
screen.onscreenclick(on_left_click, 1)
screen.onkeypress(on_a_click,"a")
screen.onkeypress(on_d_click,"d")
screen.onkeypress(on_z_click,"z")
screen.onkeypress(on_c_click,"c")
screen.listen()

while True:
    turtle.clear()
    surface.draw()
    for ball in balls:
        if ball.active:
            ball.move()
            ball.check_collision(surface)
        ball.draw()
    for line in lines:
        line.draw()
    screen.update()
    time.sleep(sleep)

turtle.done()