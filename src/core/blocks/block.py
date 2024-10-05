import uuid
from cairo import Context

class Block:
    size = 64
    radius = 5

    def __init__(self, context: Context, name: str, pos: tuple) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.ctx = context
        self.pos = pos

    def draw(self):
        x, y = 30, 30
        self.ctx.arc(self.pos[0] + self.size - self.radius, self.pos[1] + self.radius, self.radius, -0.5 * 3.14, 0)
        self.ctx.arc(self.pos[0] + self.size - self.radius, self.pos[1] + self.size - self.radius, self.radius, 0, 0.5 * 3.14)
        self.ctx.arc(self.pos[0] + self.radius, self.pos[1] + self.size - self.radius, self.radius, 0.5 * 3.14, 3.14)
        self.ctx.arc(self.pos[0] + self.radius, self.pos[1] + self.radius, self.radius, 3.14, 1.5 * 3.14)
        self.ctx.close_path()

        self.ctx.set_source_rgb(0.9, 0.9, 0.5)
        self.ctx.fill_preserve()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'position': {'x': self.pos[0], 'y': self.pos[1]}
        }

    @staticmethod
    def deserealize(data, context):
        pos = (data.get('position').get('x'), data.get('position').get('y'))
        block = Block(context, data.get('name'), pos)
        block.id = uuid.UUID(data.get('id'))
        return block