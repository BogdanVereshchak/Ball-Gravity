import turtle
import math
from ground import *
from line import *

class Ball:
    def __init__(self, x, y, vx, vy, radius):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.active = True

    def draw(self):
        turtle.penup()
        turtle.goto(self.x, self.y - self.radius)
        turtle.pendown()
        turtle.circle(self.radius)

    def move(self):
        self.vy -= 0.5  # Гравітація
        self.x += self.vx
        self.y += self.vy

    def check_collision(self, surface):
        ground_y = surface.get_y(self.x)
        if self.y - self.radius <= ground_y:
            self.y = ground_y + self.radius
            normal_angle = surface.get_normal_angle(self.x)
            self.bounce(normal_angle)

        # Відбиття від лівої та правої стін екрану
        if self.x + self.radius >= 600 or self.x - self.radius <= -600:
            self.vx = -self.vx * 0.95
            self.x = max(min(self.x, 600 - self.radius), -600 + self.radius)
        
        for line in lines:
            if self.line_collision(line):
                normal_angle = self.get_line_normal_angle(line)
                self.bounce(normal_angle)

                self.x += math.cos(math.pi / 2) * 0.95
                self.y += math.sin(math.pi / 2) * 0.95
                break

    def line_collision(self, line):
        # Compute the closest point on the line segment to the ball center
        line_vec = (line.x2 - line.x1, line.y2 - line.y1)
        pnt_vec = (self.x - line.x1, self.y - line.y1)
        line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
        line_unitvec = (line_vec[0] / line_len, line_vec[1] / line_len)
        proj_len = pnt_vec[0] * line_unitvec[0] + pnt_vec[1] * line_unitvec[1]
        closest_pnt = (line.x1 + proj_len * line_unitvec[0], line.y1 + proj_len * line_unitvec[1])

        # Clamp the closest point to the line segment
        closest_pnt = (max(min(closest_pnt[0], max(line.x1, line.x2)), min(line.x1, line.x2)),
                       max(min(closest_pnt[1], max(line.y1, line.y2)), min(line.y1, line.y2)))

        dist_to_line = math.sqrt((closest_pnt[0] - (self.x))**2 + (closest_pnt[1] - self.y)**2)
        return dist_to_line <= self.radius+1
    
    def get_line_normal_angle(self, line):
        line_angle = math.atan2(line.y2 - line.y1, line.x2 - line.x1)
        normal_angle = line_angle + math.pi / 2
        return normal_angle

    def bounce(self, normal_angle):
        speed = math.sqrt(self.vx**2 + self.vy**2)
        incidence_angle = math.atan2(self.vy, self.vx)
        reflection_angle = normal_angle + incidence_angle
        self.vx = speed * math.cos(reflection_angle) * 0.9  # Зменшення швидкості для врахування втрат енергії
        self.vy = speed * math.sin(reflection_angle) * 0.9
        if abs(self.vx) < 0.1:  # Зупиняємо м'яч, якщо швидкість дуже мала
            self.vy = 0
            self.vx = 0
            self.active = False

