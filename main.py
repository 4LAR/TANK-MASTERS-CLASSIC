#
#    STONE ENGINE
#       by 100LAR (100LAR STUDIO)
#           15.03.2021
#

version_engine = 'STONE ENGINE 2.5.0' # версия движка

import time
import datetime
import os
import sys
import traceback

# функции
def get_time(): # получить текущее время
    return time.strftime("%H:%M:%S|%d-%m-%y", time.localtime())

log_list = [] # список строк которые будут показаны в консоли

def log(text, time_log_bool=True, print_console=False): # запись в файл строки со времением
    log_file = open('log.txt', 'a')
    log_file.write((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text) + '\n')
    log_file.close()

def log_screen(text, time_log_bool=True): # вывод строки в консоль
    log_list.append((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text))
    print((('[' + str(get_time()) + '] ') if time_log_bool else '') + str(text))

class Engine_settings(): #
    def __init__(self):
        self.on_text_bool           = False # разрешение на ввод текста
        self.on_mouse_motion_bool   = False # разрешение на получение информации о положении мыши (не работает когда нажата клавиша)
        self.on_mouse_drag_bool     = False # разрешение на получение информации о положении мыши (работает когда нажата клавиша)
        self.on_key_press_bool      = False # разрешение на получение информации о клавишах клавиатуры (нажатие)
        self.on_mouse_press_bool    = False # разрешение на получение информации о клавишах мыши (нажатие)
        self.on_mouse_scroll_bool   = False # разрешение на получение информации о клавишах мыши (скроллинг)
        self.on_mouse_release_bool  = False # разрешение на получение информации о клавишах мыши (отпускание)
        self.on_draw_bool           = False # разрешение на прорисовку
        self.on_update_bool         = False # разрешение на обновление всез классов

        self.window_event_list = { #
            'on_text': 'text',
            'on_mouse_motion': 'x, y, dx, dy',
            'on_mouse_drag': 'x, y, dx, dy, buttons, modifiers',
            'on_key_press': 'symbol, modifiers',
            'on_mouse_press': 'x, y, button, modifiers',
            'on_mouse_scroll': 'x, y, scroll_x, scroll_y',
            'on_mouse_release': 'x, y, button, modifiers'
        }

engine_settings = Engine_settings()

engine_run = True

def exit(): # заставляет закрыть программу
    global engine_run
    engine_run = False
    sys.exit(0)

'''def reboot():
    global engine_run
    engine_run = True
    pyglet.app.stop()
    window.close()'''

#while engine_run:
try:
    engine_run = False
    # библиотеки которые использует движок
    from collections import deque
    import pyglet
    from pyglet import image
    from pyglet.gl import *
    from pyglet.graphics import TextureGroup
    from pyglet.window import key, mouse
    import multiprocessing
    import PIL
    from PIL import ImageFont
    from PIL import Image
    import configparser
    from os import path

    import pickle
    from PIL import ImageEnhance
    import math, random
    import numpy as np
    import collision
    import copy
    import time
    import copy
    import json

    from socket import *

    from socketserver import *

    from weakref import WeakKeyDictionary

    #from PodSixNet.Server import Server
    #from PodSixNet.Channel import Channel

    # расположение нужных каталогов
    img_dir     = path.join(path.dirname(__file__), 'img') # путь к папке с картинками
    sound_dir   = path.join(path.dirname(__file__), 'sound') # путь к папке со звуком
    font_dir    = path.join(path.dirname(__file__), 'fonts') # путь к папке со шрифтами

    objects_other = []      # разные объекты не причастные к прорисовке или считыванию нажатий
    list_objects_other = {}
    list_objects_other_index = 0

    objects_display = []    # объекты для отрисовки
    list_main_game_obj = {}
    list_objects_display_index = 0

    def get_name_object(obj):
        return (str(obj).split('.')[1]).split(' ')[0]

    ###
    def get_obj_other(obj_name):
        return objects_other[list_objects_other[obj_name]]

    def clear_objects_other(): # функция для очищения объектов
        global list_objects_other
        global list_objects_other_index
        list_objects_other = {}
        list_objects_other_index = 0
        objects_other.clear()
        log_screen('OTHER CLEAR')

    def del_obj_other(obj_name): # функция для удаления объекта по его названию (бесполезный кусок говна)
        obj_delete_bool = False
        for i in range(len(objects_display)): # проверяем каждый объект
            if (str(objects_display[i]).split('.')[1]).split(' ')[0] == obj_name: # если попадается нужный объект
                objects_other.pop(i)
                obj_delete_bool = True
                log_screen('OTHER OBJECT DELETED: ' + obj_name)
                return True
        if not obj_delete_bool: # на случай отсутсвия нужного объекта
            log_screen('OTHER OBJECT NOT DELETED: ' + obj_name)
            return False

    def add_objects_other(obj): # функция для добавления объектов
        global list_objects_other
        global list_objects_other_index

        list_objects_other[get_name_object(obj).lower()] = list_objects_other_index
        list_objects_other_index += 1
        objects_other.append(obj)
        log_screen('OTHER ADD: ' + str(obj))

    ###

    def clear_display(): # функция для очищения объектов
        global list_main_game_obj
        global list_objects_display_index
        list_main_game_obj = {}
        list_objects_display_index = 0
        objects_display.clear()
        log_screen('DISPLAY CLEAR')

    code = ''
    files = []

    def del_obj_display(obj_name): # функция для удаления объекта по его названию (бесполезный кусок говна)
        obj_delete_bool = False
        for i in range(len(objects_display)): # проверяем каждый объект
            if (str(objects_display[i]).split('.')[1]).split(' ')[0] == obj_name: # если попадается нужный объект
                objects_display.pop(i)
                #list_main_game_obj.pop(obj_name)
                obj_delete_bool = True
                log_screen('DISPLAY OBJECT DELETED: ' + obj_name)
                return True
        if not obj_delete_bool: # на случай отсутсвия нужного объекта
            log_screen('DISPLAY OBJECT NOT DELETED: ' + obj_name)
            return False

    def add_display(obj): # функция для добавления объектов
        global list_main_game_obj
        global list_objects_display_index

        list_main_game_obj[get_name_object(obj).lower()] = list_objects_display_index
        list_objects_display_index += 1
        objects_display.append(obj)
        log_screen('DISPLAY ADD: ' + str(obj))

    def get_obj_display(obj_name):
        return objects_display[list_main_game_obj[obj_name]]


    class settings():
        def __init__(self):
            self.width = 1280 # ширина окна
            self.height = 720 # высота окна
            self.full_screen = 0 # как будет работать окно (0 - окно с рамками, 1 - окно без рамок, полный экран (не стабильно) )
            self.gamma = 1.0 # гамма (не используется)

            self.fps = 120 # максимальный fps при обновлении классов

            self.show_fps = False # показ текущего fps

            self.console = False # включение консоли (не используется)

            self.sound_volume = 0.01 # громкость звука (1 - максимальное значение)

            self.use_window = True # False для включения только консольного режима (не используется)

            self.use_numba = False # Использовать библиотку numba для более быстрых рассчётов

            self.read_settings() # читаем настроки

        def save_settings(self):
            config = configparser.ConfigParser()

            config.add_section("Screen")
            config.set("Screen", "use_window", str(self.use_window)) # хз как делать
            config.set("Screen", "width", str(self.width))
            config.set("Screen", "height", str(self.height))
            config.set("Screen", "full-screen", str(self.full_screen))

            config.add_section("User_interface")
            config.set("User_interface", "show-fps", str(self.show_fps))
            config.set("User_interface", "console", str(self.console))

            config.add_section("Sound")
            config.set("Sound", "volume", str(self.sound_volume))

            config.add_section("Engine")
            config.set("Engine", "use_numba", str(self.use_numba))


            with open("settings.txt", "w") as config_file: # запись файла с настройками
                config.write(config_file)


        def read_settings(self):
            if not os.path.exists("settings.txt"): # проверка файла с настройками
                self.save_settings()
                self.read_settings()
            else:
                config = configparser.ConfigParser()
                config.read("settings.txt")
                self.use_window = True if (config.get("Screen", "use_window")).lower() == 'true' else False
                self.width = int(config.get("Screen", "width"))
                self.height = int(config.get("Screen", "height"))
                self.full_screen = int(config.get("Screen", "full-screen"))

                self.show_fps = True if (config.get("User_interface", "show-fps")).lower() == 'true' else False

                self.console = True if (config.get("User_interface", "console")).lower() == 'true' else False

                self.sound_volume = float(config.get("Sound", "volume"))

                self.use_numba = True if (config.get("Engine", "use_numba")).lower() == 'true' else False
                if self.use_numba:
                    import numba # типо оптимизация

    settings = settings() # инициализация класса с настройками


    class file_code():
        def __init__(self):
            self.files = []
            self.code = ''


    def load_obj_file(name ):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)

    # получение названия файла с объектами (если на задано то будет <<objects.list>>)
    file_list_objects = 'objects' #
    if len(sys.argv) > 1:
        file_list_objects = sys.argv[1]
        # получаем названия файлов с нужными объктами
        file_objects = (open('objects/'+file_list_objects+'.list', 'r', encoding="utf-8").read()).split('\n') #
        for i in range(len(file_objects)-1): #
            files.append([file_objects[i], 0])
            print('IMPORT: ' + file_objects[i])

        # чтение файлов содержащих в себе классы
        for i in range(len(files)): #
            file_objects = open('objects/' + files[i][0], 'r', encoding="utf-8") #
            code += file_objects.read() + '\n' #
            files[i][1] = len(code.split('\n')) #
            file_objects.close() #
    else:
        file = load_obj_file('objects')

        code = file.code
        files = file.files

    if len(sys.argv) > 2:
        settings.use_window = True if sys.argv[2].lower() == 'true' else False

    if settings.use_window:
        if settings.full_screen == 1: # окно без рамок
            window = pyglet.window.Window(settings.width, settings.height, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, vsync=True)
        elif settings.full_screen == 2: # полный экран
            window = pyglet.window.Window(settings.width, settings.height, fullscreen=settings.full_screen, vsync=True)
        else: # окно с рамками
            window = pyglet.window.Window(settings.width, settings.height, vsync=True)

        window.set_caption(version_engine) # изменение названия окна

        def change_window_settings():
            #window.width = settings.width
            #window.height = settings.height
            window.set_fullscreen(fullscreen=(True if settings.full_screen == 2 else False), width=settings.width, height=settings.height)


        width = settings.width # ширина окна
        height = settings.height # высота окна

        # тут магия opengl
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        viewport = window.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()

        keyboard = pyglet.window.key.KeyStateHandler() #
        window.push_handlers(keyboard) #

    print('STRING: '  +str(len(code.split('\n')))) #
    exec(code) # запуск всего кода который мы прочитали из файлов

    class FPS_label(): # класс для показа fps в левом верхнем угле
        def __init__(self, x, y, size, color):
            self.x = x # позиция по высоте
            self.y = y # позиция по высоте (инвертировано)
            self.size = size # размер шрифта
            self.color = color # цвет шрифта

            self.label = pyglet.text.Label('0',
                font_size=self.size,
                x=self.x, y=self.y,
                color=self.color) # создаём текст

        def update(self): # постоянно обновляем показания
            self.label.text = str(int(pyglet.clock.get_fps()))

        def draw(self): # прорисовываем текст
            self.label.draw()

    fps_label = FPS_label(0, settings.height - settings.height//40, 18, (50, 255, 50, 255)) # добавляем класс

    if settings.use_window:
        keys = key.KeyStateHandler()
        window.push_handlers(keys) # делаем так чтобы мы могли считать нажатые клавиши

    class Time_fps(): # для обновления основного цикла (потом заменится), попытка многопоточности
        def __init__(self):
            self.delay = 1/(settings.fps)                   # задержка таймера
            self.time = time.perf_counter() + self.delay    # таймер
    time_fps = Time_fps()

    def check_Exception(o, e, event): # проверка на ошибку (есть ли в таком классе эта функция)
        if str(e) != "'" + (str(o).split('.')[1]).split(' ')[0] + "' object has no attribute '"+event+"'":
            print(str(o) + ' : ' + str(event) + ' : ' + str(e))

    def on_update(dt): # функция для обновления основного цикла
        if engine_settings.on_update_bool:
            for o in objects_other: # проходим по каждому объекту в цикле
                try: # проверяем есть ли у объекта такая функция
                    o.update()
                except Exception as e:
                    check_Exception(o, e, 'update')
            for o in objects_display: # проходим по каждому объекту в цикле
                try: # проверяем есть ли у объекта такая функция
                    o.update()
                except Exception as e:
                    check_Exception(o, e, 'update')

    def on_draw(dt): # функция для прорисовки
        window.clear()
        if engine_settings.on_draw_bool:
            for o in objects_display: # проходим по каждому объекту в цикле
                try: # проверяем есть ли у объекта такая функция
                    o.draw()
                except Exception as e:
                    check_Exception(o, e, 'draw')
                        #traceback.format_exc()
            for o in objects_other: # проходим по каждому объекту в цикле
                try: # проверяем есть ли у объекта такая функция
                    o.draw()
                except Exception as e:
                    check_Exception(o, e, 'draw')

        if settings.show_fps: # если нам надо показать fps
            fps_label.update()
            fps_label.draw()


    def update(dt): # функция для обновления остальныйх функция в классе
        if time_fps.time <= time.perf_counter():
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

            on_update(dt) # обновляем основной цикл
            on_draw(dt) # рисуем

            #if settings.full_screen == 2: # для стабильной работы полноэкранного режима (без это штуки разрывается изображение)
            #    pyglet.clock.unschedule(update)
            #    pyglet.clock.schedule_interval(update, 1/pyglet.clock.get_fps())

    if settings.use_window:
        pyglet.clock.schedule_interval(update, 1/settings.fps) # запускаем цикл с частотой 1/settings.fps мс
    else:
        while True:
            if time_fps.time <= time.perf_counter():
                on_update(0)
                time_fps.time = time.perf_counter() + time_fps.delay

    #pyglet.clock.schedule_interval(on_update, 1/settings.fps)
    #pyglet.clock.schedule_interval(on_draw, 1/settings.fps)

    #proc = multiprocessing.Process(target=update, name='update').start()
    #proc = multiprocessing.Process(target=on_update, name='on_update').start()
    #proc = multiprocessing.Process(target=on_draw, name='on_draw').start()
    if settings.use_window:
        pyglet.app.run() # запускаем эту дичь

except Exception as e: # если крашнулся движок, то ошибка покажется на экране и запишетсяв log файл
    print("FATAL ERROR: " + str(traceback.format_exc()))
    log('FATAL ERROR: ' + str(traceback.format_exc()))
    exit()
