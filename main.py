#
#    STONE ENGINE 2
#       by 100LAR (100LAR STUDIO)
#           08.06.2022
#

version_engine = 'STONE-ENGINE-2 v1.0.0'

# import
import os
import sys
import time
import math
import random
import datetime

# pyglet (pyOpenGL)
import pyglet
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

# многопоточность
import multiprocessing
import threading

# обработка изображений
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageEnhance
from collections import deque

# для конфигов
import configparser
import json

# коллизия
import collision

# для сохранений объектов
import pickle

# массивы
import numpy as np
import copy

# сокеты (для мультиплеера)
from socket import *
from socketserver import *
from weakref import WeakKeyDictionary

# информация о экране
import screeninfo

# для обработки ошибок
import traceback

# импортирование своих библиотек
sys.path.append('libs')
from get_time import *
from console import *
from args import *
from fuckimport import *
from pickle_func import *
from engine_settings import *
from settings import *
from fps_monitor import *
from check_exception import *

game_args = game_args()
console_term = console_term(game_args.args.log)
fuck_import = fuck_import()
engine_settings = Engine_settings()
settings = settings()

# константы директорий
img_dir     = os.path.join(os.path.dirname(__file__), 'img') # путь к папке с картинками
sound_dir   = os.path.join(os.path.dirname(__file__), 'sound') # путь к папке со звуком
font_dir    = os.path.join(os.path.dirname(__file__), 'fonts') # путь к папке со шрифтами

engine_run = True

# заставляет закрыть программу
def exit():
    global engine_run
    engine_run = False
    #sys.exit(0)
    os._exit(0)

#------------------------------------------------------------------------------#

def check_Exception(o, e, event): # проверка на ошибку (есть ли в таком классе эта функция)
    if str(e) != "'" + (str(o).split('.')[1]).split(' ')[0] + "' object has no attribute '" + event + "'":
        console_term.print(str(o) + ' : ' + str(event) + ' : ' + str(e), 2)

#------------------------------------------------------------------------------#

# списоки объектов
objects_other = []
list_objects_other = {}
list_objects_other_index = 0

objects_display = []
list_main_game_obj = {}
list_objects_display_index = 0

# функция для получения имени объекта
def get_name_object(obj):
    return (str(obj).split('.')[1]).split(' ')[0]

# функция для получения объекта по его имени
def get_obj_other(obj_name):
    return objects_other[list_objects_other[obj_name]]

# функция для удаления всех объектов
def clear_objects_other():
    global list_objects_other
    global list_objects_other_index
    list_objects_other = {}
    list_objects_other_index = 0
    objects_other.clear()
    console_term.print('OTHER CLEAR')

def clear_display():
    global list_main_game_obj
    global list_objects_display_index
    list_main_game_obj = {}
    list_objects_display_index = 0
    objects_display.clear()
    console_term.print('DISPLAY CLEAR')

# функция для удаления объекта по его названию (бесполезный кусок говна)
def del_obj_other(obj_name):
    obj_delete_bool = False

    # проверяем каждый объект
    for i in range(len(objects_display)):
        # если попадается нужный объект
        if (str(objects_display[i]).split('.')[1]).split(' ')[0] == obj_name:
            objects_other.pop(i)
            obj_delete_bool = True
            console_term.print('OTHER OBJECT DELETED: ' + obj_name, 0)
            return True

    # на случай отсутсвия нужного объекта
    if not obj_delete_bool:
        console_term.print('OTHER OBJECT NOT DELETED: ' + obj_name, 2)
        return False

# функция для удаления объекта по его названию (бесполезный кусок говна)
def del_obj_display(obj_name):
    obj_delete_bool = False

    # проверяем каждый объект
    for i in range(len(objects_display)):
        # если попадается нужный объект
        if (str(objects_display[i]).split('.')[1]).split(' ')[0] == obj_name:
            objects_display.pop(i)
            obj_delete_bool = True
            console_term.print('DISPLAY OBJECT DELETED: ' + obj_name, 0)
            return True

    # на случай отсутсвия нужного объекта
    if not obj_delete_bool:
        console_term.print('DISPLAY OBJECT NOT DELETED: ' + obj_name, 0)
        return False

# функция для добавления объектов
def add_objects_other(obj):
    global list_objects_other
    global list_objects_other_index

    list_objects_other[get_name_object(obj).lower()] = list_objects_other_index
    list_objects_other_index += 1
    objects_other.append(obj)
    console_term.print('OTHER ADD: ' + str(obj), 0)

# функция для добавления объектов
def add_display(obj):
    global list_main_game_obj
    global list_objects_display_index

    list_main_game_obj[get_name_object(obj).lower()] = list_objects_display_index
    list_objects_display_index += 1
    objects_display.append(obj)
    console_term.print('DISPLAY ADD: ' + str(obj), 0)

def get_obj_display(obj_name):
    return objects_display[list_main_game_obj[obj_name]]

#------------------------------------------------------------------------------#

def on_update(dt): # функция для обновления основного цикла
    if engine_settings.on_update_bool:
        # проходим по каждому объекту в цикле
        for o in objects_other:
            try: # проверяем есть ли у объекта такая функция
                o.update()
            except Exception as e:
                check_Exception(o, e, 'update')

        # проходим по каждому объекту в цикле
        for o in objects_display:
            try: # проверяем есть ли у объекта такая функция
                o.update()
            except Exception as e:
                check_Exception(o, e, 'update')

def on_draw(dt): # функция для прорисовки
    #  очищиаем экран
    window.clear()
    if engine_settings.on_draw_bool:
        # проходим по каждому объекту в цикле
        for o in objects_display:
            try: # проверяем есть ли у объекта такая функция
                o.draw()
            except Exception as e:
                check_Exception(o, e, 'draw')

        # проходим по каждому объекту в цикле
        for o in objects_other:
            try: # проверяем есть ли у объекта такая функция
                o.draw()
            except Exception as e:
                check_Exception(o, e, 'draw')

    # показ кадров
    if settings.show_fps:
        fps_label.update()
        fps_label.draw()

# функция для обновления остальныйх функция в классе
def update(dt):
    for type_event in engine_settings.window_event_list:
        exec('''
@window.event
def '''+type_event+'''('''+engine_settings.window_event_list[type_event]+'''):
    if engine_settings.'''+type_event+'''_bool:
        for o in objects_other:
            try:
                o.'''+ type_event +'''('''+engine_settings.window_event_list[type_event]+''')
            except Exception as e:
                check_Exception(o, e, "'''+type_event+'''")
        for o in objects_display:
            try:
                if o.'''+ type_event +'''('''+engine_settings.window_event_list[type_event]+'''):
                    return pyglet.event.EVENT_HANDLED
            except Exception as e:
                check_Exception(o, e, "'''+type_event+'''")
            ''')

    # обновляем основной цикл
    on_update(dt)
    # рисуем
    on_draw(dt)

#------------------------------------------------------------------------------#

if (game_args.args.source.split('.')[1] == 'list'):
    fuck_import.read(game_args.args.source.split('.')[0])
    fuck_import.build()

elif (game_args.args.source.split('.')[1] == 'pkl'):
    fuck_import.read_pack(game_args.args.source.split('.')[0])

else:
    console_term.print('Bad source argument', 3)

CODE = fuck_import.get_code()

if (game_args.args.pack and CODE):
    print(game_args.args.pack)
    fuck_import.pack(game_args.args.source.split('.')[0])

else:
    if (CODE):
        if settings.use_window:

            def change_window_settings():
                window.set_fullscreen(fullscreen=(True if settings.full_screen == 2 else False), width=settings.width, height=settings.height)

            if settings.full_screen == 1: # окно без рамок
                window = pyglet.window.Window(
                    settings.width, settings.height,
                    style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                    vsync=True
                )
            elif settings.full_screen == 2: # полный экран
                window = pyglet.window.Window(
                    settings.width, settings.height,
                    fullscreen=settings.full_screen,
                    vsync=True
                )
            else: # окно с рамками
                window = pyglet.window.Window(
                    settings.width, settings.height,
                    vsync=True
                )

        window.set_caption(version_engine)

        width = settings.width # ширина окна
        height = settings.height # высота окна

        fps_label = FPS_label(0, settings.height - settings.height//40, 18, (50, 255, 50, 255))

        keyboard = key.KeyStateHandler()
        window.push_handlers(keyboard)

        keys = key.KeyStateHandler()
        window.push_handlers(keys) # делаем так чтобы мы могли считать нажатые клавиши

        #console_term.run_terminal()
        #console_term.stop_terminal()
        try:

            exec(CODE)
            pyglet.clock.schedule_interval(update, 1/settings.fps)
            pyglet.app.run()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            line_error = traceback.extract_tb(exc_tb)[-1][1] - 1

            lines = 0
            for i in range(len(fuck_import.files)):
                if (lines > line_error):
                    console_term.print(str(e), 3)
                    console_term.print(str(fuck_import.files[i-1][0]) + ':' + str(lines - line_error) + ' >> ' + str(CODE.split('\n')[line_error]), 3)
                    break;

                lines += fuck_import.files[i][1]

            exit()
