import turtle
import math

lines = []

class Line:
    def __init__(self,x1,y1,x2,y2) -> None:
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

    def draw(self):
        turtle.penup()
        turtle.goto(self.x1, self.y1)
        turtle.dot(3)
        turtle.pendown()
        turtle.goto(self.x2, self.y2)
        turtle.dot(3)
        turtle.penup()

