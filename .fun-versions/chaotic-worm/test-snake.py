import pyglet
import random

from procedural_math import *

from snake_behavior import *

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

# Window init end

# ________________________________________________________________________________________________

# Snake parameters


HD_ENABLE =  0
COBRA_DEFORM = 0

if HD_ENABLE:
    # HD Snake
    segments = [ProceduralSegment(calculation_radius=25, radius=int(r/2)) for r in range(40*2, 5*2, -1)]
else:
    # Normal Snake
    segments = [ProceduralSegment(calculation_radius=90, radius=r) for r in range(65, 5, -4)]

if COBRA_DEFORM:

    deform_n = int(len(segments) / 5)

    size_deltas = list(range(1, deform_n)) + list(range(deform_n - 1, 0, -1))

    for i in range(len(size_deltas)):
        segments[i + 1].radius += size_deltas[i] * int(60 / deform_n)

snake = ProceduralLimb(
    segments=segments,
    batch=main_batch,
    debug_draw=True
)
snake.head().set_pos(screen_center)

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
    behaviours[BEH_MOVE_ON_ITSELF].process(snake, dt, screen_center=screen_center, mouse_pos=mouse_pos)
    snake.update(dt)


pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()