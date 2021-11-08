version = 'TANK MASTERS:CLASSIC 0.0.1'

import math, random
import numpy as np
import collision
import copy

pyglet.gl.glLineWidth(3)
pyglet.gl.glEnable (GL_LINE_SMOOTH)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

pyglet.font.add_file('font/pixel.ttf')

v = collision.Vector # для создания полигонов

engine_settings.on_text_bool           = False
engine_settings.on_mouse_motion_bool   = True
engine_settings.on_mouse_drag_bool     = True
engine_settings.on_key_press_bool      = True
engine_settings.on_mouse_press_bool    = True
engine_settings.on_mouse_release_bool  = True
engine_settings.on_draw_bool           = True
engine_settings.on_update_bool         = True

def main():
    print('HELLO WORLD')
    #menu()
    play()
