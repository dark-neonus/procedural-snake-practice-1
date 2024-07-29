import pyglet
from pyglet.gl import *
from typing import List, Tuple
from pyglet.math import Vec2
import math


from lib.graphic.color import *
from lib.graphic.shapes import *

class ProceduralCircle(BorderCircle):
    def __init__(self, calculation_radius: float, x=0, y=0, border_width=5, color=Color.grey, batch=None, radius=None, debug_draw=False, max_angle: float=math.pi / 7) -> None:
        self.calculation_radius: float = calculation_radius

        if radius == None:
            radius = self.calculation_radius

        self.debug_draw: bool = debug_draw
        self.max_angle: float = max_angle
             
        super().__init__(
            x=x, y=y,
            radius=radius,
            color=color,
            border_width=border_width,
            batch=batch
        )

        self.direction: Vec2 = Vec2(0, 0)
        self.right: Vec2 = Vec2(0, 0)
        self.left: Vec2 = Vec2(0, 0)

        self.right_circle: pyglet.shapes.Circle = pyglet.shapes.Circle(0, 0, 4, color=Color.red, batch=self.batch)
        self.left_circle: pyglet.shapes.Circle = pyglet.shapes.Circle(0, 0, 4, color=Color.blue, batch=self.batch)

        self.direction_line: pyglet.shapes.Line = pyglet.shapes.Line(0, 0, 0, 0, color=Color.green, batch=self.batch)

    def front(self) -> Vec2:
        return self.pos() + self.direction.normalize() * self.radius
    def back(self) -> Vec2:
        return self.pos() - self.direction.normalize() * self.radius

    def set_batch(self, new_batch: pyglet.graphics.Batch) -> None:
        if self.debug_draw:
            if self.batch is not None:

                mode = pyglet.gl.GL_TRIANGLES
                group = self.group

                new_batch.migrate(self._vertex_list, mode, group, new_batch)
                new_batch.migrate(self.right_circle._vertex_list, mode, group, new_batch)
                new_batch.migrate(self.left_circle._vertex_list, mode, group, new_batch)
                new_batch.migrate(self.direction_line._vertex_list, mode, group, new_batch)
            else:
                # new_batch.add(self)
                # new_batch.add(self.right_circle)
                # new_batch.add(self.left_circle)
                # new_batch.add(self.direction_line)

                self.batch = new_batch
                self.right_circle.batch = new_batch
                self.left_circle.batch = new_batch
                self.direction_line.batch = new_batch

    def pos(self) -> Vec2:
        return Vec2(self.x, self.y)
    
    def set_pos(self, pos: Vec2) -> None:
        self.x = pos.x
        self.y = pos.y


    def project_on_circle(self, next_segment: 'ProceduralCircle') -> None:
        delta = (self.pos() - next_segment.pos()).normalize() * self.calculation_radius

        self.set_pos(next_segment.pos() + delta)

    
    def process_angle(self, next_segment: 'ProceduralCircle') -> None:
        angle_diff = self.direction.heading - next_segment.direction.heading

        delta = self.pos() - next_segment.pos()

        if abs(angle_diff) > self.max_angle:
            delta = delta.lerp(delta.rotate(-angle_diff), 0.1)

        self.set_pos(next_segment.pos() + delta)

    def calculate_direction(self, next_segment: 'None | ProceduralCircle') -> None:
        
        if next_segment is not None:
            self.direction = (next_segment.pos() - self.pos()).normalize() * self.radius
        else:
            self.direction = self.direction.normalize() * self.radius


    def update_controls(self):
        self.left = self.direction.rotate(-math.pi / 2) + self.pos()
        self.right = self.direction.rotate(math.pi / 2) + self.pos()

        if self.debug_draw:
            self.right_circle.x = self.right.x
            self.right_circle.y = self.right.y

            self.left_circle.x = self.left.x
            self.left_circle.y = self.left.y

            self.direction_line.x = self.pos().x
            self.direction_line.y = self.pos().y
            self.direction_line.x2 = self.pos().x + self.direction.x
            self.direction_line.y2 = self.pos().y + self.direction.y

    def update(self, dt, next_segment: 'None | ProceduralCircle') -> None:
        if next_segment is not None:
            self.project_on_circle(next_segment)

        self.calculate_direction(next_segment)

        if next_segment is not None:
            self.process_angle(next_segment)

        self.update_controls()


    def get_point_on(self, angle_from_direction: float, distance_from_center: float=1.0) -> Vec2:
        """
        parameters:
        * angle_from_direction: float - angle in radians from the direction of the circle
        * distance_from_center: float - distance from the center of the circle where 0.0 is center and 1.0 is border
        """
        attach_angle = math.atan2(self.direction.y, self.direction.x) + angle_from_direction

        dist = Vec2(self.radius * math.cos(attach_angle), self.radius * math.sin(attach_angle)) * distance_from_center

        return self.pos() + dist
