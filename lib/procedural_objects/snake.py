import pyglet
from pyglet.gl import *
from typing import List, Tuple
from pyglet.math import Vec2
import math


from lib.graphic.color import Color
from lib.graphic.my_shaders import program
from lib.procedural_objects.circle import ProceduralCircle
from lib.snake_behavior import BEH_DO_NOTHING, behaviours

class ProceduralSnake:
    def __init__(
            self,
            segments=[],
            fill_color=(255, 0, 255, 255),
            border_color=Color.white,
            batch=None,
            debug_draw=False,
            behavior=BEH_DO_NOTHING
            ) -> None:

        self.batch: pyglet.graphics.Batch = batch
        self.fill_color = fill_color
        self.border_color = border_color
        self.debug_draw = debug_draw
        self.behavior: int = behavior

        self.group = pyglet.graphics.Group()

        self.segments: List[ProceduralCircle] = segments

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

    def head(self) -> ProceduralCircle:
        return self.segments[0] if self.segments else None
    

    def update(self, dt: float, **kwargs):
        behaviours[self.behavior].process(self, dt, **kwargs)
        
        self.segments[0].update(dt, None)
        for i in range(1, len(self.segments)):
            self.segments[i].update(dt, self.segments[i-1])
        
        if not self.debug_draw:
            self.update_vertices()

    def update_vertices(self):
        

        _right = [
            self.segments[0].front().x, self.segments[0].front().y,
            self.segments[0].get_point_on(math.radians(30)).x, self.segments[0].get_point_on(math.radians(30)).y,
            self.segments[0].get_point_on(math.radians(30)).x, self.segments[0].get_point_on(math.radians(30)).y,
            self.segments[0].get_point_on(math.radians(60)).x, self.segments[0].get_point_on(math.radians(60)).y,
            self.segments[0].get_point_on(math.radians(60)).x, self.segments[0].get_point_on(math.radians(60)).y,
            ]
        _left = [
            self.segments[0].front().y, self.segments[0].front().x,
            self.segments[0].get_point_on(math.radians(-30)).y, self.segments[0].get_point_on(math.radians(-30)).x,
            self.segments[0].get_point_on(math.radians(-30)).y, self.segments[0].get_point_on(math.radians(-30)).x,
            self.segments[0].get_point_on(math.radians(-60)).y, self.segments[0].get_point_on(math.radians(-60)).x,
            self.segments[0].get_point_on(math.radians(-60)).y, self.segments[0].get_point_on(math.radians(-60)).x,
            ]

        for segm in self.segments:
            _right.append(segm.right.x)
            _right.append(segm.right.y)
            _right.append(segm.right.x)
            _right.append(segm.right.y)

            _left.append(segm.left.y)
            _left.append(segm.left.x)
            _left.append(segm.left.y)
            _left.append(segm.left.x)

        _right.extend([
            self.segments[-1].get_point_on(math.radians(135)).x, self.segments[-1].get_point_on(math.radians(135)).y,
            self.segments[-1].get_point_on(math.radians(135)).x, self.segments[-1].get_point_on(math.radians(135)).y,
            self.segments[-1].back().x, self.segments[-1].back().y,
            ])
        
        _left.extend([
            self.segments[-1].get_point_on(math.radians(-135)).y, self.segments[-1].get_point_on(math.radians(-135)).x,
            self.segments[-1].get_point_on(math.radians(-135)).y, self.segments[-1].get_point_on(math.radians(-135)).x,
            self.segments[-1].back().y, self.segments[-1].back().x
            ])


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
   