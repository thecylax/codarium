import uuid
from typing import Dict

import cairo
from gi.repository import Gdk, GdkPixbuf, Gtk


class Block:
    size = 64
    radius = 5

    def __init__(self, context: cairo.Context, name: str, pos: tuple, icon_name: str) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.info = 'N/A'
        self.ctx = context
        self.pos = pos
        self.icon_name = icon_name
        self.ports = {}

    def draw(self):
        self.ctx.arc(self.pos[0] + self.size - self.radius, self.pos[1] + self.radius, self.radius, -0.5 * 3.14, 0)
        self.ctx.arc(self.pos[0] + self.size - self.radius, self.pos[1] + self.size - self.radius, self.radius, 0, 0.5 * 3.14)
        self.ctx.arc(self.pos[0] + self.radius, self.pos[1] + self.size - self.radius, self.radius, 0.5 * 3.14, 3.14)
        self.ctx.arc(self.pos[0] + self.radius, self.pos[1] + self.radius, self.radius, 3.14, 1.5 * 3.14)
        self.ctx.close_path()

        self.ctx.set_source_rgb(0.9, 0.9, 0.5)
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

    def draw_ports(self):
        # Considerando que passou pela valiação de schema, sempre terá ports
        inputs = self.ports.get('inputs')
        outputs = self.ports.get('outputs')
        input_port_height = self.size / len(inputs)
        output_port_height = self.size / len(outputs)
        port_width = 30
        port_height = 10
        if self.ports:
            x, y = self.pos

            # draw block wireframe
            self.ctx.arc(x + self.size - self.radius, y + self.radius, self.radius, -0.5 * 3.14, 0)
            self.ctx.arc(x + self.size - self.radius, y + self.size - self.radius, self.radius, 0, 0.5 * 3.14)
            self.ctx.arc(x + self.radius, y + self.size - self.radius, self.radius, 0.5 * 3.14, 3.14)
            self.ctx.arc(x + self.radius, y + self.radius, self.radius, 3.14, 1.5 * 3.14)
            self.ctx.close_path()
            self.ctx.fill_preserve()
            self.ctx.set_source_rgb(0, 0, 0)
            self.ctx.stroke()

            self._draw_input_ports(len(inputs), self.size / 2, input_port_height)
            self._draw_output_ports(len(outputs), self.size / 2, output_port_height)
            # # Top left port
            # self.ctx.arc(x + self.radius, y + self.radius, self.radius, 3.14, 1.5 * 3.14)
            # self.ctx.rel_line_to(port_width - self.radius, 0)
            # self.ctx.rel_line_to(0, port_height)
            # self.ctx.rel_line_to(-port_width, 0)
            # self.ctx.close_path()
            # self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
            # self.ctx.fill_preserve()
            # self.ctx.set_source_rgb(0, 0, 0)
            # self.ctx.stroke()

            # # Bottom left port
            # self.ctx.arc(x + self.radius, y + self.size - self.radius, self.radius, 0.5 * 3.14, 3.14)
            # self.ctx.rel_line_to(0, -(port_height - self.radius))   # Left line, from B to T
            # self.ctx.rel_line_to(port_width, 0)                     # Top line, from L to R
            # self.ctx.rel_line_to(0, port_height)                    # Right line, from T to B
            # self.ctx.close_path()
            # self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
            # self.ctx.fill_preserve()
            # self.ctx.set_source_rgb(0, 0, 0)
            # self.ctx.stroke()

            # # Top right port
            # self.ctx.arc(x + self.size - self.radius, y + self.radius, self.radius, -0.5 * 3.14, 0)
            # self.ctx.rel_line_to(0, port_height - self.radius)
            # self.ctx.rel_line_to(-port_width, 0)
            # self.ctx.rel_line_to(0, -port_height)
            # self.ctx.close_path()
            # self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
            # self.ctx.fill_preserve()
            # self.ctx.set_source_rgb(0, 0, 0)
            # self.ctx.stroke()

            # # Bottom right port
            # self.ctx.arc(x + self.size - self.radius, y + self.size - self.radius, self.radius, 0, 0.5 * 3.14)
            # self.ctx.rel_line_to(-(port_width - self.radius), 0)
            # self.ctx.rel_line_to(0, -port_height)
            # self.ctx.rel_line_to(port_width, 0)
            # self.ctx.close_path()
            # self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
            # self.ctx.fill_preserve()
            # self.ctx.set_source_rgb(0, 0, 0)
            # self.ctx.stroke()

    def _draw_input_ports(self, num, width, height):
        x, y = self.pos
        for i in range(num):
            self.ctx.rectangle(x, y, width, height)
            self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral -> Deve ser de acordo com o tipo!
            self.ctx.fill_preserve()
            self.ctx.set_source_rgb(0, 0, 0)
            self.ctx.stroke()
            y += height

    def _draw_output_ports(self, num, width, height):
        x, y = self.pos
        x = x + width
        for i in range(num):
            self.ctx.rectangle(x, y, width, height)
            self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral -> Deve ser de acordo com o tipo!
            self.ctx.fill_preserve()
            self.ctx.set_source_rgb(0, 0, 0)
            self.ctx.stroke()
            y += height


    def draw_icon(self):
        # Carregar o tema de ícones do sistema
        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())

        # Carregar o ícone
        icon_info = icon_theme.lookup_icon(
            self.icon_name,  # Lista de possíveis nomes de ícone
            None,
            32,         # Tamanho do ícone (32px)
            1,          # Escala
            0,          # Direção (LTR)
            Gtk.IconLookupFlags.FORCE_REGULAR
        )

        pixbuf = GdkPixbuf.Pixbuf.new_from_file("/home/cardoso/yohoho/game/desktop_cursed.png")
        # Obter dados do pixbuf
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        data = pixbuf.get_pixels()

        # Criar uma superfície Cairo compatível
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

        # Criar o pixbuf como imagem no contexto Cairo
        for y in range(height):
            for x in range(width):
                offset = (y * pixbuf.get_rowstride()) + (x * pixbuf.get_n_channels())
                pixel = data[offset:offset + 4]
                r, g, b, a = [v / 255.0 for v in pixel]
                self.ctx.set_source_rgba(r, g, b, a)
                self.ctx.rectangle(x, y, 1, 1)
                self.ctx.fill()

        self.ctx.translate(self.pos[0], self.pos[1])
        self.ctx.set_source_surface(surface, self.pos[0], self.pos[1])
        self.ctx.paint()

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'position': {'x': self.pos[0], 'y': self.pos[1]}
        }

    def focused(self, x_click: float, y_click: float) -> bool:
        x, y = self.pos
        if x <= x_click <= x + self.size and y <= y_click <= y + self.size:
            return True

    @staticmethod
    def deserealize(data: Dict, context: cairo.Context):
        pos = (data.get('position').get('x'), data.get('position').get('y'))
        block = Block(context, data.get('name'), pos, icon_name='')
        # block.id = uuid.UUID(data.get('id'))
        block.ports = data.get('ports')
        block.info = data.get('info', 'N/A')

        return block