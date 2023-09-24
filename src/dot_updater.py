from vector import TwoDimensionalVector
from dot import Dot
from mouse import Mouse
import math

# TODO this need to be improved 
class EnvironmentDotUpdater:
    '''
        This class groups together various dot updates not related to Lines.

        width:
            the width of the pyglet window
        height:
            the height of the pyglet window

    '''

    def __init__(self, width: float, height: float):
        # TODO: add configuration for the constants used in the class
        self.width = width
        self.height = height
        
    def update(self, dot: Dot, mouse: Mouse):
        '''
            Currently handles 3 unrelated updates:
            1. updates replusive force from clicking the mouse
            2. limits the velocity of a dot
            3. wraps the dots around the window
            
            dot:
                a dot object
            mouse:
                a mouse object

        '''
        
        # handles the mouse press
        if mouse.pressed:
            distance = mouse.position.distance(dot.position)
            direction = (dot.position - mouse.position) * (1 / distance)
            force_magnitude = min((1/distance)**2 * 1000000, 1000)
            dot.force += direction * force_magnitude

        # limits the velocity 
        if TwoDimensionalVector(0, 0).distance(dot.velocity) > 50:
            dot.force += -1 * dot.velocity

        # when a dot goes out of the window from one side, it appears from another side
        def fmod_positive(x, y):
            return math.fmod(math.fmod(x, y) + y, y)
        dot.position.x = fmod_positive(
            dot.position.x + 50, self.width + 100) - 50
        dot.position.y = fmod_positive(
            dot.position.y + 50, self.height + 100) - 50