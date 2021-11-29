#
#
# 16.03.2021
#


class setings_game(): # класс который содержит себе информацию о разрешениях и считывает нажатия определённых кнопок
    def __init__(self):
        self.draw_poligons = False # разрешение на прорисовку полигонов
        self.draw_info_text = False # разрешение на прорисовку информации о игроке
        self.draw_console = False # разрешение на прорисовку и использование консоли

        self.draw_rain = False # разрешение на прорисовку дождя

    def on_key_press(self, symbol, modifiers): #
        if settings.console:
            if symbol == key.F1: # если мы нажали F1, то мы включаем консоль или выключаем (запрещаем движку всё кроме прорисовки и считывание нажатие клавиш)
                if self.draw_console:
                    self.draw_console = False
                    engine_settings.on_text_bool = False
                    engine_settings.on_mouse_motion_bool   = True
                    engine_settings.on_mouse_drag_bool     = True
                    engine_settings.on_mouse_press_bool    = True
                    engine_settings.on_mouse_release_bool  = True
                else:
                    self.draw_console = True
                    engine_settings.on_text_bool = True
                    engine_settings.on_mouse_motion_bool   = False
                    engine_settings.on_mouse_drag_bool     = False
                    engine_settings.on_mouse_press_bool    = False
                    engine_settings.on_mouse_release_bool  = False

            '''
            if symbol == key.F3: # если мы нажали F2, то изменяем показ полигонов
                if self.draw_poligons:
                    self.draw_poligons = False
                else:
                    self.draw_poligons = True

            if symbol == key.F2: # если мы нажали F3, то изменяем показ информации о игроке
                if self.draw_info_text:
                    self.draw_info_text = False
                else:
                    self.draw_info_text = True

            if symbol == key.F4: # если мы нажали F4, то изменяем показ дождя
                if self.draw_rain:
                    self.draw_rain = False
                else:
                    self.draw_rain = True
            '''

class Console(): # класс игровой консоли
    def __init__(self):
        self.draw_console = False # разрешение на прорисовку и использование консоли

        self.size_terminal = settings.height//3 # высота терминала

        self.label = label(0, settings.height - self.size_terminal, settings.width, self.size_terminal, (0, 0, 0), alpha=150) # создаём фон для терминала

        self.command_ = ' >> ' # символы которые показывают что мы можем вводить комманду
        self.command = '' # здесь будет записываться сама комманда

        # символы которые можно записать в консоль
        self.symbol_list = '1234567890!@$%^&*()-=_+qwertyuiop[]asdfghjkl;zxcvbnm,.QWERTYUIOPASDFGHJKL:"ZXCVBNM<>? йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

        self.text = [] # список который содержит в себе строки (дбля прорисовки log и комманд)
        text_size = settings.height//80 # высота каждой строки
        pos_y = settings.height - self.size_terminal + text_size # изначальная позиция для прорисовки
        for i in range(1, int(self.size_terminal//(text_size * 1.5)), 1): # добавляем строки
            self.text.append(text_label(0, pos_y + (text_size * 1.5) * i, '', load_font=True, font='default.ttf', size=text_size, anchor_x='left', color = (180, 180, 180, 255)))
        # добавляем строку в которую будем вводить комманду
        self.text.append(text_label(0, pos_y + (text_size * 1.5) * 0, self.command_, load_font=True, font='default.ttf', size=text_size, anchor_x='left', color = (180, 180, 180, 255)))

    def execute_command(self, command): # функция для запуска комманды
        if command.split(' ')[0] == 'python': # если у комманды аргумент python
            python_command = ''
            for c in (command.split(' ')[1:]):
                python_command += c + ' '
            log_screen(exec(python_command)) # выполняем и выводим комманду

        elif command == 'fps': # команда для показа фпс
            if settings.show_fps:
                settings.show_fps = False
            else:
                settings.show_fps = True

        else:
            exec(command + '()')



    def on_key_press(self, symbol, modifiers):
        if objects_other[0].draw_console: # если мы выводим консоль, разрешаем пользователя нажимать на backspace и enter
            if symbol == key.BACKSPACE:
                self.command = self.command[:len(self.command)-1]
            elif symbol == key.ENTER:
                if len(self.command) > 0:
                    log_screen(self.command) # выводим комманду
                    command = self.command
                    self.command = ''
                    self.execute_command(command) # выполняем комманду

    def on_text(self, text): # функция для получения символов которые мы вводим с клавиатуры
        if objects_other[0].draw_console:
            try:
                if text in self.symbol_list: # сравниваем символ со списком разрешённых символов, если такого символа нет, то просто не добавляем его в комманду
                    self.command += text
            except:
                pass

    def draw(self): # прориссовываем консоль если есть разрешение (работает через жопу)
        if objects_other[0].draw_console:
            self.label.draw()
            list = log_list[len(log_list) - len(self.text) : len(log_list)]

            for i in range(len(self.text)-1):
                try:
                    self.text[i].label.text = list[len(self.text)-1 - i]
                    self.text[i].draw()
                except:
                    pass

            self.text[len(self.text)-1].label.text = self.command_ + self.command
            self.text[len(self.text)-1].draw()

# добавляем классы в основной цикл
add_objects_other(setings_game())
add_objects_other(Console())

class info_panel(): # информация о игроке
    def __init__(self):
        self.text_coords = { # позиции строк на которые будет выводится информация
            'ver_engine': 0,
            'ver_game': 1,
            'fps': 2,
            'pos_x': 3,
            'pos_y': 4,
            'rot_body': 5,
            'rot_tower': 6,
            'start_engine': 7,
            'health': 8
        }

        self.text = [] # список со строками
        text_size = settings.height//100 # высота каждой строки
        pos_y = settings.height//2 # изначальная позиция первой строки
        for i in range(len(self.text_coords)): # создаём строки
            self.text.append(text_label(0, pos_y + (text_size * 1.5) * i, '', load_font=True, font='default.ttf', size=text_size, anchor_x='left', color = (180, 180, 180, 255)))

    def update(self):
        if objects_other[0].draw_info_text: # если мы дали разрешение на прорисовку информации, то обновляем информацию
            self.text[self.text_coords['ver_engine']].label.text = 'ENGINE: ' + version_engine
            self.text[self.text_coords['ver_game']].label.text = 'GAME: ' + version
            self.text[self.text_coords['pos_x']].label.text = 'X: ' + str(objects_display[list_main_game_obj['player']].pos[0])
            self.text[self.text_coords['pos_y']].label.text = 'Y: ' + str(objects_display[list_main_game_obj['player']].pos[1])
            self.text[self.text_coords['rot_body']].label.text = 'ROTATE BODY: ' + str(objects_display[list_main_game_obj['player']].rot_body)
            self.text[self.text_coords['rot_tower']].label.text = 'ROTATE TOWER: ' + str(objects_display[list_main_game_obj['player']].rot_tower)
            self.text[self.text_coords['start_engine']].label.text = 'ENGINE TANK: ' + str(objects_display[list_main_game_obj['player']].start_engine)
            self.text[self.text_coords['health']].label.text = 'HEALTH: ' + str(objects_display[list_main_game_obj['player']].health)

            self.text[self.text_coords['fps']].label.text = 'FPS: ' + str(pyglet.clock.get_fps())

    def draw(self): # рисуем
        if objects_other[0].draw_info_text:
            for text in self.text:
                text.draw()

class save_game():
    def __init__(self):
        self.name = 'PLAYER'
        self.money = 0
        self.persons = 5
        self.research_points = 0

        self.tanks = [
            ['tank_b', 'bgun', True, ''],
            ['tank_b', 'bgun', True, ''],
            ['tank_b', 'bgun', True, ''],
            ['tank_b', 'bgun', True, '']
        ]
'''
if not os.path.exists('save/user.pkl'):
    save_obj(save_game(), 'save/user')
    add_objects_other(load_obj('save/user'))
else:
    add_objects_other(load_obj('save/user'))
'''

def save_game_in_file():
    save_obj(objects_other[2], 'save/user')

add_objects_other(os_world())
