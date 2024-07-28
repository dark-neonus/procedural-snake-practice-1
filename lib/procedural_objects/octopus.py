from lib.procedural_objects.snake import ProceduralSnake
from lib.procedural_objects.circle import ProceduralCircle
from lib.snake_behavior import SnakeBehavior, behaviours, BEH_DO_NOTHING, BEH_FOLLOW_MOUSE, BEH_MOVE_ON_ITSELF, BEH_SET_POS
from lib.graphic.color import Color

import math

from typing import Dict

class Octopus:
    def __init__(
            self,
            head: None | ProceduralSnake = None,
            tentacles: Dict[float, ProceduralSnake] = {},
            debug_draw: bool = False,
            behavior: int = BEH_DO_NOTHING         
            ) -> None:
        


        self.head: ProceduralSnake = head
        if self.head == None or len(self.head.segments) == 0:
            raise ValueError("Head cannot be empty!")

        self.tentacles: Dict[float, ProceduralSnake] = tentacles

        self.debug_draw: bool = debug_draw
        self.behavior: int = behavior

    def update(self, dt: float, **kwargs):
        self.head.update(dt, **kwargs)

        for angle, limb in self.tentacles.items():
            limb.update(
                dt,
                pos=self.head.segments[-1].get_point_on(math.radians(angle + 180), 0.8)
                #get_attach_pos(self.head.segments[-1].pos(), self.head.segments[-1].radius * 0.8, angle + 180, self.head.segments[-1].direction)
                )
            
    def set_fill_color(self, color: tuple):
        self.head.fill_color = color
        for limb in self.tentacles.values():
            limb.fill_color = color

    def set_border_colro(self, color: tuple):
        self.head.border_color = color
        for limb in self.tentacles.values():
            limb.border_color = color


