from procedural_math import *
import random

class SnakeBehavior:
    def __init__(self, process_function):
        self.process_function = process_function

    def process(self, snake, dt, **kwargs):

        self.process_function(snake, snake.head(), dt, **kwargs)

behaviours = {}

def follow_mouse(snake, head, dt, **kwargs):
    """
    kwargs: 
        - mouse_pos: Vec2
    """
    diff = kwargs["mouse_pos"] - head.pos()
    
    if diff != Vec2(0, 0):
        head.set_pos(head.pos().lerp(kwargs["mouse_pos"], 0.3))
        head.direction = diff

BEH_FOLLOW_MOUSE = 0
behaviours[BEH_FOLLOW_MOUSE] = SnakeBehavior(follow_mouse)



delta_angle = 0
angle_time = 0
def move_on_itself(snake, head, dt, **kwargs):
    """
    kwargs: 
        - screen_center: Vec2
    """
    if head.direction == Vec2(0, 0):
        head.direction = Vec2(1, 0)

    global delta_angle, angle_time
    if angle_time <= 0:
        delta_angle = random.uniform(-0.1, 0.1)
        angle_time = random.randint(2, 20)
    angle_time -= 1

    head.direction = head.direction.normalize().rotate(delta_angle)

    if abs(head.pos().x - kwargs["screen_center"].x) > 800 or abs(head.pos().y - kwargs["screen_center"].y) > 400:
        head.direction = head.direction.normalize().rotate(math.copysign(0.1, delta_angle))
        angle_time += 1

    head.set_pos(head.pos() + head.direction * 15)

BEH_MOVE_ON_ITSELF = 1
behaviours[BEH_MOVE_ON_ITSELF] = SnakeBehavior(move_on_itself)
