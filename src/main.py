# TODO: this should not be needed in Python >= 3.10
from __future__ import annotations
from typing import Union
import pyglet
import math
import random

class TwoDimensionalVector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: TwoDimensionalVector) -> TwoDimensionalVector:
        return TwoDimensionalVector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: TwoDimensionalVector) -> TwoDimensionalVector:
        return TwoDimensionalVector(self.x - other.y, self.y - other.y)
    
    def __mul__(self, other: Union[TwoDimensionalVector, float]) -> TwoDimensionalVector:
        if isinstance(other, TwoDimensionalVector):
            return TwoDimensionalVector(self.x * other.x, self.y * other.y)
        else:
            return  self * TwoDimensionalVector(other, other)

    def distance(self, other: TwoDimensionalVector) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    


class Dot:
    def __init__(self, position: TwoDimensionalVector, velocity: TwoDimensionalVector):
        self.position = position
        self.velocity = velocity

    def update_position(self, delta_time: float):
        self.position = self.position + self.velocity * delta_time

     


class App:
    def __init__(self):
        self.dots = []
        for _ in range(100):
            position = TwoDimensionalVector(random.random()*1000, random.random()*1000) 
            velocity = TwoDimensionalVector((random.random() - 0.5)*50, (random.random() - 0.5)*50)
            self.dots.append(Dot(position, velocity))
        # self.dots = [Dot(random.random()*1000, random.random()*1000) for _ in range(100)]
        # self.dot_moves = [[(random.random() - 0.5)*50, (random.random() - 0.5)*50] for _ in range(100)]

    def update_state(self, delta_time):
        for i in range(len(self.dots)):
            self.dots[i].update_position(delta_time)


    def draw(self):
        for dot in self.dots:
            pyglet.shapes.Circle(dot.position.x, dot.position.y, 10, 10).draw()
        
        for i in range(len(self.dots)):
            for j in range(i+1, len(self.dots)):
                if self.dots[i].position.distance(self.dots[j].position) <= 100:
                    pyglet.shapes.Line(self.dots[i].position.x , self.dots[i].position.y, self.dots[j].position.x, self.dots[j].position.y).draw()


app = App()

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    app.draw()

pyglet.clock.schedule_interval(app.update_state, 1/120)

pyglet.app.run()