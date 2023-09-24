from vector import TwoDimensionalVector
from typing import Any
import pyglet
import random


class Dot:
    '''
        position:
            The current position of the dot expressed as a TwoDimensionalVector (x, y)
        force:
            The force to be applied to the dot expressed as a TwoDimensionalVector (force on x-axis and y-axis). This is reset always by add_force.
        velocity:
            The current velocity of the dot expressed as a TwoDimensionalVector (velocity on x-axis and y-axis).
        radius:
            Radius of the dot. It is only used to decide the thickness of the line between two dots.
        sprite:
            The pyglet Sprite which is used to draw the dot.
    '''

    def __init__(self, position: TwoDimensionalVector, velocity: TwoDimensionalVector,
                 radius: float, sprite: pyglet.sprite.Sprite):
        self.position = position
        self.force = TwoDimensionalVector(0.0, 0.0)  # force
        self.velocity = velocity
        self.radius = radius
        self.sprite = sprite  # each sprite is an object from pyglet to draw the dot 

    def add_force(self, force: TwoDimensionalVector):
        '''
            Adds force to the dot 
        '''
        self.force = self.force + force

    def update_state(self, delta_time: float):
        '''
            Updates the status of the dot object.

            delta_time: time since last update
        '''
        # new position is decided by the distance covered (velocity * travelling time)
        self.position = self.position + self.velocity * delta_time

        # assuming the dots have mass = 1, we have
        # acceleration = force / mass = force
        # we then apply this acceleration for delta_time to the dot
        self.velocity = self.velocity + self.force * delta_time

        # after updating the state, force is set back to 0 to avoid accumlation in force
        self.force = TwoDimensionalVector(0.0, 0.0)

    def update_sprite(self):
        '''
            Updates the position of the sprite
        '''
        self.sprite.x = self.position.x
        self.sprite.y = self.position.y


class DotFactory:
    '''
        Dot factory to create random dots for the app

        image: a pyglet.image that is used to draw the dot 
        area_width: the width of the pyglet window, which is the maximum x coordinate where the dot can be 
        area_height: the height of the pyglet window, which is the maximum y coordinate where the dot can be
        min_size: the minimum size of the dot
        max_size: the maximum size of the dot 
        max_velocity: the maximum velocity of the dot
    '''

    def __init__(self, image: pyglet.image, area_width: float, area_height: float, min_size: float, max_size: float, max_velocity: float):
        self.image = image
        self.area_width = area_width
        self.area_height = area_height
        self.min_size = min_size
        self.max_size = max_size
        self.max_velocity = max_velocity

    def create(self, batch: pyglet.graphics.Batch):
        '''
            Creates random dots in batch 
        '''

        position = TwoDimensionalVector(
            random.random()*self.area_width, random.random()*self.area_height)
        
        velocity = TwoDimensionalVector(
            (random.random() - 0.5)*self.max_velocity, (random.random() - 0.5)*self.max_velocity)
        
        radius = (random.random()*(self.max_size - self.min_size) + self.min_size)

        sprite = pyglet.sprite.Sprite(self.image, batch=batch)
        # rescales the sprite to have a height that equals 2 * radius
        scale = radius * 2 / sprite.height
        sprite.scale_x = scale
        sprite.scale_y = scale

        return Dot(position, velocity, radius, sprite=sprite)
