import pyglet
from pyglet.gl import *
import pyglet.graphics.shader

window = pyglet.window.Window()

# Compiling Shader Programs
vertex_source = """
#version 150 core
in vec2 position;
in vec4 colors;
out vec4 vertex_colors;

uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

uniform vec4 outlineColor;
uniform float glowRadius;

void main()
{
    vec4 pos = window.projection * window.view * vec4(position, 0.0, 1.0);
    vec2 direction = normalize(position);
    vec4 outlinePos = vec4(position + direction * glowRadius, 0.0, 1.0);
    gl_Position = window.projection * window.view * outlinePos;
    vertex_colors = mix(colors, outlineColor, 0.5);
}
"""

fragment_source = """
#version 150 core
in vec4 vertex_colors;
out vec4 final_color;

void main()
{
    final_color = vertex_colors;
}
"""

# vert_shader = Shader(vertex_source, 'vertex')
# frag_shader = Shader(fragment_source, 'fragment')
# program = ShaderProgram(vert_shader, frag_shader)

shader_program = pyglet.graphics.shader.ShaderProgram(
    pyglet.graphics.shader.Shader(vertex_source, 'vertex'),
    pyglet.graphics.shader.Shader(fragment_source, 'fragment')
)

# Set up OpenGL
pyglet.gl.glEnable(GL_BLEND)
pyglet.gl.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

vertex_list = shader_program.vertex_list(4, 
    ('v2f', [-0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5]),
    ('c4f', [1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0])
)

# Uniform values
outline_color = (0.0, 1.0, 1.0, 1.0)  # Cyan outline
glow_radius = 0.1

@window.event
def on_draw():
    window.clear()
    shader_program.use()
    
    # Pass uniform data
    shader_program['outlineColor'] = outline_color
    shader_program['glowRadius'] = glow_radius
    
    vertex_list.draw(GL_QUADS)

pyglet.app.run()
