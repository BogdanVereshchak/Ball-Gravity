import turtle
import random
import math
t = turtle

class Surface:
    def __init__(self):
        self.points = []
        self.generate_terrain()

    def generate_terrain(self):
        x = -600
        y=-300
        while x <= 600:
            y = random.randint(max(y-20,-300),y+20)
            self.points.append((x, y))
            x += 20

    def draw(self):
        t.hideturtle()
        t.fillcolor('#8C6F3E')
        t.begin_fill()
        t.teleport(-600, -400)
        for point in self.points:
            turtle.goto(point)
            turtle.pendown()
            t.setposition(point)
        t.setposition(600,-400)
        t.end_fill()


    def get_y(self, x):
        for i in range(len(self.points) - 1):
            if self.points[i][0] <= x <= self.points[i+1][0]:
                x1, y1 = self.points[i]
                x2, y2 = self.points[i+1]
                return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        return 0

    def get_normal_angle(self, x):
        for i in range(len(self.points) - 1):
            if self.points[i][0] <= x <= self.points[i+1][0]:
                x1, y1 = self.points[i]
                x2, y2 = self.points[i+1]
                angle = math.atan2(y2 - y1, x2 - x1)
                return angle + math.pi / 2
        return math.pi / 2
