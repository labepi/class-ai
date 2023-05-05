import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

import time
import cairo
import random
from math import pi

X_AND = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_AND = [0, 0, 0, 1]

X_OR = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_OR = [0, 1, 1, 1]

X_XOR = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_XOR = [0, 1, 1, 0]

def f_signal(value):
    """
    """
    if value > 0:
        return 1.0
    return -1.0

def f_step(value):
    """
    """
    if value > 0:
        return 1.0
    return 0.0

def f_rand():
    """
    """
    return 2 * random.random() - 1

class Perceptron:
    """
    """
    def __init__(self, X, Y, learning_rate=0.001, bias=1.0):
        """
        """
        self.training_set = X
        self.desired_set = Y
        self.set_size = len(self.training_set)
        self.bias = bias
        self.weights = [-0.5, 0.0, 1.0]
        self.f_activation = f_step
        self.learning_rate = learning_rate
        self.change = 1.0

    def rand_weights(self):
        """
        """
        self.weights = [f_rand(), f_rand(), f_rand()]

    def learn(self):
        """
        """
        w0, w1, w2 = self.weights
 
        order = random.sample(list(range(self.set_size)), self.set_size)
        self.change = 0.0
        for i in order:
            x1, x2 = self.training_set[i]
            d = self.desired_set[i]
 
            y = self.f_activation((w0 * self.bias) + (x1 * w1) + (x2 * w2))
 
            if d != y:
                self.change = 1.0
 
            w0 = w0 + self.learning_rate * (d - y) * self.bias
            w1 = w1 + self.learning_rate * (d - y) * x1
            w2 = w2 + self.learning_rate * (d - y) * x2

        self.weights = [w0, w1, w2]

def draw(context, width, height):
    """
    This is the draw function, that will be called every time `queue_draw` is
    called on the drawing area. Currently, this is setup to be every frame, 60
    times per second, but you can change that by changing line 95. 
    
    Ported from the first example here, with minimal changes:
    https://www.cairographics.org/samples/
    context - cairo.Context
    """
    neuron.learn()
    w0, w1, w2 = neuron.weights

    context.set_source_rgb(0.6, 0.6, 0.6)
    context.rectangle(0, 0, 256, 256)
    context.fill()

    context.set_source_rgb(1.0, 1.0, 1.0)
    context.rectangle(28, 28, 200, 200)
    context.fill()

    for i in range(neuron.set_size):
        x1, x2 = neuron.training_set[i]
        d = neuron.desired_set[i]
        context.set_source_rgb(d, 0.0, 0.0)
        context.rectangle(28 + 200 * x1 - 5, 28 + 200 * x2 - 5, 10, 10)
        context.fill()

    slope = -(w1 / w2)
    delta = -(w0 / w2) * neuron.bias

    context.set_source_rgb(neuron.change, 1.0, 0.0)
    xo, yo = 28 - 1 * 200, 28 + 200 * (-1 * slope + delta)
    xd, yd = 28 + 2 * 200, 28 + 200 * (2 * slope + delta)
    context.move_to(xo, yo)
    context.line_to(xd, yd)
    context.stroke()

def on_draw(drawing_area, context):
    """
    A callback called every time `drawingarea.queue_draw` is called.
    area - Gtk.DrawingArea
    context - cairo.Context
    """
    allocation = drawing_area.get_allocation()
    width = allocation.width
    height = allocation.height

    draw(context, width, height)

def on_mouse_pressed(drawing_area, event, *data):
    """
    This is called when the mouse is pressed
    """
    neuron.rand_weights()

def create_window(width, height):
    """
    The main function
    """
    # Create a window, set it up to quit on close
    window = Gtk.Window()
    window.set_title("Perceptron")
    window.connect('destroy', Gtk.main_quit)
    window.set_default_size(width, height)

    # Create a DrawingArea, add it to the window, and connect it to the
    # `on_draw` function
    drawing_area = Gtk.DrawingArea()
    window.add(drawing_area)
    drawing_area.connect('draw', on_draw)

    # Add a button pressed event, and connect it to the `on_mouse_pressed`
    # callback
    drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
    drawing_area.connect('button-press-event', on_mouse_pressed)

    # Tell the drawing area to render
    drawing_area.queue_draw()

    def refresh_screen():
        drawing_area.queue_draw()
        GLib.timeout_add(1000 / 60, refresh_screen)

    # Normally, GUI Libraries don't automatically redraw the screen every
    # frame. In order to do that, I've setup a timer to call `refresh_screen`
    # in 16.666 milliseconds (60 FPS). `refresh_screen`, queues a draw command
    # to re-draw the drawing area and then re-adds the timer for the next
    # frame. This might seem like a hack, but its more-or-less the "correct"
    # way to implement this.
    # 
    # If this is not the behavior you want (perhaps you only want your fractal
    # to re-draw when the mouse button is pressed), remove this line and the
    # `refresh_screen` function, and call `drawing_area.queue_draw()`.from
    # somewhere else 
    GLib.timeout_add(1000 / 60, refresh_screen)

    # Show the window
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    """
    """
    neuron = Perceptron(X_AND, Y_AND)
    create_window(256, 256)
