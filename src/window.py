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

import json
from gi.repository import Adw, Gio, Gtk
import cairo

from .core.blocks.block import Block


@Gtk.Template(filename="src/splash.ui")
class SplashScreen(Adw.Window):
    __gtype_name__ = "Splash"

    # logo_image = Gtk.Template.Child("logo_image")
    # label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()
        # self.set_app_paintable(True)
        # self.set_decorated(False)
        # self.set_keep_above(True)
        # self.set_resizable(False)
        # self.set_opacity(0.1)

        # Adiciona uma imagem se disponível
        # self.logo_image.set_from_icon_name("your-app-logo", Gtk.IconSize.DIALOG)

        # Fechar splash depois de 3 segundos e abrir o app principal
        # GLib.timeout_add_seconds(3, self.close_splash)

    def close_splash(self):
        # Aqui você pode iniciar a janela principal
        self.close()
        return False  # Retorna False para parar o timeout


@Gtk.Template(filename='src/codarium.ui')
# @Gtk.Template(resource_path='/com/blacktomato/Codarium/codarium.ui')
class CodariumWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CodariumWindow'

    split_view = Gtk.Template.Child()
    canvas = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.set_draw_func(self.on_draw)
        e = Gtk.GestureClick.new()
        e.connect("pressed", self.on_click)
        self.canvas.add_controller(e)

        shortcut_controller = Gtk.ShortcutController()
        self.add_controller(shortcut_controller)

        # Definir atalho Ctrl+S para salvar
        save_shortcut = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>S"),
            Gtk.CallbackAction.new(self.on_save_trigger)
        )
        # Definir atalho Ctrl+O para abrir
        open_shortcut = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>O"),
            Gtk.CallbackAction.new(self.on_open_trigger)
        )
        shortcut_controller.add_shortcut(save_shortcut)
        shortcut_controller.add_shortcut(open_shortcut)

        self.blocks = []
        self.state = []

    def on_open_trigger(self, *args):
        print('Abrindo...')
        with open('foo_save.json', 'r') as file:
            data = json.load(file)
            for i in data:
                block = Block.deserealize(i, None)
                self.blocks.append(block)

        self.canvas.queue_draw()

    def on_save_trigger(self, *args):
        print("Salvando...")
        print(len(self.blocks))
        for b in self.blocks:
            serialized = b.serialize()
            if serialized not in self.state:
                self.state.append(serialized)
        with open('foo_save.json', 'w') as file:
            json.dump(self.state, file)

    @Gtk.Template.Callback()
    def on_draw(self, area, ctx, width, height):
        print('draw')
        ctx.set_source_rgb(0.9, 0.9, 1)
        ctx.paint()
        for b in self.blocks:
            b.ctx = ctx
            b.draw()

    def on_click(self, gesture, data, x, y):
        b = Block(None, 'foo', (x,y))
        self.blocks.append(b)
        # self.state.append(b.serialize())
        self.canvas.queue_draw()
        # print(len(self.blocks))

    @Gtk.Template.Callback()
    def on_toggle(self, widget):
        if widget.get_active():
            print('abrindo')
            self.split_view.set_collapsed(False)
        else:
            print('fechando')
            self.split_view.set_collapsed(True)