import math

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk


class CustomGesture(Gtk.Gesture):
    __gtype_name__ = 'CustomGesture'

    def __init__(self, drawing_area):
        super().__init__()
        self.connect("pressed", self.on_clicked)
        self.ctrl_pressed = False
        drawing_area.connect("key-press-event", self.on_key_press)

    def on_clicked(self, gesture, n_press, x, y):
        if self.ctrl_pressed:
            print("Ctrl+clique detectado em x={}, y={}".format(x, y))
            # Desenhar algo especial no canvas, por exemplo
            ctx = self.get_widget().get_window().create_cairo_context()
            ctx.set_source_rgb(1, 0, 0)  # Cor vermelha
            ctx.arc(x, y, 10, 0, 2 * math.pi)
            ctx.fill()
        else:
            print("Clique simples detectado em x={}, y={}".format(x, y))
            # Desenhar algo diferente, por exemplo
            ctx = self.get_widget().get_window().create_cairo_context()
            ctx.set_source_rgb(0, 0, 1)  # Cor azul
            ctx.arc(x, y, 5, 0, 2 * math.pi)
            ctx.fill()
        self.ctrl_pressed = False

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Control_L:
            self.ctrl_pressed = True