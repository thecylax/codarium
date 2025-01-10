from typing import Tuple

import cairo


class Port:
    size = 64
    radius = 5

    def __init__(self, context: cairo.Context, pos: Tuple, width: float, height: float) -> None:
        self.ctx = context
        self.pos = pos
        self.width = width
        self.height = height
        self.direction = None
        self.dtype = None


    def draw(self):
        x, y = self.pos[0], self.pos[1]

        # draw block
        self.ctx.arc(x + self.size - self.radius, y + self.radius, self.radius, -0.5 * 3.14, 0)
        self.ctx.arc(x + self.size - self.radius, y + self.size - self.radius, self.radius, 0, 0.5 * 3.14)
        self.ctx.arc(x + self.radius, y + self.size - self.radius, self.radius, 0.5 * 3.14, 3.14)
        self.ctx.arc(x + self.radius, y + self.radius, self.radius, 3.14, 1.5 * 3.14)
        self.ctx.close_path()
        self.ctx.set_source_rgb(0.9, 0.9, 0.5)
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

        # Top left
        self.ctx.arc(x + self.radius, y + self.radius, self.radius, 3.14, 1.5 * 3.14)  # TL
        self.ctx.rel_line_to(self.width - self.radius, 0)
        self.ctx.rel_line_to(0, self.height)
        self.ctx.rel_line_to(-self.width, 0)
        self.ctx.close_path()
        self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

        # Top right
        self.ctx.arc(x + self.size - self.radius, y + self.radius, self.radius, -0.5 * 3.14, 0)
        self.ctx.rel_line_to(0, self.height-self.radius)
        self.ctx.rel_line_to(-self.width, 0)
        self.ctx.rel_line_to(0, -self.height)
        self.ctx.close_path()
        self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

        # Bottom left
        self.ctx.arc(x + self.radius, y + self.size - self.radius, self.radius, 0.5 * 3.14, 3.14)  # BL
        self.ctx.rel_line_to(0, -(self.height-self.radius))
        self.ctx.rel_line_to(self.width, 0)
        self.ctx.rel_line_to(0, self.height)
        self.ctx.close_path()
        self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

        # Bottom right
        self.ctx.arc(x + self.size - self.radius, y + self.size - self.radius, self.radius, 0, 0.5 * 3.14)
        self.ctx.rel_line_to(-(self.width-self.radius), 0)
        self.ctx.rel_line_to(0, -self.height)
        self.ctx.rel_line_to(self.width, 0)
        self.ctx.close_path()
        self.ctx.set_source_rgb(1, 0.38, 0.27)  # coral
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()


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

    # @staticmethod
    # def deserealize(data, context):
    #     pos = (data.get('position').get('x'), data.get('position').get('y'))
    #     block = Port(context, data.get('name'), pos, icon_name='')
    #     block.id = uuid.UUID(data.get('id'))
    #     return block