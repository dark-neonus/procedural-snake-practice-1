import pyglet
from pyglet.window import key

global n
global vertices
global colors
window = pyglet.window.Window()
n = 0
vertices = []
colors = []
polygon = None
main_Batch = pyglet.graphics.Batch()


@window.event
def on_draw():
    window.clear()
    main_Batch = pyglet.graphics.Batch()
    if n > 2:
        polygon = main_Batch.add(n, pyglet.gl.GL_POLYGON, None,
                                         ('v2i', vertices),
                                         ('c3B', colors))
    main_Batch.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.DELETE:
        global n;
        global vertices
        global colors
        vertices = []
        colors = []
        n = 0


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        global n
        vertices.append(x)
        vertices.append(y)
        n = n + 1
        colors.append(255)
        colors.append(255)
        colors.append(255)

pyglet.app.run()