#
#
#
#

import os
import hashlib

from console import *
from pickle_func import *

# функция для получения хэша
def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).digest()

# класс для сохранения всего кода в файл
class file_code():
    def __init__(self):
        self.files = [] # список файлов
        self.code = ''  # исходный код
        self.hash = ''  # хэш

class fuck_import(console_term):
    def __init__(self, path='objects'):
        super().__init__()

        self.error_promt = 'IMPORT: '

        self.path = path         # дтректория где будут лежать файлы
        self.main_file_name = '' # название основного списка

        self.code = ''  # здесь будет храниться код после сборки (build)
        self.files = [] # здесь будет храниться список файлов и размер каждого файла в строках

        self.read_file_bool = False
        self.build_file_bool = False

    # чтение списка файлов проекта
    def read(self, name='objects'):
        if (os.path.exists(self.path + '/' + name + '.list')):
            file_objects = (
                open(self.path + '/' + name + '.list', 'r', encoding="utf-8").read()
            ).split('\n')

            for file_name in file_objects:
                if (len(file_name) > 0):
                    if (file_name.split('.')[1] == 'list'):
                        self.read(file_name.split('.')[0])
                    else:
                        self.files.append(
                            [
                                (name + '.list').replace( # название и путь у файлу
                                    name.split('/')[len(name.split('/'))-1] + '.list',
                                    file_name
                                ),
                                0 # количество строк в файле (по умалочанию 0)
                            ]
                        )

            self.read_file_bool = True

        else:
            self.print(str(self.error_promt) + 'Source file opening error (' + str(name) + '.list)', 2)

    # сборка всех файлов из списка в код
    def build(self):
        if self.read_file_bool:
            self.code = ''
            for file_code_name in self.files:
                try:
                    file_code_buf = open(self.path + '/' + file_code_name[0], 'r', encoding="utf-8").read() + '\n'
                    file_code_name[1] = len(file_code_buf.split('\n'))
                    self.code += file_code_buf
                    self.print(str(self.error_promt) + str(file_code_name[0]), 0)

                except:
                    self.print(str(self.error_promt) + 'File opening error (' + str(file_code_name[0]) + ')', 2)

            self.build_file_bool = True

        else:
            self.print(str(self.error_promt) + 'File is not open', 3)

    # функция для сохранения всего кода в 1 собранный файл
    def pack(self, name):
        try:
            file_code_buf = file_code()
            file_code_buf.files = self.files
            file_code_buf.code = self.code
            file_code_buf.hash = get_hash(self.code)

            save_obj(file_code_buf, name)
            self.print(str(self.error_promt) + 'Code built successfully (' + name + '.pkl)', 1)
            return True

        except Exception as e:
            self.print(str(self.error_promt) + str(e), 3)
            return False

    # функция для чтения собранного файла
    def read_pack(self, name):
        if (os.path.exists(name + '.pkl')):
            file_code_buf = load_obj(name)

            if (get_hash(file_code_buf.code) == file_code_buf.hash):
                self.code = file_code_buf.code
                self.files = file_code_buf.files

                self.build_file_bool = True
                return True
            else:
                self.print(str(self.error_promt) + 'File is not valid', 3)
                return False

        else:
            self.print(str(self.error_promt) + 'Pack file opening error (' + str(name) + '.pkl)', 2)
            return False

    # возврат кода
    def get_code(self):
        if self.build_file_bool:
            return self.code

        else:
            self.print(str(self.error_promt) + 'File was not collected', 3)
            return False
