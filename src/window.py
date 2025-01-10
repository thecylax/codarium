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
import os
from copy import copy
from time import sleep

from gi.repository import Adw, Gdk, Gio, Gtk

from .core.blocks.block import Block
from .core.blocks.port import Port
from .core.database import Database
from .core.gesture import CustomGesture


# @Gtk.Template(resource_path='/com/blacktomato/codarium/inspector.ui')
@Gtk.Template(filename='src/inspector.ui')
class Inspector(Adw.Dialog):
    __gtype_name__ = 'InspectorWindow'

    block_name = Gtk.Template.Child()
    title = Gtk.Template.Child()
    close_btn = Gtk.Template.Child()
    canvas = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.set_draw_func(self.on_draw)
        self.block = None
        self.is_visible = False

    @Gtk.Template.Callback()
    def on_close_inspector(self, widget):
        self.is_visible = False
        self.close()

    @Gtk.Template.Callback()
    def on_draw(self, area, ctx, width, height):
        print('draw_inspector')
        self.block.ctx = ctx
        self.block.pos = ((width-64) / 2, (height - 64) / 2)
        ctx.set_source_rgb(0.9, 0.9, 0.9)
        ctx.paint()
        self.block.draw_ports()

    def set_block(self, block: Block):
        print(block)
        self.block = copy(block)
        self.block_name.set_markup(block.info)  # mudar nome para nao causar confusão
        self.title.set_subtitle(block.name)


@Gtk.Template(filename="src/splash.ui")
class SplashScreen(Gtk.Window):
    __gtype_name__ = "Splash"

    logo_image = Gtk.Template.Child()
    # label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_default_size(400, 300)
        # self.set_app_paintable(True)
        # self.set_decorated(True)
        # self.set_keep_above(True)
        # self.set_resizable(False)
        # self.set_opacity(0.1)
        print(os.getcwd())
        self.logo_image.set_filename('src/splash.png')


@Gtk.Template(filename="src/splash2.ui")
class SplashScreen2(Adw.Window):
    __gtype_name__ = "Splash2"

    logo_image = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logo_image.set_filename('src/splash2.png')

@Gtk.Template(filename='src/codarium.ui')
# @Gtk.Template(resource_path='/com/blacktomato/Codarium/codarium.ui')
class CodariumWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CodariumWindow'

    split_view = Gtk.Template.Child()
    canvas = Gtk.Template.Child()
    status_bar = Gtk.Template.Child()
    title_bar = Gtk.Template.Child()
    blocks_grid = Gtk.Template.Child()
    sidebar_toggle = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.set_draw_func(self.on_draw)

        me = Gtk.GestureClick.new()
        me.connect("pressed", self.on_click)
        self.canvas.add_controller(me)
        ke = Gtk.EventControllerKey.new()
        ke.connect("key-pressed", self.on_key_pressed)
        ke.connect("key-released", self.on_key_released)
        self.add_controller(ke)

        self.ctrl_pressed = False

        self.block_selection = {}

        self.inspector = Inspector()

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
        # Definir atalho Ctrl+B para esconder painel
        panel_shortcut = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>B"),
            Gtk.CallbackAction.new(self.on_panel_toggle_trigger)
        )
        shortcut_controller.add_shortcut(save_shortcut)
        shortcut_controller.add_shortcut(open_shortcut)
        shortcut_controller.add_shortcut(panel_shortcut)

        # define banco de dados
        self.db = Database('codadb.json')

        self.blocks: Block = []
        self.state = []
        self.focused_block: Block = None

        # Modelo de dados (ícones e nomes)
        icon_data = [
            {"name": "Icon 1", "icon": "folder"},
            {"name": "Icon 2", "icon": "user-home"},
            {"name": "Icon 3", "icon": "system-run"},
            {"name": "Icon 4", "icon": "document-open"},
            {"name": "Icon 5", "icon": "edit-copy"},
            {"name": "Icon 6", "icon": "media-playback-start"},
            {"name": "Icon 7", "icon": "airplane-mode"},
            {"name": "Icon 8", "icon": "alarm"}
        ]
        # Abrir db e carregar blocos na biblioteca
        self.db.restore_database()
        print('Loading blocks...')
        core_blocks = self.db.get_all('blocks')
        for cb in core_blocks:
            icon_data.append({'name': cb['name'], 'icon': cb['icon']})

        # Criação do ListStore para armazenar os ícones
        list_store = Gio.ListStore.new(Gtk.StringObject)

        # Adicionar dados ao modelo
        for item in icon_data:
            list_store.append(Gtk.StringObject.new(f"{item['name']}|{item['icon']}"))

        # Encapsular o ListStore em GtkSingleSelection
        self.selection_model = Gtk.SingleSelection.new(list_store)
        self.selection_model.set_can_unselect(True)

        # Definir a fábrica de itens para o GtkGridView
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.setup_icon_item)
        factory.connect("bind", self.bind_icon_item)

        # Conectar o modelo e a fábrica ao GtkGridView
        self.blocks_grid.set_model(self.selection_model)
        self.blocks_grid.set_factory(factory)

        self.selection_model.connect("notify::selected", self.on_icon_selected)

    def setup_icon_item(self, factory, list_item):
        """Configura cada item com uma GtkBox contendo um GtkImage e GtkLabel"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        icon = Gtk.Image()

        box.append(icon)

        list_item.set_child(box)

    def bind_icon_item(self, factory, list_item):
        """Vincula os dados do modelo ao item do grid"""
        data = list_item.get_item().get_string()
        icon_label, icon_name = data.split('|')
        box = list_item.get_child()

        icon = box.get_first_child()  # O GtkImage
        icon.set_from_icon_name(icon_name)

        box.set_tooltip_text(icon_label.capitalize())

    def on_icon_selected(self, selection_model: Gtk.SingleSelection, param):
        """Callback chamado quando um ícone é selecionado"""
        selected_item = selection_model.get_selected_item()
        # selection_model.

        if selected_item:
            block_name, icon_name = selected_item.get_string().split('|')
            print(f"Ícone selecionado: {block_name} | {icon_name}")
            self.block_selection = {'name': block_name, "icon": icon_name}
            self.status_bar.remove_all(1)
            # Aqui você pode executar ações específicas baseadas no ícone selecionado
            # self.perform_action_for_icon(icon_name)

    def on_open_trigger(self, *args):
        print('Abrindo...')
        file_name = 'foo_save.json'
        with open(file_name, 'r') as file:
            data = json.load(file)
            for i in data:
                block = Block.deserealize(i, None)
                self.blocks.append(block)

        self.canvas.queue_draw()
        self.title_bar.set_subtitle(f"<i>{file_name}</i>")

    def on_save_trigger(self, *args):
        print("Salvando...")
        print(len(self.blocks))
        for b in self.blocks:
            serialized = b.serialize()
            if serialized not in self.state:
                self.state.append(serialized)
        with open('foo_save.json', 'w') as file:
            json.dump(self.state, file)

    def on_panel_toggle_trigger(self, *args):
        print("Hiding...")
        active = self.sidebar_toggle.get_active()
        self.split_view.set_collapsed(not active)
        self.sidebar_toggle.set_active(not active)

    @Gtk.Template.Callback()
    def on_draw(self, area, ctx, width, height):
        # print('draw')
        ctx.set_source_rgb(0.9, 0.9, 1)
        ctx.paint()
        for b in self.blocks:
            b.ctx = ctx
            b.draw()
            # b.draw_icon()

    def on_click(self, gesture, data, x, y):
        # p = Port(None, 'input', (30,30), 32, 10)
        # self.blocks.append(p)
        # self.canvas.queue_draw()

        block_name = self.block_selection.get('name')
        # block_icon = self.block_selection.get('icon')
        if self.block_selection:  # Vai inserir um novo bloco no canvas?
            block_data = self.db.get_one('blocks', 'name', block_name)
            b = Block.deserealize(block_data, None)
            b.pos = (x, y)
            self.blocks.append(b)
            self.canvas.queue_draw()
            self.status_bar.push(1, b.name)
            print(b.ports)

            self.block_selection = {}
        else:  # Seleção vazia ou num bloco existente
            for b in self.blocks:
                if b.focused(x,y):
                    self.focused_block = b
                    self.status_bar.push(1, b.name)
            if self.focused_block and self.ctrl_pressed:
                # Open inspector and Draw ports?
                print('switch to ports')
                self.inspector.set_block(self.focused_block)
                self.inspector.present()
                self.focused_block = None
                self.ctrl_pressed = False
                self.inspector.is_visible = True

                return

            if self.focused_block:
                print(f'selected {self.focused_block.name}')
                if self.inspector.is_visible:
                    # self.inspector.block_name.set_label(self.focused_block.info)
                    # self.inspector.block_name.set_markup(self.focused_block.info)
                    # self.inspector.title.set_subtitle(self.focused_block.name)
                    self.inspector.set_block(self.focused_block)
                    self.inspector.present()

                self.focused_block = None
                return

            self.inspector.on_close_inspector(self.inspector.close_btn) if self.inspector.is_visible else None
            # self.inspector.is_visible = False
            self.status_bar.remove_all(1)

    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Control_L or keyval == Gdk.KEY_Control_R:
        # if keyval == Gdk.KEY_i and state & Gdk.ModifierType.CONTROL_MASK:
            self.ctrl_pressed = True
            print('Ctrl pressed.')

    def on_key_released(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Control_L or keyval == Gdk.KEY_Control_R:
            self.ctrl_pressed = False
            print("Ctrl released.")

    @Gtk.Template.Callback()
    def on_toggle(self, widget):
        if widget.get_active():
            print('abrindo')
            self.split_view.set_collapsed(False)
        else:
            print('fechando')
            self.split_view.set_collapsed(True)