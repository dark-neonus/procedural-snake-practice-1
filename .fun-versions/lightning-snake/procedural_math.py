import pyglet
from pyglet.gl import *
from typing import List
from pyglet.math import Vec2
from my_shader import *
import math

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
    def __init__(self, calculation_radius, x=0, y=0, border_width=5, color=Color.grey, batch=None, radius=None) -> None:
        self.calculation_radius = calculation_radius

        if radius == None:
            radius = self.calculation_radius
             
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

    def front(self) -> Vec2:
        return self.pos() + self.direction.normalize() * self.radius
    def back(self) -> Vec2:
        return self.pos() - self.direction.normalize() * self.radius

    def set_batch(self, new_batch):
        if self.batch is not None:
            
            mode = pyglet.gl.GL_TRIANGLES
            group = self.group
            
            # new_batch.migrate(self._vertex_list, mode, group, new_batch)
            # new_batch.migrate(self.right_circle._vertex_list, mode, group, new_batch)
            # new_batch.migrate(self.left_circle._vertex_list, mode, group, new_batch)
        else:
            # new_batch.add(self)
            # new_batch.add(self.right_circle)
            # new_batch.add(self.left_circle)

            self.batch = new_batch
            self.right_circle = new_batch
            self.left_circle = new_batch

    def pos(self) -> Vec2:
        return Vec2(self.x, self.y)
    
    def set_pos(self, pos: Vec2) -> None:
        self.x = pos.x
        self.y = pos.y

    def project_on_circle(self, next_segment: 'ProceduralSegment') -> None:
        delta = Vec2(self.x - next_segment.x, self.y - next_segment.y).normalize() * next_segment.calculation_radius

        self.set_pos(next_segment.pos() + delta)

    def check_rotation(self, next_segment: 'ProceduralSegment') -> None:
        
        current_direction = self.direction.normalize()
        next_direction = (next_segment.pos() - self.pos()).normalize()
    
        # Calculate the angle between the two directions
        dot_product = current_direction.dot(next_direction)
        angle = math.acos(dot_product)
    
        # If the angle is greater than 90 degrees, adjust the next segment
        if angle > math.pi / 2:
            # Calculate the new position for next_segment
            delta = (next_segment.pos() - self.pos()).normalize() * next_segment.calculation_radius
    
            # Try both left and right rotations to find the best fit
            left_pos = self.pos() + delta.rotate(-angle + math.pi / 2)
            right_pos = self.pos() + delta.rotate(angle - math.pi / 2)
    
            # Choose the position with the smaller angle adjustment
            if (left_pos - self.pos()).normalize().dot(current_direction) > (right_pos - self.pos()).normalize().dot(current_direction):
                next_segment.set_pos(left_pos)
            else:
                next_segment.set_pos(right_pos)
    
            # Recalculate the direction after adjustment
            next_segment.direction = (next_segment.pos() - self.pos()).normalize() * next_segment.radius

        

    def calculate_sides(self, next_segment) -> None:
        
        if next_segment is not None:
            self.direction = (self.pos() - next_segment.pos()).normalize() * self.radius
        else:
            self.direction = self.direction.normalize() * self.radius

        self.left = self.direction.rotate(-math.pi / 2) + self.pos()
        self.right = self.direction.rotate(math.pi / 2) + self.pos()

        self.right_circle.x = self.right.x
        self.right_circle.y = self.right.y

        self.left_circle.x = self.left.x
        self.left_circle.y = self.left.y



    def update(self, dt, next_segment) -> None:
        if next_segment is not None:
            self.project_on_circle(next_segment)
            self.check_rotation(next_segment)

        self.calculate_sides(next_segment)




class ProceduralLimb:
    def __init__(self, segments=[], color=(255, 0, 255, 255), batch=None):

        self.batch = batch
        self.color = color

        self.segments: List[ProceduralSegment] = segments

        # Ensure segments are associated with the batch
        for segment in self.segments:
            segment.set_batch(self.batch)

        self._vertices = []
        self._colors = []
        self.vlist = None

        self.update_vertices()

    def head(self) -> ProceduralSegment:
        return self.segments[0] if self.segments else None

    def update(self, dt):
        self.segments[0].update(dt, None)
        for i in range(1, len(self.segments)):
            self.segments[i].update(dt, self.segments[i-1])
        
        self.update_vertices()

    def update_vertices(self):
        
        self._vertices = [self.segments[0].front().x, self.segments[0].front().y]
        self._colors = []
        for segm in self.segments:
            self._vertices.extend([segm.right.x, segm.right.y, segm.left.x, segm.left.y])
            # self._vertices.extend([segm.front().x, segm.front().y])
        
        self._vertices.extend([self.segments[-1].front().x, self.segments[-1].front().y, ])

        for i in range(int(len(self._vertices) / 2)):
            for i in range(4):
                self._colors.append(self.color[i])
            
        

        if self.vlist is not None:
            self.vlist.delete()

        self.vlist = program.vertex_list(int(len(self._vertices) / 2), pyglet.gl.GL_TRIANGLE_STRIP,
                            position=('f', self._vertices),
                            colors=('Bn', self._colors,),
                            batch=self.batch)

