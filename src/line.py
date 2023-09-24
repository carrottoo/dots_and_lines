from dot import Dot
from typing import Any
import pyglet


class DotForceCalculator:
    '''
        A calculator to calculate the force to be applied between two dots depending on their distance.

        neutral distance: 
            When the distance is smaller than the neutral_distance, calculate will return a negative number
            (the dots will repel each other). When the distance is larger than the neutral_distance,
            calculate will return a positive number (the dots will attract each other). At neutral_distance
            there is no force.
        
        max_distance:
            Maximum distance between two dots to have force interaction. At distances larger than max_distance, 
            there is no force.

        force_coefficient:
            Coefficient controlling the strength of the force.
    '''
    def __init__(self, neutral_distance: float, max_distance: float, force_coefficient: float):
        self.neutral_distance = neutral_distance
        self.max_distance = max_distance
        self.force_coefficient = force_coefficient

    def calculate(self, distance: float) -> float:
        '''
            Calculates the force between two dots. When the distance is larger than the maximum distance, there will 
            not a force between them anymore. 

            distance: the distance between two dots 

            Returns the force between two dots 
        '''
        if distance <= self.max_distance:
            return self.force_coefficient * (distance - self.neutral_distance)
        return 0.0
    

class LineDrawObject:
    '''
        A class to draw lines between the dots 

        batch: 
            a pyglet batch in which we will draw the lines
        shape: 
            a pyglet shape 
        width: 
            the width of the lines
        color: 
            the color of the line, a tuple of integers (R, G, B, A). A is the opaqueness of the line.
        min_scale_length: 
            minimum length of the transparency scaling 
        max_scale_length: 
            maximum length of the transparency scaling, at which the line gets full transparent 

    '''

    def __init__(self, batch: pyglet.graphics.Batch, width: float, color: tuple, min_scale_length, max_scale_length):
        self.batch = batch
        self.shape = None
        self.width = width
        self.color = color
        self.min_scale_length = min_scale_length
        self.max_scale_length = max_scale_length

    def _get_color(self, distance: float) -> tuple:
        '''
            Protected method to return the color of the line based on the distance between two dots 
            
            distance: the distance between the dots 

            Returns the color of the line as a tuple 
        '''
        return self.color[:-1] + (int(255*self._scaling(distance)), )

    def _scaling(self, distance: float) -> float:
        '''
            Protected method to scale the transparency of the lines based on the distance between two dots. When the 
            distance is smaller than the minimum scale length it would directly return 0, which means that the line is
            fully untransparent

            distance: the distance between the dots

            Returns the alpha level in RGBA as a float number 

        '''
        if distance > self.min_scale_length:
            return max(1 - (distance - self.min_scale_length) * (1 / (self.max_scale_length - self.min_scale_length)), 0)
        return 1.0

    def update(self, start: Dot, end: Dot):
        '''
            Updates the position of the line based on the start dot and end dot 
        '''

        distance = start.position.distance(end.position)
        
        # drawing invisible lines makes the code very slow!
        if distance > self.max_scale_length:
            # assigning None to shape also deletes the shape from the batch
            # this speeds up the app since we do not draw invisible lines
            self.shape = None
            return

        # when we need to draw the lines, we first check if the old line stil exists. If not, we create a new line. If yes, 
        # we just update the line (we could also just always create a new line, but this might be slower)
        if self.shape is None:
            self.shape = pyglet.shapes.Line(x=start.position.x, y=start.position.y,
                                            x2=end.position.x, y2=end.position.y, width=self.width,
                                            color=self._get_color(distance), batch=self.batch)
        else:
            self.shape.x = start.position.x
            self.shape.y = start.position.y
            self.shape.x2 = end.position.x
            self.shape.y2 = end.position.y
            self.shape.color = self._get_color(distance)
            self.shape.width = self.width


class Line:
    '''
        Constructs a Line object. Each line has a start point, end point and a force calculator and a draw object.

        start: 
            the start point(dot)
        end:
            the end point(dot)
        dot_force_calculator:
            to map the dot distance to force magnitude
        line_draw_object:
            to draw the lines 

    '''

    def __init__(self, start: Dot, end: Dot, dot_force_calculator: DotForceCalculator, line_draw_object: LineDrawObject = None):
        self.start = start
        self.end = end
        self.dot_force_calculator = dot_force_calculator
        self.line_draw_object = line_draw_object

    def update_state(self):
        '''
            Update the state of the start and end dots 
        '''

        distance = self.start.position.distance(self.end.position)

        # Optimization: skip calculations when the distance is too large
        if distance > self.dot_force_calculator.max_distance:
            return

        self._apply_dot_force(self.start, self.end, distance)
        self._apply_dot_force(self.end, self.start, distance)

    def _apply_dot_force(self, dot1: Dot, dot2: Dot, distance: float):
        '''
            Protected method to apply the force to the dot1 based on the distance
        '''

        force_strength = self.dot_force_calculator.calculate(distance)
        dot1.force += force_strength * (dot2.position - dot1.position) / distance

    def update_draw_object(self):
        '''
            Update the line draw object depending on the start dot and end dot 
        '''

        self.line_draw_object.update(self.start, self.end)
