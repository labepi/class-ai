import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

import sys
import copy
import random
import neuron

X = [[0,0,1,0,0,
      0,1,0,1,0,
      0,1,1,1,0,
      0,1,0,1,0,
      0,1,0,1,0],

     [0,1,1,1,0,
      0,1,0,0,0,
      0,1,1,0,0,
      0,1,0,0,0,
      0,1,1,1,0],

     [0,1,1,1,0,
      0,0,1,0,0,
      0,0,1,0,0,
      0,0,1,0,0,
      0,1,1,1,0],

     [0,0,1,0,0,
      0,1,0,1,0,
      0,1,0,1,0,
      0,1,0,1,0,
      0,0,1,0,0],

     [0,1,0,1,0,
      0,1,0,1,0,
      0,1,0,1,0,
      0,1,0,1,0,
      0,0,1,0,0],

     [1,0,0,0,1,
      1,1,0,1,1,
      1,0,1,0,1,
      1,0,0,0,1,
      1,0,0,0,1],

     [1,0,0,0,1,
      1,0,0,0,1,
      1,1,1,1,1,
      1,0,0,0,1,
      1,0,0,0,1]]

#    A  E  I  O  U  M  H
Y = [0, 1, 0, 0, 0, 0, 0]

class Plot2DBoundary(Gtk.Window):
    """
    """
    def __init__(self, neuron, write_to_file=False, width=256, height=256):
        """
        """
        Gtk.Window.__init__(self)

        self.neuron = neuron
        self.width = width
        self.height = height
        self.refresh_rate = 1000 / 10
        self.write_to_file = write_to_file
        self.set_title("Perceptron")
        self.connect('destroy', Gtk.main_quit)
        self.set_default_size(self.width, self.height)

        # Create a DrawingArea, add it to the window, and connect it to the
        # `on_draw` function
        self.drawing_area = Gtk.DrawingArea()
        self.add(self.drawing_area)
        self.drawing_area.connect('draw', self.on_draw)

        # Add a button pressed event, and connect it to the `on_mouse_pressed`
        # callback
        self.drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect('button-press-event', self.on_mouse_pressed)
 
        # Tell the drawing area to render
        self.drawing_area.queue_draw()
        GLib.timeout_add(self.refresh_rate, self.refresh_screen)
 
        # Show the window
        self.show_all()
        Gtk.main()
 
    def refresh_screen(self):
        """
        """
        if self.neuron.changed == 1.0:
            self.neuron.learn()
            if self.write_to_file:
                self.save_drawing_to_file("%05d" % (self.neuron.count))
        self.drawing_area.queue_draw()
        GLib.timeout_add(self.refresh_rate, self.refresh_screen)

    def draw(self, context, width, height):
        """
        This is the draw function, that will be called every time `queue_draw`
        is called on the drawing area. Currently, this is setup to be every
        frame, 60 times per second.
        
        Ported from the first example here, with minimal changes:
        https://www.cairographics.org/samples/
        context - cairo.Context
        """
        self.neuron.weights
    
        context.set_source_rgb(0.0, 1 - self.neuron.changed, 0.0)
        context.rectangle(0, 0, 256, 256)
        context.fill()
    
        context.set_source_rgb(1.0, 1.0, 1.0)
        context.rectangle(28, 28, 200, 200)
        context.fill()

        b = max(self.neuron.weights)
        l = min(self.neuron.weights)
        weights = []
        for w in self.neuron.weights:
            v = (w - l) / (b - l)
            if w > 0:
                weights.append((0.0, 0.0, v))
            else:
                weights.append((v, 0.0, 0.0))

        x = 28
        y = 28
        for i in range(1, len(self.neuron.weights)):
            w = weights[i]
            context.set_source_rgb(w[0], w[1], w[2])
            context.rectangle(x, y, 30, 30)
            context.fill()
            x = x + 30
            if (i % 5 == 0):
                x = 28
                y = y + 30

        context.set_source_rgb(weights[0][0], weights[0][1], weights[0][2])
        context.rectangle(198, 198, 30, 30)
        context.fill()

        self.neuron.learn()
    
    def on_draw(self, drawing_area, context):
        """
        A callback called every time `drawing_area.queue_draw` is called.
        area - Gtk.DrawingArea
        context - cairo.Context
        """
        allocation = drawing_area.get_allocation()
        width = allocation.width
        height = allocation.height
    
        self.draw(context, width, height)
    
    def on_mouse_pressed(self, drawing_area, event, *data):
        """
        This is called when the mouse is pressed
        """
        n = self.neuron
        self.neuron = neuron.Perceptron(n.training_set, n.desired_set)
        self.neuron.rand_weights()

    def save_drawing_to_file(self, file_name):
        """
        """
        allocation = self.drawing_area.get_allocation()

        self.drawing_area.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                                       allocation.width,
                                                       allocation.height)

        context = cairo.Context(self.drawing_area.surface)

        context.rectangle(0, 0, allocation.width, allocation.height)
        context.set_source_rgb(1.0, 1.0, 1.0)
        context.fill()

        self.draw(context, allocation.width, allocation.height)

        self.drawing_area.surface.write_to_png(file_name + ".png")

        self.drawing_area.surface.flush()
        self.drawing_area.surface.finish()

def invert(a):
    """
    """
    return 1 - a 

def f_rand():
    """
    """
    return 2 * random.random() - 1

if __name__ == '__main__':
    """
    """
    rand = int(sys.argv[1])
    xset = copy.copy(X)
    yset = copy.copy(Y)
    while rand > 0:
        for i in range(len(X)):
            x = copy.copy(xset[i])
            for b in range(len(x)):
                x[b] = x[b] + f_rand() * 0.5
            xset.append(x)
            yset.append(yset[i])
        rand = rand - 1
    n = neuron.Perceptron(xset, yset)
    n.rand_weights()
    print(len(xset), len(yset), n.set_size)
    w = Plot2DBoundary(n)
