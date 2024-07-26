import pyglet
from pyglet.gl import *
from typing import List, Tuple
from pyglet.math import Vec2
from my_shader import *
import math
import random


class Color:
    white = (255, 255, 255, 255)
    grey = (127, 127, 127, 255)
    black = (0, 0, 0, 255)

    red = (255, 0, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)


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

class ProceduralSegment(BorderCircle):
    def __init__(self, calculation_radius, x=0, y=0, border_width=5, color=Color.grey, batch=None, radius=None, debug_draw=False) -> None:
        self.calculation_radius = calculation_radius

        if radius == None:
            radius = self.calculation_radius

        self.debug_draw = debug_draw
        self.max_angle = math.pi / 7
             
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

        self.right_circle = pyglet.shapes.Circle(0, 0, 4, color=Color.red, batch=self.batch)
        self.left_circle = pyglet.shapes.Circle(0, 0, 4, color=Color.blue, batch=self.batch)

        self.direction_line = pyglet.shapes.Line(0, 0, 0, 0, color=Color.green, batch=self.batch)

    def front(self) -> Vec2:
        return self.pos() + self.direction.normalize() * self.radius
    def back(self) -> Vec2:
        return self.pos() - self.direction.normalize() * self.radius

    def set_batch(self, new_batch):
        if self.debug_draw:
            if self.batch is not None:

                mode = pyglet.gl.GL_TRIANGLES
                group = self.group

                new_batch.migrate(self._vertex_list, mode, group, new_batch)
                new_batch.migrate(self.right_circle._vertex_list, mode, group, new_batch)
                new_batch.migrate(self.left_circle._vertex_list, mode, group, new_batch)
                new_batch.migrate(self.direction_line._vertex_list, mode, group, new_batch)
            else:
                new_batch.add(self)
                new_batch.add(self.right_circle)
                new_batch.add(self.left_circle)
                new_batch.add(self.direction_line)

                self.batch = new_batch
                self.right_circle.batch = new_batch
                self.left_circle.batch = new_batch
                self.direction_line.batch = new_batch

    def pos(self) -> Vec2:
        return Vec2(self.x, self.y)
    
    def set_pos(self, pos: Vec2) -> None:
        self.x = pos.x
        self.y = pos.y


    def project_on_circle(self, next_segment: 'ProceduralSegment') -> None:
        delta = (self.pos() - next_segment.pos()).normalize() * self.calculation_radius

        self.set_pos(next_segment.pos() + delta)

    
    def process_angle(self, next_segment) -> None:
        angle_diff = self.direction.heading - next_segment.direction.heading

        delta = self.pos() - next_segment.pos()

        if abs(angle_diff) > self.max_angle:
            delta = delta.lerp(delta.rotate(-angle_diff), 0.1)

        self.set_pos(next_segment.pos() + delta)

    def calculate_direction(self, next_segment) -> None:
        
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

    def update(self, dt, next_segment) -> None:
        if next_segment is not None:
            self.project_on_circle(next_segment)

        self.calculate_direction(next_segment)

        if next_segment is not None:
            self.process_angle(next_segment)

        self.update_controls()




class ProceduralLimb:
    def __init__(self, segments=[], fill_color=(255, 0, 255, 255), border_color=Color.white, batch=None, debug_draw=False) -> None:

        self.batch: pyglet.graphics.Batch = batch
        self.fill_color = fill_color
        self.border_color = border_color
        self.debug_draw = debug_draw

        self.group = pyglet.graphics.Group()

        self.segments: List[ProceduralSegment] = segments

        # Ensure segments are associated with the batch
        for segment in self.segments:
            segment.debug_draw = self.debug_draw
            segment.set_batch(self.batch)

        self.border_vertices = []

        self._colors_fill = []
        self._colors_border = []
        
        self.vlist_fill_list: List[pyglet.graphics.VertexList] = []
        self.vlist_border = None

        self.update_vertices()

    def head(self) -> ProceduralSegment:
        return self.segments[0] if self.segments else None
    

    def update(self, dt):
        self.segments[0].update(dt, None)
        for i in range(1, len(self.segments)):
            self.segments[i].update(dt, self.segments[i-1])
        
        if not self.debug_draw:
            self.update_vertices()

    def update_vertices(self):
        

        _right = [self.segments[0].front().x, self.segments[0].front().y]
        _left = [self.segments[0].front().y, self.segments[0].front().x]

        for segm in self.segments:
            _right.append(segm.right.x)
            _right.append(segm.right.y)
            _right.append(segm.right.x)
            _right.append(segm.right.y)

            _left.append(segm.left.y)
            _left.append(segm.left.x)
            _left.append(segm.left.y)
            _left.append(segm.left.x)

        _right.extend([self.segments[-1].back().x, self.segments[-1].back().y])
        _left.extend([self.segments[-1].back().y, self.segments[-1].back().x])


        self.fill_vertices = []

        for i in range(0, len(_right), 2):
            self.fill_vertices.extend([
                _right[i], _right[i + 1],
                _right[(i + 2) % len(_right)], _right[(i + 3) % len(_right)],
                _left[i + 1], _left[i]
            ])

            self.fill_vertices.extend([
                _left[i + 1], _left[i],
                _left[(i + 3) % len(_left)], _left[(i + 2) % len(_left)],
                _right[(i + 2) % len(_right)], _right[(i + 3) % len(_right)]
            ])


        _left.reverse()
        self.border_vertices = _right + _left

        # >>> Create colors for snake
        self._colors_fill = self.fill_color * (len(self.fill_vertices) // 2)
        self._colors_border = self.border_color * (len(self.border_vertices) // 2)


        # >>> Delete the old vertex lists
        if self.vlist_fill_list:
            for vlist in self.vlist_fill_list:
                vlist.delete()
            self.vlist_fill_list.clear()

        if self.vlist_border is not None:
            self.vlist_border.delete()

        self.vlist_border = program.vertex_list(int(len(self.border_vertices) / 2), pyglet.gl.GL_LINES,
                                            position=('f', self.border_vertices),
                                            colors=('Bn', self._colors_border,),
                                            batch=self.batch)
        
        # >>> Create new vertex lists
        for i in range(0, len(self.fill_vertices), 6):
            self.vlist_fill_list.append(
                program.vertex_list(
                    count=3,
                    mode=pyglet.gl.GL_TRIANGLES,
                    position=('f', self.fill_vertices[i:i+6]),
                    colors=('Bn', self._colors_fill[i*2:(i+6)*2],),
                    batch=self.batch)
                )
        
        

