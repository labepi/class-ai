import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

import time
import cairo
from math import pi

WIDTH = 256
HEIGHT = 256

X_AND = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_AND = [0, 0, 0, 1]

X_OR = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_OR = [0, 1, 1, 1]

WEIGHTS = [1.0, 1.0, -1.5]

def f_step(value):
    """
    """
    if value > 0:
        return 1.0
    return 0.0

def f_line(x, w0, w1, w2, bias=1.0):
    """
    """
    return (-(w1 * x) / w2) - ((w0 * bias) / w2)

def perceptron(X, Y, learning_rate=0.001, bias=1.0):
    """
    """
    global WEIGHTS
    w0, w1, w2 = WEIGHTS

    for i in range(len(X)):
        x1, x2 = X[i]
        d = Y[i]

        y = f_step((w0 * bias) + (x1 * w1) + (x2 * w2))
        print(w0, w1, w2, x1, x2, d, y, f_line(x1, w0, w1, w2, bias))

        w0 = w0 + learning_rate * (d - y) * bias
        w1 = w1 + learning_rate * (d - y) * x1
        w2 = w2 + learning_rate * (d - y) * x2

    WEIGHTS = [w0, w1, w2]

def draw(context, width, height):
    """
    This is the draw function, that will be called every time `queue_draw` is
    called on the drawing area. Currently, this is setup to be every frame, 60
    times per second, but you can change that by changing line 95. 
    
    Ported from the first example here, with minimal changes:
    https://www.cairographics.org/samples/
    context - cairo.Context
    """
    global WEIGHTS, X_AND, Y_AND
    X = X_AND
    Y = Y_AND

    perceptron(X, Y)
    w0, w1, w2 = WEIGHTS

    context.set_source_rgb(0.6, 0.6, 0.6)
    context.rectangle(0, 0, 256, 256)
    context.fill()

    context.set_source_rgb(1.0, 1.0, 1.0)
    context.rectangle(28, 28, 200, 200)
    context.fill()

    for i in range(len(X)):
        x1, x2 = X[i]
        d = Y[i]
        context.set_source_rgb(d, 0.0, 0.0)
        context.rectangle(28 + 200 * x1 - 2, 28 + 200 * x2 - 2, 4, 4)
        context.fill()

    context.set_source_rgb(0.0, 0.0, 1.0)
    context.move_to(0, 256 * f_line(0, w0, w1, w2))
    context.line_to(256, 256 * f_line(1, w0, w1, w2))
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

def on_mouse_pressed(da, event, *data):
    """
    This is called when the mouse is pressed
    """
    print("The mouse was pressed!")

def main():
    """
    The main function
    """

    # Create a window, set it up to quit on close
    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_default_size(WIDTH, HEIGHT)

    # Create a DrawingArea, add it to the window, and connect it to the
    # `on_draw` function
    drawing_area = Gtk.DrawingArea()
    win.add(drawing_area)
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
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
