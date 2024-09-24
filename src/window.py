# window.py
#
# Copyright 2024 Robson Cardoso dos Santos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gio, Gtk
import cairo

@Gtk.Template(filename='src/codarium.ui')
# @Gtk.Template(filename='src/window.ui')
# @Gtk.Template(resource_path='/com/blacktomato/Codarium/codarium.ui')
class CodariumWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CodariumWindow'

    # label = Gtk.Template.Child()
    canvas = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.set_draw_func(self.on_draw)
        e = Gtk.GestureClick.new()
        e.connect("pressed", self.on_click)
        self.canvas.add_controller(e)
        self.blocks = []

    @Gtk.Template.Callback()
    def on_draw(self, area, ctx, width, height):
        ctx.set_source_rgb(0.9, 0.9, 1)
        ctx.paint()
        # self.triangle(ctx)
        for x, y in self.blocks:
            self.triangle(ctx)

    def on_click(self, gesture, data, x, y):
        self.blocks.append((x,y))
        self.canvas.queue_draw()

    def triangle(self, ctx):
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(100, 0)
        ctx.rel_line_to(30, 2 * 30)
        ctx.rel_line_to(-2 * 30, 0)
        ctx.close_path()
        ctx.stroke()