version = 'TANK MASTERS:CLASSIC 0.9.0'

window.set_caption(version_engine + ' | ' + version)

import math, random
import numpy as np
import collision
import copy

pyglet.gl.glLineWidth(3)
pyglet.gl.glEnable (GL_LINE_SMOOTH)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

pyglet.font.add_file('assets/font/pixel.ttf')

v = collision.Vector # для создания полигонов

engine_settings.on_text_bool           = False
engine_settings.on_mouse_motion_bool   = True
engine_settings.on_mouse_drag_bool     = True
engine_settings.on_key_press_bool      = True
engine_settings.on_mouse_press_bool    = True
engine_settings.on_mouse_release_bool  = True
engine_settings.on_draw_bool           = True
engine_settings.on_update_bool         = True

def off_input():
    engine_settings.on_text_bool           = False
    engine_settings.on_mouse_motion_bool   = True
    engine_settings.on_mouse_drag_bool     = False
    engine_settings.on_key_press_bool      = False
    engine_settings.on_mouse_press_bool    = False
    engine_settings.on_mouse_release_bool  = False
    engine_settings.on_draw_bool           = True
    engine_settings.on_update_bool         = True

def on_input():
    engine_settings.on_text_bool           = False
    engine_settings.on_mouse_motion_bool   = True
    engine_settings.on_mouse_drag_bool     = True
    engine_settings.on_key_press_bool      = True
    engine_settings.on_mouse_press_bool    = True
    engine_settings.on_mouse_release_bool  = True
    engine_settings.on_draw_bool           = True
    engine_settings.on_update_bool         = True

def menu_cursor():
    image = pyglet.image.load('img/cursor/cursor_menu.png')
    texture = image.get_texture()
    texture.width = settings.height//50
    texture.height = settings.height//50

    cursor = pyglet.window.ImageMouseCursor(texture, 9, 9)
    window.set_mouse_cursor(cursor)

def show_cursor():
    window.set_mouse_visible(True)

def hide_cursor():
    window.set_mouse_visible(False)

def main():
    # if FIRST_START:
    #     first_name()
    # else:
    #     menu()
    menu()
