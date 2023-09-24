from vector import TwoDimensionalVector
import pyglet


def create_and_bind_mouse(window: pyglet.window):
    '''
        Creates a Mouse object and binds its methods to the window.
        
        window: 
            a pyglet window
    '''
    mouse = Mouse()

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        mouse.mouse_press(x, y, button)

    @window.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):
        mouse.mouse_drag(x, y, button)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        mouse.mouse_release(button)

    return mouse


class Mouse:
    '''
        A class to track the state of the mouse
        
        position: 
            position of the mouse. This is currently only valid if the mouse is pressed
        pressed: 
            True if the mouse is currently pressed and False otherwise.

        The methods mouse_press, mouse_drag and mouse_release should be bind
        to corresponding pyglet window events

    '''

    def __init__(self):
        self.position = TwoDimensionalVector(0., 0.)
        self.pressed = False

    def mouse_press(self, x, y, button):
        '''
            Updates the Mouse if the left mouse button was clicked

            x: 
                x-coordinate of the mouse
            y: 
                y-coordinate of the mouse
            button: 
                bitmask of the currently pressed buttons

        '''

        if button & pyglet.window.mouse.LEFT:
            self.position.x = x
            self.position.y = y
            self.pressed = True

    def mouse_drag(self, x, y, button):
        '''
            This is handled by invoking mouse_press
        '''
        self.mouse_press(x, y, button)

    def mouse_release(self, button):
        '''
            Updates the Mouse if the left button was released.
            
            button: 
                bitmask of the currently pressed buttons.
        '''
        if button & pyglet.window.mouse.LEFT:
            self.pressed = False
