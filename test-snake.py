import pyglet

from pyglet.math import Vec2
from pyglet.gl import *

from lib.snake_behavior import *
from lib.procedural_objects.snake import ProceduralSnake
from lib.procedural_objects.circle import ProceduralCircle
from lib.graphic.color import Color

# ________________________________________________________________________________________________

# Window init

screen = pyglet.canvas.get_display().get_default_screen()
screen_width = screen.width
screen_height = screen.height

screen_center = Vec2(screen_width / 2, screen_height / 2)

window = pyglet.window.Window(screen_width, screen_height, "Snake")
window.maximize()

main_batch = pyglet.graphics.Batch()

mouse_pos: Vec2 = Vec2(0, 0)
mouse_delta: Vec2 = Vec2(0, 0)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glDisable(GL_DEPTH_TEST)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

# Window init end

# ________________________________________________________________________________________________

# Snake parameters


HD_ENABLE =  1
COBRA_DEFORM = 0

if HD_ENABLE:
    # HD Snake
    segments = [ProceduralCircle(calculation_radius=r // 3, radius=int(r/2)) for r in range(40*2, 5*2, -1)]
else:
    # Normal Snake
    segments = [ProceduralCircle(calculation_radius=r, radius=r) for r in range(60, 5, -3)]
if COBRA_DEFORM:

    deform_n = int(len(segments) / 5)

    size_deltas = list(range(1, deform_n)) + list(range(deform_n - 1, 0, -1))

    for i in range(len(size_deltas)):
        segments[i + 1].radius += size_deltas[i] * int(60 / deform_n)

snake = ProceduralSnake(
    segments=segments,
    batch=main_batch,
    debug_draw=False,
    fill_color=Color.get_transparent_color(Color.magenta, 80),
    behavior=BEH_FOLLOW_MOUSE
)
snake1 = ProceduralSnake(
    segments=[ProceduralCircle(calculation_radius=r, radius=r) for r in range(30, 5, -2)],
    batch=main_batch,
    debug_draw=False,
    behavior=BEH_MOVE_ON_ITSELF,
    fill_color=Color.get_transparent_color(Color.magenta, 80),
)
snake2 = ProceduralSnake(
    segments=[ProceduralCircle(calculation_radius=r, radius=r) for r in range(30, 5, -2)],
    batch=main_batch,
    debug_draw=False,
    behavior=BEH_SWIM_ON_ITSELF,
    fill_color=Color.get_transparent_color(Color.magenta, 80),
)
snake.head().set_pos(screen_center)
snake1.head().set_pos(screen_center)
snake2.head().set_pos(screen_center)

# Snake parameters end

# ________________________________________________________________________________________________

# Events and functions

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos, mouse_delta
    mouse_pos = Vec2(x, y)
    mouse_delta = Vec2(dx, dy)

@window.event
def on_draw():
    window.clear()
    main_batch.draw()



def update(dt):
    
    snake.update(dt, screen_center=screen_center, mouse_pos=mouse_pos)
    snake1.update(dt, screen_center=screen_center, mouse_pos=mouse_pos)
    snake2.update(dt, screen_center=screen_center, mouse_pos=mouse_pos)



pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()