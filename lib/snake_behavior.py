import random

from pyglet.math import Vec2
from typing import Dict, Callable
import math

from lib.procedural_objects.circle import ProceduralCircle


class ProceduralSnake:
    pass

class SnakeBehavior:
    def __init__(self, process_function: Callable[[ProceduralSnake, ProceduralCircle, float], None]) -> None:
        self.process_function: Callable[['ProceduralSnake', ProceduralCircle, float], None] = process_function

    def process(self, snake: ProceduralSnake, dt: float, **kwargs):

        self.process_function(snake, snake.head(), dt, **kwargs)

behaviours: Dict[int, SnakeBehavior] = {}

def do_nothing(snake: ProceduralSnake, head: ProceduralCircle, dt: float, **kwargs):
    """
    Do nothing ro snake
    """

    pass

BEH_DO_NOTHING = 0
behaviours[BEH_DO_NOTHING] = SnakeBehavior(do_nothing)



def follow_mouse(snake: ProceduralSnake, head: ProceduralCircle, dt: float, **kwargs):
    """
    kwargs: 
        - mouse_pos: Vec2
    """
    diff = kwargs["mouse_pos"] - head.pos()
    
    if diff != Vec2(0, 0):
        head.set_pos(head.pos().lerp(kwargs["mouse_pos"], 0.3))
        head.direction = diff

BEH_FOLLOW_MOUSE = 1
behaviours[BEH_FOLLOW_MOUSE] = SnakeBehavior(follow_mouse)



delta_angle = 0
delta_angle_tick = 0

speed = 15.0
delta_speed = 0.0
delta_speed_tick = 0


def move_on_itself(snake: ProceduralSnake, head: ProceduralCircle, dt: float, **kwargs):
    """
    kwargs: 
        - screen_center: Vec2
    """
    global delta_angle, delta_angle_tick, speed, delta_speed, delta_speed_tick

    if head.direction == Vec2(0, 0):
        head.direction = Vec2(1, 0)

    
    if delta_angle_tick <= 0:
        delta_angle = random.uniform(-0.1, 0.1)
        delta_angle_tick = random.randint(2, 20)
    delta_angle_tick -= 1

    

    if abs(head.pos().x - kwargs["screen_center"].x) > 800 or abs(head.pos().y - kwargs["screen_center"].y) > 400:
        dir_to_center: Vec2 = kwargs["screen_center"] - head.pos()
        center_delta_angle = dir_to_center.heading - head.direction.heading
        if abs(center_delta_angle) == 0 or abs(center_delta_angle) > math.pi:
            center_delta_angle = 1

        head.direction = head.direction.normalize().rotate(math.copysign(0.1, center_delta_angle))
        delta_angle_tick += 1
    else:
        head.direction = head.direction.normalize().rotate(delta_angle)


    delta_speed_tick -= 1
    if delta_speed_tick <= 0:
        delta_speed = min(1.5, max(-1.5, delta_speed + random.uniform(-0.5, 0.5)))
        delta_speed_tick = random.randint(5, 15)

    speed = min(20.0, max(5.0, speed + delta_speed * dt * 100))

    head.set_pos(head.pos() + head.direction * speed)

BEH_MOVE_ON_ITSELF = 2
behaviours[BEH_MOVE_ON_ITSELF] = SnakeBehavior(move_on_itself)



def set_pos(snake, head, dt, **kwargs):
    """
    kwargs: 
        - pos: Vec2
    """
    diff = kwargs["pos"] - head.pos()
    
    if diff != Vec2(0, 0):
        head.set_pos(kwargs["pos"])
        head.direction = diff

BEH_SET_POS = 3
behaviours[BEH_SET_POS] = SnakeBehavior(set_pos)



delta_swim_angle = 0
delta_swim_angle_tick = 0

swim_speed = 15.0
delta_swim_speed = 0.0
delta_swim_speed_tick = 0

def swim_on_itself(snake: ProceduralSnake, head: ProceduralCircle, dt: float, **kwargs):
    """
    kwargs: 
        - screen_center: Vec2
    """
    global delta_swim_angle, delta_swim_angle_tick, swim_speed, delta_swim_speed, delta_swim_speed_tick

    if head.direction == Vec2(0, 0):
        head.direction = Vec2(1, 0)

    
    if delta_swim_angle_tick <= 0:
        delta_swim_angle = random.uniform(-0.1, 0.1)
        delta_swim_angle_tick = random.randint(2, 20)
    delta_swim_angle_tick -= 1

    
    if abs(head.pos().x - kwargs["screen_center"].x) > 800 or abs(head.pos().y - kwargs["screen_center"].y) > 400:
        dir_to_center: Vec2 = kwargs["screen_center"] - head.pos()
        center_delta_swim_angle = dir_to_center.heading - head.direction.heading
        if abs(center_delta_swim_angle) == 0 or abs(center_delta_swim_angle) > math.pi:
            center_delta_swim_angle = 1

        head.direction = head.direction.normalize().rotate(math.copysign(0.1 * (swim_speed / 20), center_delta_swim_angle))
        delta_swim_angle_tick += 1
    else:
        head.direction = head.direction.normalize().rotate(delta_swim_angle * (swim_speed / 20))


    if swim_speed < 0.3:
        delta_swim_speed_tick -= 1

    if delta_swim_speed_tick <= 0:
        delta_swim_speed = 5.0
        delta_swim_speed_tick = random.randint(5, 40)

    delta_swim_speed = max(-0.4, delta_swim_speed - 0.3)

    swim_speed = min(20.0, max(0.0, swim_speed + delta_swim_speed * dt * 100))

    head.set_pos(head.pos() + head.direction * swim_speed)

BEH_SWIM_ON_ITSELF = 4
behaviours[BEH_SWIM_ON_ITSELF] = SnakeBehavior(swim_on_itself)