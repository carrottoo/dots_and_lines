from typing import Any, Union
import pyglet
import math
import random
from mouse import create_and_bind_mouse, Mouse
from vector import TwoDimensionalVector
from dot import Dot, DotFactory
from line import Line, LineDrawObject, DotForceCalculator
from dot_updater import EnvironmentDotUpdater


def create_dots_and_lines(window: pyglet.window, line_batch: pyglet.graphics.Batch, dot_batch: pyglet.graphics.Batch):
    '''
        Constructs the Dot and Line objects for the app. We configure everythihg we need here. Later it can take an external configure file (e.g. .toml)

        window: a pyglet window 
        line_batch: a drawing batch for the lines, it is faster to render the lines in batch
        dot_batch: a drawing batch for the dots 

        Returns a pair of lists: (dots, lines)

    '''
    
    dot_image = pyglet.image.load('../images/dot_2.png')
    # uses dot image's center as the position of the dot
    dot_image.anchor_x = dot_image.width//2
    dot_image.anchor_y = dot_image.height//2

    # configures DotFactory to create dots 
    dot_factory = DotFactory(image=dot_image, area_width=window.width, area_height=window.height, 
                             min_size=5, max_size=10, max_velocity=50)

    dots = []
    lines = []

    # creates dots 
    for _ in range(100):
        dots.append(dot_factory.create(dot_batch))
    
    # configures the DotForceCalculator, which will be used by lines to apply forces to the dots
    dot_force_calculator = DotForceCalculator(neutral_distance=75, max_distance=150, force_coefficient=0.02)

    # creates lines
    for i in range(len(dots)):
        for j in range(i+1, len(dots)):
            start = dots[i]
            end = dots[j]
            line_draw_object = LineDrawObject(batch=line_batch, width=(start.radius + end.radius) / 2 / 3, color=(
                255, 255, 255, 255), min_scale_length=10, max_scale_length=150)
            lines.append(
                Line(start=start, end=end, dot_force_calculator=dot_force_calculator, line_draw_object=line_draw_object))
            
    return dots, lines


class App:
    '''
        Collects all the objects we have created into an app

        backgroud:
            the background of the app
        dots:
            dots to be drawn in the app
        lines:
            lines to be drawn in the app
        mouse:
            a mouse object through which we can click and apply a repelling force
        dot_updater:
            a EnvironmentDotUpdater that handles 3 different updates
        line_batch:
            a pyglet batch in which we would draw the lines
        dot_batch:
            a pyglet batch in which we would draw the dots 

    '''

    def __init__(self, background: pyglet.sprite.Sprite, dots: Dot, lines: Line, mouse: Mouse,
                 dot_updater: EnvironmentDotUpdater,
                 line_batch: pyglet.graphics.Batch, dot_batch: pyglet.graphics.Batch):

        self.background = background
        self.dots = dots
        self.lines = lines
        self.mouse = mouse
        self.dot_updater = dot_updater

        self.line_batch = line_batch
        self.dot_batch = dot_batch

    def update_state(self, delta_time: float):
        '''
            Updates the internal state of the app

            delta_time:
                the time passed since last state update 

        '''

        for line in self.lines:
            line.update_state()

        for dot in self.dots:
            self.dot_updater.update(dot, self.mouse)
            # Update internal state of the dot
            dot.update_state(delta_time)

    def draw(self):
        '''
            Draws all the objects in the app
        '''
        self.background.draw()

        for line in self.lines:
            line.update_draw_object()
        self.line_batch.draw()

        for dot in self.dots:
            dot.update_sprite()
        self.dot_batch.draw()


def create_and_bind_app(window: pyglet.window):
    '''
        Creates an app and binds it to the given window
    '''
    background = pyglet.image.load('../images/starry_sky_3.png')
    background_sprite = pyglet.sprite.Sprite(background)
    background_sprite.scale_x = 0.6
    background_sprite.scale_y = 0.6

    line_batch = pyglet.graphics.Batch()
    dot_batch = pyglet.graphics.Batch()

    dots, lines = create_dots_and_lines(window, line_batch, dot_batch)

    mouse = create_and_bind_mouse(window)
    dot_updater = EnvironmentDotUpdater(window.width, window.height)

    app = App(background_sprite, dots, lines, mouse,
              dot_updater, line_batch, dot_batch)

    fps_display = pyglet.window.FPSDisplay(window)

    @window.event
    def on_draw():
        window.clear()
        app.draw()
        fps_display.draw()

    pyglet.clock.schedule_interval(app.update_state, 1/120)
    

if __name__ == '__main__':
    # Create a pyglet window 
    window = pyglet.window.Window(width=1000, height=800, fullscreen=True)
    # Hack, pyglet has a bug that on MacOS it sometimes fails to focus on the window
    # going to fullscreen ensures we get focus on the window
    window.set_fullscreen(False)
    
    # Create an app and bind it to the window 
    create_and_bind_app(window)

    # Play background music
    player = pyglet.media.Player()
    sound = pyglet.media.load('../music/music_fx_starry_sky_of_summer.wav')
    player.queue(sound) 

    # keep playing in loops as long as the app is running:
    player.loop = True
    
    player.play()
    
    pyglet.app.run()
