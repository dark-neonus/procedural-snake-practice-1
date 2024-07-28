import pyglet
from pyglet.gl import *
from typing import List, Tuple
from pyglet.math import Vec2
from lib.graphic.my_shaders import *
from lib.graphic.color import Color

class BorderCircle(pyglet.shapes.Arc):
    def __init__(self, x, y, radius, color=Color.grey, border_width=1, batch=None):
        super().__init__(
            x=x, y=y,
            radius=radius,
            color=color,
            segments=18,
            thickness=border_width,  # Set thickness to border_width
            batch=batch
        )

    def set_batch(self, new_batch):
        if self.batch is not None:
            # Determine the rendering mode and group for migration
            mode = pyglet.gl.GL_TRIANGLES  # Example mode, adjust as needed
            group = self.group  # Use the current group
            # Migrate the vertex list to the new batch with specified mode and group
            new_batch.migrate(self._vertex_list, mode, group, new_batch)
        else:
            new_batch.add(self)  # Add the circle to the new batch
            self.batch = new_batch  # Assign the new batch

    def set_pos(self, new_pos: Vec2):
        self.x = new_pos.x
        self.y = new_pos.y
