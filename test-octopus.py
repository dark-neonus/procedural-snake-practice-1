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

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glDisable(GL_DEPTH_TEST)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

# Window init end

# ________________________________________________________________________________________________

# Snake parameters

head = ProceduralLimb(
        segments=[ProceduralSegment(100),]
    )

tentacle_start_size = 50
tentacle_reduce = 5
tentacle_lengths = [5, 7, 10, 7, 5]
tentacle_angles = [-50, -30, 0, 30, 50]
tentacle_count = len(tentacle_lengths)

tentacles = {}
for i in range(tentacle_count):
    segments = [ProceduralSegment(calculation_radius=(tentacle_start_size - tentacle_reduce * j)) for j in range(tentacle_lengths[i])]

    tentacles[tentacle_lengths] = ProceduralLimb(
                                    segments=segments,
                                    batch=main_batch,
                                    debug_draw=False
                                )
    


snake = ProceduralLimb(
    segments=segments,
    batch=main_batch,
    debug_draw=False
)
snake1 = ProceduralLimb(
    segments=[ProceduralSegment(calculation_radius=r, radius=r) for r in range(30, 5, -2)],
    batch=main_batch,
    debug_draw=False
)
snake2 = ProceduralLimb(
    segments=[ProceduralSegment(calculation_radius=r, radius=r) for r in range(30, 5, -2)],
    batch=main_batch,
    debug_draw=False
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
    behaviours[BEH_FOLLOW_MOUSE].process(head, dt, screen_center=screen_center, mouse_pos=mouse_pos)


    
    for angle, limb in tentacles.items():
        pass
    
    head.update(dt)
    snake1.update(dt)
    snake2.update(dt)



pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()