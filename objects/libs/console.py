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
            console_term.print(exec(python_command)) # выполняем и выводим комманду

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
                    console_term.print(self.command) # выводим комманду
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
            list = console_term.log_list[len(console_term.log_list) - len(self.text) : len(console_term.log_list)]

            for i in range(len(self.text)-1):
                try:
                    lest_buf = list[len(self.text)-1 - i]
                    self.text[i].label.text = lest_buf[0]
                    self.text[i].label.color = console_term.type_color_RGBA[lest_buf[1]]
                    self.text[i].draw()
                except:
                    pass

            self.text[len(self.text)-1].label.text = self.command_ + self.command
            self.text[len(self.text)-1].draw()

add_objects_other(Console())
