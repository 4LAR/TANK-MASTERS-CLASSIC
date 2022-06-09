#
#
#
#

import os
import multiprocessing
import termcolor

from get_time import *

#def print_char(x, y, char):
#    print("\033[" + str(y) + ";" + str(x) + "H" + char)

class console_term():
    def __init__(self, log_bool=True, log_time_bool=True):
        super().__init__()

        self.log_bool = log_bool
        self.log_time_bool = log_time_bool
        self.log_list = []
        if self.log_bool:
            open('log.txt', 'w').close()

        os.system('color')

        self.type_color = [
            'white',
            'green',
            'yellow',
            'red'
        ]

        self.type_color_RGBA = [
            (180, 180, 180, 255),
            (0, 180, 0, 255),
            (180, 180, 0, 255),
            (180, 0, 0, 255)
        ]

        self.promt = ""

        self.console = multiprocessing.Process(target=self.input_terminal)

        self.run = False

    def run_terminal(self):
        self.run = True
        self.console.start()

    def stop_terminal(self):
        self.run = False
        self.console.terminate()

    def input_terminal(self):
        while self.run:
            command = input(self.promt)
            self.exec(command)

    def exec(self, command):
        try:
            exec(command)

        except Exception as e:
            self.print(e, 3)

    def print(self, text, type=0):
        termcolor.cprint((('[' + str(get_time()) + '] ') if self.log_time_bool else '') + str(text), self.type_color[type])
        self.log_list.append([
            (('[' + str(get_time()) + '] ') if self.log_time_bool else '') + str(text),
            type
        ])
        if (self.log_bool):
            log_file = open('log.txt', 'a')
            log_file.write((('[' + str(get_time()) + '] ') if self.log_time_bool else '') + str(text) + '\n')
            log_file.close()
