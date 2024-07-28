import pyglet
from pyglet.math import Vec2
from lib.blueprint.octopus import *

from pyglet.math import Vec2
from pyglet.gl import *

from lib.snake_behavior import *
from lib.procedural_objects.snake import ProceduralSnake
from lib.procedural_objects.circle import ProceduralCircle
from lib.procedural_objects.octopus import Octopus
from lib.blueprint.octopus import OctopusBlueprint
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

# Octopus parameters

"""
# Test octopus blueprint generation

blueprint = OctopusBlueprint(
    head_sizes=[150, 140, 130],
    tentacle_lengths=[10, 12, 15, 12, 10],
    tentacle_angles=[-90, -50, 0, 50, 90],
    tentacle_start_size=32,
    tentacle_size_reduction=2,
    fill_color=Color.get_transparent_color(Color.magenta, 100)
)

blueprint.save(os.path.join("blueprints", "octopuses", "test-octopus.json"))

# End test octopus blueprint
"""

blueprint = OctopusBlueprint()
blueprint.load(os.path.join("blueprints", "octopuses", "regular-octopus.json"))

octopus: Octopus = blueprint.create_octopus(
    batch=main_batch,
    debug_draw=False,
    behavior=BEH_FOLLOW_MOUSE,
    additional_tentacle_calculation_radius=30
    )


    
#  ________________________________________________________________________________________________

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



octopus.head.head().set_pos(screen_center)

octopus_fill_color = octopus.head.fill_color

tmp_head_pos = octopus.head.head().pos()
delta_vector = Vec2(0, 0)

color_change: float = 0.0
delta_change: float = 0.0

def update(dt):
    global delta_vector, tmp_head_pos, delta_change, color_change

    delta_vector = tmp_head_pos - octopus.head.head().pos()
    tmp_head_pos = octopus.head.head().pos()

    if delta_vector.mag < 15.0:
        delta_change = max(-10.0, min(0.0, delta_change - 0.1))
    else:
        delta_change = min(5.0, max(0.0, int(delta_vector.mag) / 20))

    color_change = max(0.0, min(100.0, color_change + delta_change))

    new_color = (
        50 + int(color_change),
        150 - int(color_change * 1.5),
        150 - int(color_change),
        80
    )

    octopus.set_fill_color(new_color)
    octopus.set_border_colro(new_color)

    octopus.update(dt, screen_center=screen_center, mouse_pos=mouse_pos)
      



pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()