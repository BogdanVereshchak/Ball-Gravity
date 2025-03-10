import math

class Vector3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)


    def __rmul__(self, other):
        return self * other
    
    def __rmul__(self, scalar):
        return self * scalar
    
    def dot(self, p_with):
        return self.x * p_with.x + self.y * p_with.y + self.z * p_with.z

class Vector2i:
    def __init__(self, x = 0, y = 0):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector2i(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2i(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2i(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar

class Basis:
    def __init__(self, *args):
        if len(args) == 0:
            self.matrix = [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        elif len(args) == 1:
            self.matrix = args[0]
        elif len(args) == 9:
            self.set(*args)
        else:
            raise ValueError("Invalid number of arguments")

    def __str__(self):
        return f"[{self.matrix}]"

    def set(self, ax, bx, cx, ay, by, cy, az, bz, cz):
        self.matrix = [[ax, bx, cx], [ay, by, cy], [az, bz, cz]]
  
    def xform(self, vector : Vector3):
        rows = self.matrix
        return Vector3(
            vector.dot(Vector3(rows[0][0], rows[0][1], rows[0][2])),
            vector.dot(Vector3(rows[1][0], rows[1][1], rows[1][2])),
            vector.dot(Vector3(rows[2][0], rows[2][1], rows[2][2]))
        )

    def tdotx(self, v : list) -> float:
        matrix = self.matrix
        return matrix[0][0] * v[0] + matrix[1][0] * v[1] + matrix[2][0] * v[2]

    def tdoty(self, v : list) -> float:
        matrix = self.matrix
        return matrix[0][1] * v[0] + matrix[1][1] * v[1] + matrix[2][1] * v[2]
    
    def tdotz(self, v : list) -> float:
        matrix = self.matrix
        return matrix[0][2] * v[0] + matrix[1][2] * v[1] + matrix[2][2] * v[2]

    def __mul__(self, other):
        rows = self.matrix
        return Basis(
            other.tdotx(rows[0]), other.tdoty(rows[0]), other.tdotz(rows[0]),
 			other.tdotx(rows[1]), other.tdoty(rows[1]), other.tdotz(rows[1]),
 			other.tdotx(rows[2]), other.tdoty(rows[2]), other.tdotz(rows[2]))
        
    def __rmul__(self, other):
        rows = self.matrix
        self.set(
            other.tdotx(rows[0]), other.tdoty(rows[0]), other.tdotz(rows[0]),
 			other.tdotx(rows[1]), other.tdoty(rows[1]), other.tdotz(rows[1]),
 			other.tdotx(rows[2]), other.tdoty(rows[2]), other.tdotz(rows[2]))

    def rotate_euler(self, euler : Vector3):
        c = math.cos(euler.x)
        s = math.sin(euler.x)
        xmat = Basis(1, 0, 0, 0, c, -s, 0, s, c)

        c = math.cos(euler.y)
        s = math.sin(euler.y)
        ymat = Basis(c, 0, s, 0, 1, 0, -s, 0, c)
        
        c = math.cos(euler.z)
        s = math.sin(euler.z)
        zmat = Basis(c, -s, 0, s, c, 0, 0, 0, 1)
        matrix = xmat * ymat * zmat
        self.matrix = matrix.matrix
        

class Transform:
    def __init__(self, position : Vector3, basis : Basis):
        self.position = position
        self.basis = basis

    def __str__(self):
        return f"Position: {self.position}, Matrix: {self.basis}"
    
    def rotate(self, to : Vector3):
        self.basis.rotate_euler(to)

class CubeMesh:
    def __init__(self, size):
        self.size = size
        half_size = size / 2
        self.vertices = [Vector3(half_size, half_size, half_size),
                  Vector3(half_size, half_size, -half_size),
                  Vector3(half_size, -half_size, -half_size),
                  
                  Vector3(half_size, -half_size, -half_size),
                  Vector3(half_size, -half_size, half_size), 
                  Vector3(half_size, half_size, half_size),
                  
                  Vector3(-half_size, half_size, -half_size),
                  Vector3(-half_size, half_size, half_size),
                  Vector3(-half_size, -half_size, -half_size),
                  
                  Vector3(-half_size, half_size, half_size),
                  Vector3(-half_size, -half_size, -half_size),
                  Vector3(-half_size, -half_size, half_size), 
                  
                  Vector3(half_size, half_size, half_size),
                  Vector3(-half_size, half_size, half_size),
                  Vector3(-half_size, -half_size, half_size),
                  
                  Vector3(-half_size, -half_size, half_size),
                  Vector3(half_size, -half_size, half_size),
                  Vector3(half_size, half_size, half_size),
                  
                  Vector3(half_size, half_size, -half_size),
                  Vector3(-half_size, half_size, -half_size),
                  Vector3(-half_size, -half_size, -half_size),
                  
                  Vector3(-half_size, -half_size, -half_size),
                  Vector3(half_size, -half_size, -half_size),
                  Vector3(half_size, half_size, -half_size),
                  
                  Vector3(half_size, half_size, half_size),
                  Vector3(half_size, half_size, -half_size),
                  Vector3(-half_size, half_size, -half_size),
                  
                  Vector3(-half_size, half_size, -half_size),
                  Vector3(-half_size, half_size, half_size),
                  Vector3(half_size, half_size, half_size),
                  
                  Vector3(half_size, -half_size, half_size),
                  Vector3(half_size, -half_size, -half_size),
                  Vector3(-half_size, -half_size, -half_size),
                  
                  Vector3(-half_size, -half_size, -half_size),
                  Vector3(-half_size, -half_size, half_size),
                  Vector3(half_size, -half_size, half_size),
                  ]
        
        
class SphereMesh:
    def __init__(self, radius : float, accuracy : float):
        self.radius = radius
        self.accuracy = accuracy
        self.vertices = self._generate_mesh()
        
    def _generate_mesh(self):
        vertices = []
        radius = self.radius
        
        # x=r⋅sin(ϕ)⋅cos(θ)
        # y=r⋅sin⁡(ϕ)⋅sin⁡(θ)
        # z=r⋅cos⁡(ϕ)
        for i in range(0, 628, int(1 + 10 / self.accuracy)):
            f_i = i / 100
            cos_i = math.cos(f_i)
            sin_i = math.sin(f_i)
            for j in range(0, 628, int(1 + 10 / self.accuracy)):
                f_j = j / 100
                cos_j = math.cos(f_j)
                sin_j = math.sin(f_j)
                
                vert = Vector3(radius * sin_j * cos_i, radius * cos_j * cos_i, radius * sin_i)
                vertices.append(vert)
            
        # fill the array of vertices perpendicular to other triangles.
        for i in range(0, 628, int(1 + 10 / self.accuracy)):
            f_i = i / 100
            cos_i = math.cos(f_i)
            sin_i = math.sin(f_i)
            for j in range(0, 628, int(1 + 10 / self.accuracy)):
                f_j = j / 100
                cos_j = math.cos(f_j)
                sin_j = math.sin(f_j)
                
                vert = Vector3(radius * sin_i * cos_j, radius * cos_i * cos_j, radius * sin_j)
                vertices.append(vert)
        
        length_remainder = len(vertices) % 3        
        if length_remainder == 1:
            vertices.pop(len(vertices) - 1)
        elif length_remainder == 2:
            vertices.pop(len(vertices) - 1)
            vertices.pop(len(vertices) - 1)
    
        
        vertices.append(vertices[-1])
        vertices.append(vertices[0])
        vertices.append(vertices[-1])

        return vertices

class Object:
    def __init__(self, transform : Transform, aabb):
        self.transform = transform
        self.aabb = aabb
from turtle import *

import turtle
import time

basis = Basis([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
transform = Transform(Vector3(100, 100, -200), basis)
cube = Object(transform, SphereMesh(100, 0.25))

turtle.hideturtle()

screen = turtle.Screen()
screen.tracer(0)

def draw_line(x1, y1, x2, y2):
    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)

def main():
    fps = float(144)
    frameDelay = 1000 / fps
    turtle.speed(0)
    turtle.hideturtle()  
    
    screen.title('3D render')
    screen.setup(width=0.75, height=0.75)
    screen.bgcolor('#729EFF')
    turtle.color("#FFFFFF")
    frametime = float(frameDelay)
    frameStart = float()
    while True:
        frameStart = time.time()
        turtle.clear()
        update(frametime)
        render(frametime)
        frametime = time.time() - frameStart
        if frameDelay > frametime: 
            time.sleep((frameDelay - frametime) / 1000)
        screen.update() 

x2 = float(10)      
y2 = float(10)
rotation_speed = Vector3(1, 1, 1) # In radians.
start_rotation = Vector3()

def render(delta):
    global cube
    position = cube.transform.position
    vertices = cube.mesh.vertices
    d = 1000
    xform_vertices_2d = []
    for vert in vertices: # IDK How to use turtle and vertex shader.
        xvert = transform.basis.xform(vert)
        
        fx = 55.08 + d * (position.x - 600 + xvert.x) / (xvert.z + position.z + d)
        fy = 18.08 + d * (position.y - 150 + xvert.y) / (xvert.z + position.z + d)
        
        xform_vertices_2d.append(Vector2i(fx, fy))

    for i in range(int(len(xform_vertices_2d) / 3)):
        loc = i * 3 
        draw_line(xform_vertices_2d[loc].x, xform_vertices_2d[loc].y, xform_vertices_2d[loc + 1].x, xform_vertices_2d[loc + 1].y)
        draw_line(xform_vertices_2d[loc + 1].x, xform_vertices_2d[loc + 1].y, xform_vertices_2d[loc + 2].x, xform_vertices_2d[loc + 2].y)
        draw_line(xform_vertices_2d[loc + 2].x, xform_vertices_2d[loc + 2].y, xform_vertices_2d[loc].x, xform_vertices_2d[loc].y)    
    
    
def update(delta):
    global cube
    global rotation_speed
    global start_rotation
    cube.transform.rotate(start_rotation)
    start_rotation += rotation_speed * delta
    
    x, y = screen.getcanvas().winfo_pointerxy()
    y = screen.getcanvas().winfo_height() - y
    cube.transform.position = Vector3(x, y, cube.transform.position.z)

def input(key):
    global cube
    global rotation_speed
    
    if key == "q":
        rotation_speed.x += 0.5
    elif key == "a":
        rotation_speed.x -= 0.5
        
    elif key == "w":
        rotation_speed.y += 0.5
    elif key == "s":
        rotation_speed.y -= 0.5
        
    elif key == "e":
        rotation_speed.z += 0.5
    elif key == "d":
        rotation_speed.z -= 0.5
    
    elif key == "k":
        cube.transform.position.z -= 10
    elif key == "l":
        cube.transform.position.z += 10
    elif key == "c":
        if isinstance(cube.mesh, SphereMesh):
            cube.mesh = CubeMesh(100)
        else:
            cube.mesh = SphereMesh(100, 0.25)


screen.listen()

screen.onkeypress(lambda: input("k"), "k")
screen.onkeypress(lambda: input("l"), "l")
screen.onkeypress(lambda: input("c"), "c")

screen.onkeypress(lambda: input("q"), "q")
screen.onkeypress(lambda: input("a"), "a")

screen.onkeypress(lambda: input("w"), "w")
screen.onkeypress(lambda: input("s"), "s")

screen.onkeypress(lambda: input("e"), "e")
screen.onkeypress(lambda: input("d"), "d")

if __name__ == "__main__":
    main()

