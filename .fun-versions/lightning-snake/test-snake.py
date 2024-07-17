import pyglet

from procedural_math import *

screen = pyglet.canvas.get_display().get_default_screen()
screen_width = screen.width
screen_height = screen.height

window = pyglet.window.Window(screen_width, screen_height, "Snake")
window.maximize()

main_batch = pyglet.graphics.Batch()

mouse_pos: Vec2 = Vec2(0, 0)
mouse_delta: Vec2 = Vec2(0, 0)


HD_ENABLE =  0
COBRA_DEFORM = 0

if HD_ENABLE:
    # HD Snake
    segments = [ProceduralSegment(calculation_radius=25, radius=r) for r in range(65, 5, -1)]
else:
    # Normal Snake
    segments = [ProceduralSegment(calculation_radius=70, radius=r) for r in range(65, 5, -4)]

if COBRA_DEFORM:

    deform_n = int(len(segments) / 5)

    size_deltas = list(range(1, deform_n)) + list(range(deform_n - 1, 0, -1))

    for i in range(len(size_deltas)):
        segments[i + 1].radius += size_deltas[i] * int(60 / deform_n)

snake = ProceduralLimb(
    segments=segments,
    batch=main_batch
)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos, mouse_delta
    mouse_pos = Vec2(x, y)
    mouse_delta = Vec2(dx, dy)

@window.event
def on_draw():
    window.clear()
    main_batch.draw()

def process_head() -> None:
    diff = mouse_pos - snake.head().pos()

    if diff != Vec2(0, 0):
        snake.head().set_pos(snake.head().pos().lerp(mouse_pos, 0.3))
        snake.head().direction = diff

def update(dt):
    process_head()
    snake.update(dt)

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()